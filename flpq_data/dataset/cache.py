"""Machine-global, version-preserving cache for downloaded dataset data."""

import os
import pathlib
import shutil

import platformdirs

from flpq_data.config import DATASET_VERSION

__all__ = [
    "CACHE_ENV_VAR",
    "cache_root",
    "version_dir",
    "cached_versions",
    "clear_cache",
]

#: Environment variable overriding the cache root.
CACHE_ENV_VAR = "FLPQ_DATA_CACHE"


def cache_root() -> pathlib.Path:
    """Return the effective cache root.

    The ``FLPQ_DATA_CACHE`` environment variable wins when set to a
    non-empty value; otherwise the OS default from
    ``platformdirs.user_cache_dir("flpq-data")`` (``~/.cache/flpq-data`` on
    Linux, ``~/Library/Caches/flpq-data`` on macOS,
    ``%LOCALAPPDATA%\\flpq-data\\Cache`` on Windows).

    Returns
    -------
    root : pathlib.Path
        The cache root directory (not necessarily existing yet).
    """
    env = os.environ.get(CACHE_ENV_VAR)
    if env:
        return pathlib.Path(env)
    return pathlib.Path(platformdirs.user_cache_dir("flpq-data"))


def version_dir(version: str | None = None) -> pathlib.Path:
    """Return the cache directory of a dataset version.

    Parameters
    ----------
    version : str, optional
        The dataset version; defaults to the current one (the package major
        version with zeroed minor and patch).

    Returns
    -------
    path : pathlib.Path
        ``<cache_root>/<version>`` (not necessarily existing yet).
    """
    return cache_root() / (version or DATASET_VERSION)


def cached_versions() -> list[str]:
    """Return the dataset versions present in the cache.

    Returns
    -------
    versions : list of str
        The directory names under the cache root, sorted; empty when the
        root does not exist.
    """
    root = cache_root()
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def clear_cache(keep: str | None = None) -> list[pathlib.Path]:
    """Remove the cached dataset versions, optionally keeping one.

    Every version directory under the cache root is removed except the one
    named by ``keep``; ``keep=None`` removes all of them. Non-directory
    entries under the root are left untouched.

    Parameters
    ----------
    keep : str, optional
        The dataset version to keep (default ``None`` — remove everything).

    Examples
    --------
    >>> from flpq_data import *
    >>> clear_cache()  # doctest: +SKIP
    []

    Returns
    -------
    removed : list of Path
        The removed version directories, in sorted order; empty when the
        cache root does not exist or nothing was removed.
    """
    root = cache_root()
    if not root.is_dir():
        return []
    removed = [p for p in sorted(root.iterdir()) if p.is_dir() and p.name != keep]
    for path in removed:
        shutil.rmtree(path)
    return removed
