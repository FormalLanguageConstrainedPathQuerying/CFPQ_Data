"""Reference reachable-pair counts for graph x grammar pairs."""

import csv
import pathlib
from typing import Optional

__all__ = [
    "REACHABLE_PAIRS_CSV",
    "reachable_pairs",
]

REACHABLE_PAIRS_CSV: pathlib.Path = (
    pathlib.Path(__file__).parent / "reachable_pairs.csv"
)


def reachable_pairs(
    graph: Optional[str] = None,
    grammar: Optional[str] = None,
    category: Optional[str] = None,
) -> list[dict]:
    """Return reference reachable-pair counts.

    Each row is a dict with keys ``graph``, ``grammar``, ``category``, and
    ``num_reachable_pairs`` (int or None when not yet available).

    Parameters
    ----------
    graph:
        Filter by graph name (exact match).
    grammar:
        Filter by grammar file name (exact match, e.g. ``"c_alias.cnf"``).
    category:
        Filter by graph category (exact match, e.g. ``"rdf"``); the
        categories are the sections of the Graphs catalog on the site.
    """
    rows: list[dict] = []
    with REACHABLE_PAIRS_CSV.open(newline="") as f:
        for row in csv.DictReader(f):
            if graph is not None and row["graph"] != graph:
                continue
            if grammar is not None and row["grammar"] != grammar:
                continue
            if category is not None and row["category"] != category:
                continue
            val = row["num_reachable_pairs"]
            rows.append(
                {
                    "graph": row["graph"],
                    "grammar": row["grammar"],
                    "category": row["category"],
                    "num_reachable_pairs": int(val) if val else None,
                }
            )
    return rows
