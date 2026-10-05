"""Generate FastMatrixCFPQ .g graph files from edge streams."""

import logging
import pathlib
import re
from typing import Any, Iterable, Iterator, Tuple, Union

from flpq_data.graphs.readwrite.mtx import iter_edges_from_mtx_dir

__all__ = ["graph_dir_to_g_text", "g_text_from_edges"]

_INDEXED_RE = re.compile(r"^(.+)_(\d+)$")


def _reverse_label(label: str) -> str:
    if label.endswith("_i"):
        return label[:-2] + "_r_i"
    return label + "_r"


def _g_lines(edges: Iterable[Tuple[Any, str, Any]]) -> Iterator[str]:
    """Yields the FastMatrixCFPQ .g lines of an edge stream.

    Each ``(u, label, v)`` edge yields a forward line and an auto-generated
    reverse line (the :func:`reverse_label` convention); an indexed label
    ``X_N`` collapses to ``X_i`` with the index as a fourth column.

    Parameters
    ----------
    edges : Iterable[Tuple[Any, str, Any]]
        The ``(u, label, v)`` edge tuples to turn into .g lines.

    Returns
    -------
    lines : Iterator[str]
        The .g lines, two per edge (forward then reverse).
    """
    for u, label, v in edges:
        m = _INDEXED_RE.match(label)
        if m:
            out_label, idx = f"{m.group(1)}_i", m.group(2)
        else:
            out_label, idx = label, None

        rev = _reverse_label(out_label)
        if idx is not None:
            yield f"{u} {v} {out_label} {idx}"
            yield f"{v} {u} {rev} {idx}"
        else:
            yield f"{u} {v} {out_label}"
            yield f"{v} {u} {rev}"


def g_text_from_edges(
    edges: Iterable[Tuple[Any, str, Any]], path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Writes an edge stream to a FastMatrixCFPQ .g file.

    The file holds the ``u v label`` lines with auto-generated reverse edges
    (see :func:`graph_dir_to_g_text` for the format); the memory stays O(1)
    in the number of edges.

    Parameters
    ----------
    edges : Iterable[Tuple[Any, str, Any]]
        The ``(u, label, v)`` edge tuples to write.

    path : Union[Path, str]
        The path to the .g file where the edges will be saved.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "g.g"
    >>> _ = g_text_from_edges([(0, "a", 1)], p)
    >>> p.read_text()
    '0 1 a\\n1 0 a_r\\n'

    Returns
    -------
    path : Path
        Path to the .g file where the edges will be saved.
    """
    dest = pathlib.Path(path)
    with open(dest, "w") as f:
        for line in _g_lines(edges):
            f.write(line + "\n")

    dest = dest.resolve()

    logging.info(f"Save edges to {dest=}")

    return dest


def graph_dir_to_g_text(
    path: Union[pathlib.Path, str],
) -> str:
    """Generates a FastMatrixCFPQ .g file text from a directory of mtx files.

    Each ``*.mtx`` file contributes forward edges; reverse edges are
    auto-generated with the :func:`reverse_label` convention. Indexed files
    (``X_N.mtx``) produce 4-column lines with label ``X_i`` and index ``N``.

    Parameters
    ----------
    path : Union[Path, str]
        Directory containing MatrixMarket files.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> d = pathlib.Path(tempfile.mkdtemp())
    >>> _ = (d / "a.mtx").write_text(
    ...     "%%MatrixMarket matrix coordinate pattern general\\n"
    ...     "%%GraphBLAS type bool\\n3 3 1\\n0 1\\n"
    ... )
    >>> _ = (d / "b_5.mtx").write_text(
    ...     "%%MatrixMarket matrix coordinate pattern general\\n"
    ...     "%%GraphBLAS type bool\\n3 3 1\\n2 0\\n"
    ... )
    >>> text = graph_dir_to_g_text(d)
    >>> lines = text.strip().splitlines()
    >>> len(lines)
    4
    >>> "0 1 a" in lines
    True
    >>> "1 0 a_r" in lines
    True
    >>> "2 0 b_i 5" in lines
    True
    >>> "0 2 b_r_i 5" in lines
    True

    Returns
    -------
    text : str
        The .g file content.
    """
    lines = list(_g_lines(iter_edges_from_mtx_dir(path)))
    text = "\n".join(lines) + "\n" if lines else ""

    logging.info(f"Generate .g text from {path=}: {len(lines)} edges")

    return text
