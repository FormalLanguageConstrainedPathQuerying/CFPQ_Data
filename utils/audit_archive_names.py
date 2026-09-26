"""Audit dataset archives for non-canonical indexed-label file names.

The canonical file name of an edge label is the label itself
(``load_5.mtx``). Older archives use the ``_i`` placeholder style
(``load_i_5.mtx`` holds the edges labeled ``load_5``); this tool lists the
archives that still contain such files.

Usage::

    python utils/audit_archive_names.py [--names NAME ...]
"""

import argparse
import re
import tarfile
from typing import Iterable, Optional, Sequence

import requests

from flpq_data.dataset.data import DATASET, DATASET_URL

__all__ = [
    "INDEXED_NAME_RE",
    "find_indexed_names",
    "list_members",
    "main",
]

#: A MatrixMarket file name that uses the ``_i`` placeholder for the real
#: index of an indexed label (``load_i_5.mtx`` holds the label ``load_5``).
INDEXED_NAME_RE = re.compile(r".*_i_\d+\.mtx$")


def find_indexed_names(members: Iterable[str]) -> list[str]:
    """Returns the archive member names that use the ``_i`` placeholder style.

    Parameters
    ----------
    members : Iterable[str]
        The names of the archive members.

    Examples
    --------
    >>> find_indexed_names(["g/load_5.mtx", "g/load_i_5.mtx", "README.md"])
    ['g/load_i_5.mtx']

    Returns
    -------
    indexed : list[str]
        The member names that use the ``_i`` placeholder style.
    """
    return [name for name in members if INDEXED_NAME_RE.search(name)]


def list_members(url: str) -> list[str]:
    """Streams the archive at `url` and returns its member names."""
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with tarfile.open(fileobj=r.raw, mode="r|gz") as tf:
            return tf.getnames()


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Audits the dataset archives and reports the ``_i`` placeholder users."""
    parser = argparse.ArgumentParser(
        description=(
            "List the dataset archives that contain indexed-label files with "
            "the `_i` placeholder style."
        )
    )
    parser.add_argument(
        "--names", nargs="*", default=None, help="graph names to audit (default: all)"
    )
    args = parser.parse_args(argv)

    names = args.names or DATASET
    affected = []
    for name in names:
        url = DATASET_URL + f"{name}.tar.gz"
        indexed = find_indexed_names(list_members(url))
        if indexed:
            affected.append((name, len(indexed)))
            print(f"AFFECTED {name}: {len(indexed)} indexed files")

    print(f"\n{len(affected)} of {len(names)} archives use the `_i` placeholder style")


if __name__ == "__main__":
    main()
