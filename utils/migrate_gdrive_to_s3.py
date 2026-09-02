"""Migrate graph archives from Google Drive to Yandex Object Storage.

Handles items one by one: download an archive from Google Drive, upload it
to the cfpq-data bucket (via utils/upload_to_s3.py), remove the local copy,
and point the docs at the new Yandex URL. Items already present on Yandex
are skipped, so re-running the tool is safe.
"""

import argparse
import hashlib
import json
import logging
import pathlib
import re
import shutil
import tempfile
from dataclasses import dataclass

import requests

from cfpq_data.dataset import DATASET, DATASET_URL
from upload_to_s3 import (
    DEFAULT_BUCKET,
    DEFAULT_ENDPOINT_URL,
    create_s3_client,
    upload_file,
)

__all__ = [
    "MigrationItem",
    "DriveDownloadError",
    "MigrationError",
    "discover_items",
    "download_from_drive",
    "sha256_of",
    "is_on_yandex",
    "update_docs",
    "load_mapping",
    "save_mapping",
    "migrate",
    "main",
]

DRIVE_FILE_ID_RE = re.compile(
    r"drive\.google\.com/(?:uc\?export=download&id=|file/d/)([A-Za-z0-9_-]+)"
)
FULL_NAME_RE = re.compile(r"Full Name\s*\n\s*- (\S+)")
DRIVE_DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id={file_id}"
DRIVE_REQUEST_TIMEOUT = 300
DRIVE_URL_FORMS = (
    "https://drive.google.com/uc?export=download&id={file_id}",
    "https://drive.google.com/file/d/{file_id}/view?usp=sharing",
)

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
DEFAULT_DOCS_DIR = SCRIPT_DIR.parent / "docs"
DEFAULT_MAPPING_PATH = SCRIPT_DIR / "migration_mapping.json"


@dataclass(frozen=True)
class MigrationItem:
    """A graph archive hosted on Google Drive.

    Attributes
    ----------
    name : str
        Graph name; also the S3 object key stem (``<name>.tar.gz``).
    file_id : str
        Google Drive file ID of the archive.
    source : str
        Path of the docs page where the item was found, relative to the
        docs directory.
    """

    name: str
    file_id: str
    source: str


def _direct_download_file_id(text: str) -> str | None:
    """Return the Drive file ID from the "Direct download" row of a page."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "Direct download" in line:
            for j in range(i + 1, min(i + 3, len(lines))):
                match = DRIVE_FILE_ID_RE.search(lines[j])
                if match:
                    return match.group(1)
    return None


def discover_items(docs_dir: pathlib.Path | str) -> list[MigrationItem]:
    """Collect all graph archives linked from the docs to Google Drive.

    Parameters
    ----------
    docs_dir : Union[str, Path]
        The documentation directory (contains ``graphs/data`` and
        ``old_graphs/data``).

    Returns
    -------
    items : list of MigrationItem
        One item per unique Drive file ID. Only the "Direct download"
        archive is considered; "Origin" files (``.txt``, ``.xml.tar.gz``)
        are ignored. The object key name is the rst stem for old-collection
        graphs (stems in :data:`cfpq_data.dataset.DATASET`) and the page's
        "Full Name" otherwise.
    """
    docs_dir = pathlib.Path(docs_dir)
    items: list[MigrationItem] = []
    seen_file_ids: set[str] = set()

    for sub in ("graphs/data", "old_graphs/data"):
        data_dir = docs_dir / sub
        if not data_dir.is_dir():
            continue
        for rst in sorted(data_dir.glob("*.rst")):
            text = rst.read_text(encoding="utf-8")
            file_id = _direct_download_file_id(text)
            if file_id is None or file_id in seen_file_ids:
                continue
            seen_file_ids.add(file_id)

            match = FULL_NAME_RE.search(text)
            full_name = match.group(1) if match else rst.stem
            name = rst.stem if rst.stem in DATASET else full_name

            items.append(
                MigrationItem(
                    name=name,
                    file_id=file_id,
                    source=f"{sub}/{rst.name}",
                )
            )

    return items


class DriveDownloadError(Exception):
    """Raised when a Google Drive download fails."""


def _parse_confirm_form(html: str) -> tuple[str, dict[str, str]] | None:
    """Parse the Drive confirmation form into (action url, hidden inputs)."""
    action_match = re.search(r'action="([^"]+)"', html)
    if action_match is None:
        return None
    params = dict(
        re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', html)
    )
    return action_match.group(1), params


def download_from_drive(file_id: str, dest_path: pathlib.Path | str) -> pathlib.Path:
    """Download a file from Google Drive to ``dest_path``.

    Small files are served directly as a binary response; large files first
    return an HTML confirmation form (virus-scan warning page), whose action
    URL is then requested with the form's hidden inputs.

    Parameters
    ----------
    file_id : str
        Google Drive file ID.
    dest_path : Union[str, Path]
        Local path to write the file to.

    Returns
    -------
    dest_path : Path
        The path the file was written to.

    Raises
    ------
    DriveDownloadError
        If Drive returns an error page or an empty file.
    """
    dest_path = pathlib.Path(dest_path)
    session = requests.Session()
    response = session.get(
        DRIVE_DOWNLOAD_URL.format(file_id=file_id),
        stream=True,
        timeout=DRIVE_REQUEST_TIMEOUT,
    )
    try:
        if "text/html" in (response.headers.get("content-type") or ""):
            form = _parse_confirm_form(response.content.decode("utf-8", "replace"))
            if form is None:
                raise DriveDownloadError(
                    f"Google Drive returned an error page for file {file_id}"
                )
            action, params = form
            response.close()
            response = session.get(
                action, params=params, stream=True, timeout=DRIVE_REQUEST_TIMEOUT
            )
            if "text/html" in (response.headers.get("content-type") or ""):
                raise DriveDownloadError(
                    f"Google Drive returned an error page for file {file_id}"
                )
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(response.raw, f)
    finally:
        response.close()

    if dest_path.stat().st_size == 0:
        dest_path.unlink(missing_ok=True)
        raise DriveDownloadError(
            f"Google Drive returned an empty file for file {file_id}"
        )

    return dest_path


class MigrationError(Exception):
    """Raised when a migration item cannot be processed safely."""


def sha256_of(path: pathlib.Path | str) -> str:
    """Return the SHA-256 hex digest of a local file."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_on_yandex(name: str) -> bool:
    """Check whether ``<name>.tar.gz`` is already stored on Yandex.

    Uses the public bucket URL, so no credentials are needed. Network
    errors count as "not present" (the following download/upload will then
    fail with a clear error).
    """
    url = DATASET_URL + f"{name}.tar.gz"
    try:
        with requests.head(url, timeout=30) as response:
            return response.status_code == 200
    except requests.RequestException:
        return False


def update_docs(docs_dir: pathlib.Path | str, file_id: str, new_url: str) -> int:
    """Replace all Drive URLs of ``file_id`` in the docs with ``new_url``.

    Both URL forms (``uc?export=download`` and ``file/d/<id>/view``) are
    replaced in every ``*.rst`` file under ``docs_dir`` except the ``_build``
    directory.

    Returns the number of files changed.
    """
    docs_dir = pathlib.Path(docs_dir)
    changed = 0
    for rst in sorted(docs_dir.rglob("*.rst")):
        if "_build" in rst.parts:
            continue
        text = rst.read_text(encoding="utf-8")
        new_text = text
        for form in DRIVE_URL_FORMS:
            new_text = new_text.replace(form.format(file_id=file_id), new_url)
        if new_text != text:
            rst.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def load_mapping(path: pathlib.Path | str) -> dict[str, dict]:
    """Load the name -> {url, drive_file_id, sha256} mapping ({} if absent)."""
    path = pathlib.Path(path)
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_mapping(path: pathlib.Path | str, mapping: dict[str, dict]) -> None:
    """Persist the mapping after every item so progress survives interrupts."""
    path = pathlib.Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, sort_keys=True)
        f.write("\n")


def migrate(
    items: list[MigrationItem],
    client,
    bucket: str,
    docs_dir: pathlib.Path | str,
    workdir: pathlib.Path | str,
    mapping_path: pathlib.Path | str,
    limit: int | None = None,
) -> dict[str, int]:
    """Migrate items from Google Drive to Yandex, one item at a time.

    For each item (at most one local file on disk at any time):

    - if the name is already in the mapping with a recorded SHA-256, the
      archive is downloaded and its digest compared with the recorded one:
      equal means the same graph (must not be stored twice) so the upload is
      skipped; different raises :class:`MigrationError` and keeps the local
      copy for inspection;
    - else if the object already exists on Yandex (public HEAD check), the
      item is skipped without downloading — this also covers re-runs of
      entries recorded without a hash by a previous skip;
    - else the archive is downloaded, uploaded via ``upload_file`` (verified
      upload) and recorded in the mapping.

    Afterwards the item's Drive URLs are replaced with the new Yandex URL in
    the docs and the mapping is saved. On success the local copy is removed;
    on any error it is kept and the error re-raised, so a re-run resumes
    where this one stopped.

    Returns a summary: ``{"uploaded": n, "skipped_existing": n,
    "skipped_duplicate": n}``.
    """
    docs_dir = pathlib.Path(docs_dir)
    workdir = pathlib.Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    mapping = load_mapping(mapping_path)

    summary = {"uploaded": 0, "skipped_existing": 0, "skipped_duplicate": 0}

    for index, item in enumerate(items):
        if limit is not None and index >= limit:
            break

        url = DATASET_URL + f"{item.name}.tar.gz"
        local_path = workdir / f"{item.name}.tar.gz"

        try:
            recorded = mapping.get(item.name, {}).get("sha256")
            if recorded is not None:
                download_from_drive(item.file_id, local_path)
                digest = sha256_of(local_path)
                if digest != recorded:
                    raise MigrationError(
                        f"Content mismatch for graph {item.name!r}: Drive file "
                        f"{item.file_id} has sha256 {digest}, but the stored copy "
                        f"was recorded as {recorded}. Local copy kept at "
                        f"{local_path} for inspection."
                    )
                logging.info(
                    f"{item.name}: content identical to the stored copy, "
                    f"skipping upload"
                )
                summary["skipped_duplicate"] += 1
            elif is_on_yandex(item.name):
                logging.info(f"{item.name}: already on Yandex, skipping")
                mapping[item.name] = {
                    "url": url,
                    "drive_file_id": item.file_id,
                    "sha256": None,
                }
                summary["skipped_existing"] += 1
            else:
                download_from_drive(item.file_id, local_path)
                digest = sha256_of(local_path)
                upload_file(client, local_path, bucket, key=f"{item.name}.tar.gz")
                mapping[item.name] = {
                    "url": url,
                    "drive_file_id": item.file_id,
                    "sha256": digest,
                }
                summary["uploaded"] += 1

            changed = update_docs(docs_dir, item.file_id, url)
            logging.info(f"{item.name}: updated {changed} doc file(s) to {url}")
            save_mapping(mapping_path, mapping)

            if local_path.exists():
                local_path.unlink()
                logging.info(f"{item.name}: removed local copy {local_path}")
        except Exception:
            if local_path.exists():
                logging.error(
                    f"{item.name}: keeping local copy at {local_path} for inspection"
                )
            raise

    return summary


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point.

    Usage::

        python utils/migrate_gdrive_to_s3.py \\
            --access-key-id KEY_ID --secret-access-key SECRET \\
            [--endpoint-url URL] [--bucket BUCKET] \\
            [--docs-dir DIR] [--workdir DIR] [--mapping FILE] \\
            [--limit N] [--dry-run]

    Credentials are always taken from the command line and are never read
    from environment variables or config files.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Migrate graph archives from Google Drive to Yandex Object "
            "Storage, one item at a time."
        )
    )
    parser.add_argument(
        "--access-key-id", required=True, help="Yandex Cloud IAM key ID"
    )
    parser.add_argument(
        "--secret-access-key",
        required=True,
        help="Yandex Cloud IAM secret key",
    )
    parser.add_argument(
        "--endpoint-url",
        default=DEFAULT_ENDPOINT_URL,
        help=f"S3 API endpoint (default: {DEFAULT_ENDPOINT_URL})",
    )
    parser.add_argument(
        "--bucket",
        default=DEFAULT_BUCKET,
        help=f"target bucket (default: {DEFAULT_BUCKET})",
    )
    parser.add_argument(
        "--docs-dir",
        default=str(DEFAULT_DOCS_DIR),
        help=f"documentation directory (default: {DEFAULT_DOCS_DIR})",
    )
    parser.add_argument(
        "--workdir",
        default=None,
        help="directory for temporary downloads (default: a new temp dir)",
    )
    parser.add_argument(
        "--mapping",
        default=str(DEFAULT_MAPPING_PATH),
        help=f"name -> URL mapping file (default: {DEFAULT_MAPPING_PATH})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="migrate at most N items (for testing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report the plan without downloading, uploading or modifying "
        "docs/mapping",
    )
    args = parser.parse_args(argv)

    docs_dir = pathlib.Path(args.docs_dir)
    items = discover_items(docs_dir)
    if not items:
        print("No Google Drive items found in the docs; nothing to migrate.")
        return

    if args.dry_run:
        mapping = load_mapping(args.mapping)
        planned = items[: args.limit] if args.limit is not None else items
        for item in planned:
            if item.name in mapping:
                plan = "skip (name already migrated; content will be rechecked)"
            elif is_on_yandex(item.name):
                plan = "skip (already on Yandex)"
            else:
                plan = "upload"
            print(f"{item.name}: {plan} [{item.source}]")
        return

    workdir = (
        pathlib.Path(args.workdir)
        if args.workdir
        else pathlib.Path(tempfile.mkdtemp(prefix="cfpq_migration_"))
    )
    client = create_s3_client(
        args.access_key_id, args.secret_access_key, args.endpoint_url
    )
    summary = migrate(
        items,
        client,
        args.bucket,
        docs_dir,
        workdir,
        args.mapping,
        limit=args.limit,
    )
    print(
        f"Done: {summary['uploaded']} uploaded, "
        f"{summary['skipped_existing']} already on Yandex, "
        f"{summary['skipped_duplicate']} duplicates (content identical)."
    )


if __name__ == "__main__":
    main()
