"""Download graph data from dataset."""

import hashlib
import logging
import os
import pathlib
import shutil
import tempfile
import warnings

import requests

from flpq_data.config import DATASET_VERSION
from flpq_data.dataset.cache import version_dir
from flpq_data.dataset.registry import GraphInfo, graph_info

__all__ = [
    "DATASET_KEY_PREFIX",
    "DATASET_URL",
    "graph_dir",
    "download_graph",
    "download",
]

DATASET_KEY_PREFIX = f"{DATASET_VERSION}/graph"
DATASET_URL = f"https://cfpq-data.storage.yandexcloud.net/{DATASET_KEY_PREFIX}/"


def _sha256(path: pathlib.Path) -> str:
    """Returns the streaming sha256 hex digest of a file."""
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _install(name: str, info: GraphInfo, dest: pathlib.Path) -> None:
    """Download, verify, and install the archive of ``name`` into ``dest``.

    The download is streamed to a temp file with a running sha256; only a
    verified archive is unpacked and moved into place, so any failure leaves
    ``dest`` untouched and removes the temp files.
    """
    parent = dest.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_archive_str = tempfile.mkstemp(dir=parent, suffix=".tar.gz")
    os.close(fd)
    tmp_archive = pathlib.Path(tmp_archive_str)
    tmp_extract: pathlib.Path | None = None
    try:
        logging.info(f"Downloading {DATASET_URL}{name}.tar.gz")
        with requests.get(url=DATASET_URL + f"{name}.tar.gz", stream=True) as r:
            r.raise_for_status()
            hasher = hashlib.sha256()
            with tmp_archive.open("wb") as out:
                for chunk in iter(lambda: r.raw.read(1 << 20), b""):
                    hasher.update(chunk)
                    out.write(chunk)
        digest = hasher.hexdigest()
        if digest != info.sha256:
            raise ValueError(
                f"sha256 mismatch for {name}: expected {info.sha256}, got {digest}"
            )

        tmp_extract = pathlib.Path(tempfile.mkdtemp(dir=parent))
        shutil.unpack_archive(tmp_archive, tmp_extract)

        entries = list(tmp_extract.iterdir())
        if len(entries) != 1 or not entries[0].is_dir():
            raise ValueError(
                f"Archive for {name=} must contain a single "
                f"top-level directory, found {entries=}"
            )

        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(entries[0]), str(dest))
        shutil.move(str(tmp_archive), str(dest / f"{name}.tar.gz"))
        (dest / f"{name}.tar.gz.sha256").write_text(digest + "\n")

        logging.info(f"Installed graph {name=} to directory {dest=}")
    finally:
        if tmp_archive.exists():
            tmp_archive.unlink()
        if tmp_extract is not None and tmp_extract.exists():
            shutil.rmtree(tmp_extract, ignore_errors=True)


def graph_dir(name: str, verify: bool = False) -> pathlib.Path:
    """Return the local directory of a graph, downloading it on a cache miss.

    The data lives in the machine-global cache (see :func:`cache_root`),
    mirroring the dataset layout::

       <root>/<version>/graph/<name>/<name>.tar.gz   plus the unpacked
                                                    contents in the same folder

    A cache hit — the folder and archive are present and the digest matches
    the registry — returns the path with zero network. The digest is read
    from the ``<name>.tar.gz.sha256`` sidecar written at install;
    ``verify=True`` re-hashes the archive instead of trusting the sidecar.
    On a miss the archive is downloaded, its sha256 is verified against the
    registry while streaming, it is unpacked (a single top-level directory
    is required), and the result is moved into the cache; any failure leaves
    the cache untouched.

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.
    verify : bool, optional
        Re-hash the cached archive against the registry instead of trusting
        the sidecar digest (default ``False``).

    Examples
    --------
    >>> from flpq_data import *
    >>> path = graph_dir("generations")
    >>> path.name
    'generations'

    Returns
    -------
    path : Path
        Path to the directory with the graph data.

    Raises
    ------
    FileNotFoundError
        If no graph with this name exists in the dataset.
    """
    info = graph_info(name)
    dest = version_dir() / "graph" / name
    archive = dest / f"{name}.tar.gz"
    sidecar = archive.with_name(archive.name + ".sha256")

    if dest.is_dir() and archive.is_file():
        if verify:
            digest = _sha256(archive)
        else:
            digest = sidecar.read_text().strip() if sidecar.is_file() else None
        if digest == info.sha256:
            logging.info(f"Cache hit for graph {name=}")
            return dest

    _install(name, info, dest)
    return dest


def download_graph(name: str) -> pathlib.Path:
    """Deprecated alias of :func:`graph_dir`.

    .. deprecated:: 6.0.0
        Use :func:`graph_dir` instead.
    """
    warnings.warn(
        "download_graph() is deprecated, use graph_dir() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return graph_dir(name)


def download(name: str) -> pathlib.Path:
    """Deprecated alias of :func:`graph_dir`.

    .. deprecated:: 6.0.0
        Use :func:`graph_dir` instead.
    """
    warnings.warn(
        "download() is deprecated, use graph_dir() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return graph_dir(name)
