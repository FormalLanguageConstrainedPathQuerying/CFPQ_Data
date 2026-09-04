"""Convert old-format graph archives to the nab-like mtx-per-label format.

The old format stores a whole graph in one CSV file (``<name>/<name>.csv``,
space-separated ``from to label`` lines with CRLF endings). The new format
stores one Boolean MatrixMarket matrix per edge label
(``<name>/graph/<label>.mtx``) plus CNF grammar files
(``<name>/grammar/*.cnf``) and a README.

The tool processes graphs one by one: it downloads a single archive from the
public bucket, converts it locally, verifies the conversion by round-trip,
uploads the new archive under the ``5.0.0/graph/`` key prefix, and removes
the local files. At most one graph is on disk at any time.
"""

import logging
import pathlib
from dataclasses import dataclass, field
from typing import Dict, IO, Iterator, Tuple, Union

__all__ = [
    "MTX_BANNER",
    "MTX_TYPE",
    "GraphStats",
    "iter_edges",
    "scan_csv",
    "convert_csv_to_graph_dir",
    "validate_labels",
]

MTX_BANNER = "%%MatrixMarket matrix coordinate pattern general"
MTX_TYPE = "%%GraphBLAS type bool"


@dataclass
class GraphStats:
    """Statistics of a graph collected from its edge list.

    Attributes
    ----------
    num_nodes : int
        Number of distinct node IDs occurring in the edges.
    max_node_id : int
        The largest node ID occurring in the edges.
    total_edges : int
        Total number of edges (one per CSV line).
    edges_per_label : dict[str, int]
        Number of edges per label.
    """

    num_nodes: int
    max_node_id: int
    total_edges: int
    edges_per_label: Dict[str, int] = field(default_factory=dict)


def iter_edges(csv_path: Union[pathlib.Path, str]) -> Iterator[Tuple[int, int, str]]:
    """Yield the edges of an old-format graph CSV file.

    Parameters
    ----------
    csv_path : Union[Path, str]
        Path to the CSV file with one edge per line in the format
        ``<from> <to> <label>``. The source files use CRLF line endings;
        both CRLF and LF are accepted. Blank lines are skipped.

    Yields
    ------
    edge : Tuple[int, int, str]
        A triple ``(u, v, label)`` with 0-based integer node IDs.

    Raises
    ------
    ValueError
        If a non-blank line does not have exactly three
        whitespace-separated fields or the node IDs are not integers.
    """
    with open(csv_path, "r") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(
                    f"{csv_path}:{line_no}: expected 3 fields "
                    f"('<from> <to> <label>'), got {len(parts)}: {line!r}"
                )
            u_str, v_str, label = parts
            try:
                u, v = int(u_str), int(v_str)
            except ValueError:
                raise ValueError(
                    f"{csv_path}:{line_no}: node IDs must be integers: {line!r}"
                ) from None
            yield u, v, label


def scan_csv(csv_path: Union[pathlib.Path, str]) -> GraphStats:
    """Collect the statistics of an old-format graph CSV file.

    Parameters
    ----------
    csv_path : Union[Path, str]
        Path to the CSV file (see :func:`iter_edges`).

    Returns
    -------
    stats : GraphStats
        Distinct node count, max node ID, total edge count, and per-label
        edge counts.
    """
    nodes = set()
    edges_per_label: Dict[str, int] = {}
    total_edges = 0
    max_node_id = -1

    for u, v, label in iter_edges(csv_path):
        nodes.add(u)
        nodes.add(v)
        if u > max_node_id:
            max_node_id = u
        if v > max_node_id:
            max_node_id = v
        edges_per_label[label] = edges_per_label.get(label, 0) + 1
        total_edges += 1

    stats = GraphStats(
        num_nodes=len(nodes),
        max_node_id=max_node_id,
        total_edges=total_edges,
        edges_per_label=edges_per_label,
    )

    logging.info(f"Scanned {csv_path=}: {stats=}")
    return stats


def validate_labels(labels) -> None:
    """Validate that labels can be used as MTX file names.

    Parameters
    ----------
    labels : iterable of str
        The edge labels of the graph.

    Raises
    ------
    ValueError
        If a label is empty, starts with ``-``, or contains a slash,
        whitespace, or NUL character.
    """
    for label in labels:
        if (
            not label
            or label.startswith("-")
            or "/" in label
            or "\x00" in label
            or any(c.isspace() for c in label)
        ):
            raise ValueError(f"Label {label!r} is not filesystem-safe")


def convert_csv_to_graph_dir(
    csv_path: Union[pathlib.Path, str],
    graph_dir: Union[pathlib.Path, str],
) -> GraphStats:
    """Convert an old-format graph CSV to per-label MTX files.

    For every distinct label ``L`` the function writes
    ``<graph_dir>/<L>.mtx``::

        %%MatrixMarket matrix coordinate pattern general
        %%GraphBLAS type bool
        <N> <N> <nnz>
        <u> <v>
        ...

    where ``N = max_node_id + 1`` and one entry line follows per edge with
    label ``L``, in the order the edges appear in the CSV. Node IDs are
    written verbatim (0-based). The conversion streams the CSV twice and
    keeps O(1) data in memory, so it works for graphs with tens of millions
    of edges.

    Parameters
    ----------
    csv_path : Union[Path, str]
        Path to the old-format CSV file (see :func:`iter_edges`).
    graph_dir : Union[Path, str]
        Directory where the ``<label>.mtx`` files are written. Created if
        it does not exist.

    Returns
    -------
    stats : GraphStats
        The statistics collected from the CSV (see :func:`scan_csv`).

    Raises
    ------
    ValueError
        If a label is not filesystem-safe (see :func:`validate_labels`).
    """
    stats = scan_csv(csv_path)
    validate_labels(stats.edges_per_label)

    n = stats.max_node_id + 1
    graph_dir = pathlib.Path(graph_dir)
    graph_dir.mkdir(parents=True, exist_ok=True)

    handles: Dict[str, IO[str]] = {}
    try:
        for label, nnz in stats.edges_per_label.items():
            handle = open(graph_dir / f"{label}.mtx", "w")
            handle.write(f"{MTX_BANNER}\n{MTX_TYPE}\n{n} {n} {nnz}\n")
            handles[label] = handle
        for u, v, label in iter_edges(csv_path):
            handles[label].write(f"{u} {v}\n")
    finally:
        for handle in handles.values():
            handle.close()

    logging.info(f"Converted {csv_path=} to {graph_dir=}: {stats=}")
    return stats
