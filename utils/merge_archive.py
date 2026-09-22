"""Merge a partial archive into an existing graph archive.

A partial archive (validated with ``check_archive_structure.py --partial``)
provides new queries for an existing graph: it contains only ``queries/`` —
the new query directories plus a ``README.md`` fragment with their sections.
This tool copies the new query directories into the existing archive,
appends the README sections, re-validates the merged tree in full mode, and
writes the result as a new ``.tar.gz``.

The output file must be named after the graph (``<graph>.tar.gz``) — the
upload tool stores it under that name.

Usage (from any directory)::

    python utils/merge_archive.py EXISTING.tar.gz PARTIAL.tar.gz -o MERGED.tar.gz

``PARTIAL`` may also be an unpacked directory or a Google Drive URL / file ID
(the archive is downloaded first).
"""

import argparse
import pathlib
import re
import shutil
import tarfile
import tempfile
from typing import Optional, Sequence, Union

from check_archive_structure import (
    QUERY_CLASSES,
    parse_readme_sections,
    unpack_single_dir,
    validate_archive,
)
from migrate_gdrive_to_s3 import (
    DRIVE_FILE_ID_RE,
    DriveDownloadError,
    download_from_drive,
)

__all__ = ["merge_archives", "main"]


def _resolve_partial(source: str, tmp: pathlib.Path) -> pathlib.Path:
    """Return a local path for the partial archive source.

    ``source`` is an existing local path (a ``.tar.gz`` or an unpacked
    directory) or a Google Drive URL / file ID — in the latter case the
    archive is downloaded to ``tmp`` first.

    Raises
    ------
    ValueError
        If ``source`` is neither an existing local path nor a Google Drive
        URL / file ID.
    """
    source_path = pathlib.Path(source)
    if source_path.exists():
        return source_path
    match = DRIVE_FILE_ID_RE.search(source)
    if match is not None:
        file_id = match.group(1)
    elif re.fullmatch(r"[A-Za-z0-9_-]+", source):
        file_id = source  # a bare Drive file ID
    else:
        raise ValueError(
            f"{source}: no such file, and not a Google Drive URL or file ID"
        )
    downloaded = tmp / "partial.tar.gz"
    download_from_drive(file_id, downloaded)
    # Unpack so the archive can be validated like any directory; its
    # top-level name is checked against the existing graph below.
    return unpack_single_dir(downloaded, tmp / "partial")


def _append_sections(
    existing_text: str, fragment: dict[str, list[str]]
) -> tuple[str, list[str]]:
    """Append the fragment's sections to the existing README text.

    Returns the merged text and the problems found (a fragment section whose
    name already exists in the existing README).
    """
    problems = [
        f"queries/README.md: section {name!r} is already described in the "
        "existing archive"
        for name in fragment
        if name in parse_readme_sections(existing_text)
    ]
    if problems:
        return existing_text, problems
    merged = existing_text.rstrip("\n") + "\n"
    for name, body in fragment.items():
        merged += f"\n## {name}\n" + "\n".join(body).rstrip("\n") + "\n"
    return merged, []


def merge_archives(
    existing: Union[str, pathlib.Path],
    partial: Union[str, pathlib.Path],
    output: Union[str, pathlib.Path],
) -> list[str]:
    """Merge a partial archive into an existing one.

    Parameters
    ----------
    existing : Union[str, Path]
        The existing full graph archive (a ``.tar.gz`` or an unpacked
        directory).
    partial : Union[str, Path]
        The partial archive: a local ``.tar.gz``, an unpacked directory, or
        a Google Drive URL / file ID.
    output : Union[str, Path]
        Where to write the merged ``.tar.gz`` (named after the graph).

    Returns
    -------
    problems : list[str]
        All problems found; an empty list means the merged archive was
        written to ``output``.
    """
    output = pathlib.Path(output)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)

        # The partial source is resolved (downloaded, if needed) before any
        # validation, so it can be validated like a local archive.
        try:
            partial_local = _resolve_partial(str(partial), tmp_path)
        except (ValueError, DriveDownloadError) as error:
            return [f"partial archive: {error}"]

        problems = validate_archive(existing)
        if problems:
            return [f"existing archive: {p}" for p in problems]
        problems = validate_archive(partial_local, partial=True)
        if problems:
            return [f"partial archive: {p}" for p in problems]

        # Both inputs are treated read-only: the merge happens on a copy of
        # the existing tree, so a failed merge never leaves it half-merged.
        try:
            existing_source = pathlib.Path(existing)
            if existing_source.is_dir():
                # Keep the original directory name — the top-level-directory
                # and output-name checks depend on it.
                existing_root = tmp_path / "existing" / existing_source.name
                shutil.copytree(existing_source, existing_root)
            else:
                existing_root = unpack_single_dir(
                    existing_source, tmp_path / "existing"
                )
            partial_root = (
                partial_local
                if partial_local.is_dir()
                else unpack_single_dir(partial_local, tmp_path / "partial")
            )
        except ValueError as error:
            return [str(error)]

        problems = []
        if existing_root.name != partial_root.name:
            problems.append(
                f"the partial archive's top-level directory "
                f"{partial_root.name!r} must be named after the same graph "
                f"as the existing one ({existing_root.name!r})"
            )

        new_queries: list[tuple[str, pathlib.Path]] = []
        for cls in QUERY_CLASSES:
            cls_dir = partial_root / "queries" / cls
            if not cls_dir.is_dir():
                continue
            for query_dir in sorted(cls_dir.iterdir()):
                if not query_dir.is_dir():
                    continue  # reported by the partial validation
                new_queries.append((cls, query_dir))

        for cls, query_dir in new_queries:
            target = existing_root / "queries" / cls / query_dir.name
            if target.exists():
                problems.append(
                    f"queries/{cls}/{query_dir.name}: already exists in the "
                    "existing archive"
                )

        fragment = parse_readme_sections(
            (partial_root / "queries" / "README.md").read_text(encoding="utf-8")
        )
        if not problems:
            for cls, query_dir in new_queries:
                shutil.copytree(
                    query_dir, existing_root / "queries" / cls / query_dir.name
                )
            readme = existing_root / "queries" / "README.md"
            merged_text, readme_problems = _append_sections(
                readme.read_text(encoding="utf-8"), fragment
            )
            problems.extend(readme_problems)
            if not readme_problems:
                readme.write_text(merged_text, encoding="utf-8")

        if problems:
            return problems

        problems = validate_archive(existing_root)
        if problems:
            return [f"merged archive: {p}" for p in problems]

        if output.name != f"{existing_root.name}.tar.gz":
            return [
                f"the output file must be named {existing_root.name}.tar.gz "
                f"(the upload tool stores it under that name), got {output.name!r}"
            ]
        with tarfile.open(output, "w:gz") as tarball:
            tarball.add(existing_root, arcname=existing_root.name)
        return []


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Command-line entry point.

    Returns
    -------
    status : int
        0 when the merged archive was written, 1 otherwise.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Merge a partial archive (new queries for an existing graph) "
            "into the existing graph archive."
        )
    )
    parser.add_argument(
        "existing",
        help="the existing full graph archive (.tar.gz or unpacked directory)",
    )
    parser.add_argument(
        "partial",
        help=(
            "the partial archive: a .tar.gz, an unpacked directory, or a "
            "Google Drive URL / file ID"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="where to write the merged .tar.gz (named after the graph)",
    )
    args = parser.parse_args(argv)

    problems = merge_archives(args.existing, args.partial, args.output)
    if problems:
        for problem in problems:
            print(f"error: {problem}")
        print(f"{len(problems)} problem(s) found; the merged archive was not written")
        return 1
    print(f"merged archive written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
