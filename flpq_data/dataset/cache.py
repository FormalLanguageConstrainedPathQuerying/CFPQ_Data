"""Machine-global, version-preserving cache for downloaded dataset data."""

import os
import pathlib

import platformdirs

from flpq_data.config import DATASET_VERSION

__all__ = [
    "CACHE_ENV_VAR",
    "cache_root",
    "version_dir",
    "cached_versions",
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
