"""Reference reachable-pair counts for graph x grammar pairs."""

import csv
import logging
import pathlib
import shutil
from typing import Optional

import requests

from flpq_data.config import DATASET_VERSION
from flpq_data.dataset.cache import version_dir

__all__ = [
    "REACHABLE_PAIRS_CSV",
    "REACHABLE_PAIRS_KEY_PREFIX",
    "REACHABLE_PAIRS_URL",
    "download_reachable_pairs",
    "reachable_pairs",
]

REACHABLE_PAIRS_FILENAME = "reachable_pairs.csv"

#: Version prefix the table is published under on the dataset object storage.
#: Derived from :data:`flpq_data.config.DATASET_VERSION`, so the URL follows
#: the package version.
REACHABLE_PAIRS_KEY_PREFIX: str = DATASET_VERSION

#: Public URL of the versioned reachable-pairs CSV (see
#: :func:`download_reachable_pairs`).
REACHABLE_PAIRS_URL: str = (
    f"https://cfpq-data.storage.yandexcloud.net/"
    f"{REACHABLE_PAIRS_KEY_PREFIX}/{REACHABLE_PAIRS_FILENAME}"
)

#: Path to the reference CSV shipped with the package; always available
#: offline. :func:`download_reachable_pairs` fetches the versioned copy from
#: the dataset storage instead, and :func:`reachable_pairs` prefers it when
#: present.
REACHABLE_PAIRS_CSV: pathlib.Path = (
    pathlib.Path(__file__).parent / REACHABLE_PAIRS_FILENAME
)


def download_reachable_pairs() -> pathlib.Path:
    """Download the versioned reachable-pairs CSV from the dataset storage.

    The table is also shipped with the package (``REACHABLE_PAIRS_CSV``);
    this fetches the copy published under the current version prefix
    (``REACHABLE_PAIRS_URL``) into the machine-global cache
    (``version_dir() / "reachable_pairs.csv"``), so an updated table can be
    consumed without reinstalling. Once downloaded, :func:`reachable_pairs`
    reads it instead of the bundled copy.

    Returns
    -------
    path : pathlib.Path
        Path to the downloaded CSV.

    Raises
    ------
    requests.HTTPError
        If the table is not available at ``REACHABLE_PAIRS_URL``.
    """
    destination = version_dir() / REACHABLE_PAIRS_FILENAME
    destination.parent.mkdir(exist_ok=True, parents=True)
    logging.info(f"Downloading reachable pairs CSV from {REACHABLE_PAIRS_URL}")
    with requests.get(url=REACHABLE_PAIRS_URL, stream=True) as response:
        response.raise_for_status()
        with open(destination, "wb") as file:
            shutil.copyfileobj(response.raw, file)
    logging.info(f"Downloaded reachable pairs CSV to {destination}")
    return destination


def _csv_path() -> pathlib.Path:
    """Returns the CSV to read: the per-version cache copy if present, else bundled."""
    cached = version_dir() / REACHABLE_PAIRS_FILENAME
    return cached if cached.exists() else REACHABLE_PAIRS_CSV


def reachable_pairs(
    graph: Optional[str] = None,
    grammar: Optional[str] = None,
    category: Optional[str] = None,
    query_class: Optional[str] = None,
) -> list[dict]:
    """Return reference reachable-pair counts.

    Each row is a dict with keys ``graph``, ``grammar``, ``category``,
    ``query_class``, and ``num_reachable_pairs`` (int or None when not yet
    available).

    Parameters
    ----------
    graph:
        Filter by graph name (exact match).
    grammar:
        Filter by grammar file name (exact match, e.g. ``"c_alias.cnf"``).
    category:
        Filter by graph category (exact match, e.g. ``"rdf"``); the
        categories are the sections of the Graphs catalog on the site.
    query_class:
        Filter by query class (exact match, one of ``"cfpq"``, ``"rpq"``,
        ``"mcfpq"`` — the names of the ``queries/<class>/`` directories in
        the graph archives).
    """
    rows: list[dict] = []
    with _csv_path().open(newline="") as f:
        for row in csv.DictReader(f):
            if graph is not None and row["graph"] != graph:
                continue
            if grammar is not None and row["grammar"] != grammar:
                continue
            if category is not None and row["category"] != category:
                continue
            if query_class is not None and row["query_class"] != query_class:
                continue
            val = row["num_reachable_pairs"]
            rows.append(
                {
                    "graph": row["graph"],
                    "grammar": row["grammar"],
                    "category": row["category"],
                    "query_class": row["query_class"],
                    "num_reachable_pairs": int(val) if val else None,
                }
            )
    return rows
