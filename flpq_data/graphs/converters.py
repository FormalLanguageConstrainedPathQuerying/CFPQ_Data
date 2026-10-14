"""Format conversion over edge streams."""

import logging
import pathlib
from typing import Any, Callable, Dict, Optional, Union

import networkx as nx

from flpq_data.graphs.readwrite.graph import iter_edges_from_graph
from flpq_data.graphs.readwrite.mtx import (
    iter_edges_from_mtx_dir,
    mtx_dir_from_edges,
)
from flpq_data.graphs.readwrite.rdf import iter_edges_from_rdf, rdf_from_edges
from flpq_data.graphs.readwrite.txt import iter_edges_from_txt, txt_from_edges
from flpq_data.graphs.utils.to_g_text import g_text_from_edges

__all__ = ["convert_graph"]

#: The conversion formats: the reader (source) and writer (destination) of
#: each; a ``None`` side means the direction is unsupported. See the "Format
#: conversion" section of ``docs/graphs/index.rst``.
_FORMATS: Dict[str, Dict[str, Optional[Callable[..., Any]]]] = {
    "mtx": {"read": iter_edges_from_mtx_dir, "write": mtx_dir_from_edges},
    "txt": {"read": iter_edges_from_txt, "write": txt_from_edges},
    "rdf": {"read": iter_edges_from_rdf, "write": rdf_from_edges},
    "g": {"read": None, "write": g_text_from_edges},
    "graph": {"read": iter_edges_from_graph, "write": None},
}


def convert_graph(
    src: Union[pathlib.Path, str, nx.MultiDiGraph],
    dst: Union[pathlib.Path, str],
    *,
    src_format: str,
    dst_format: str,
    **writer_options: Any,
) -> pathlib.Path:
    """Converts a graph between formats over an edge stream.

    The conversion runs over a lazy ``(u, label, v)`` edge stream — one
    streaming reader and one streaming writer per format — without building
    an in-memory ``networkx.MultiDiGraph`` (the "Format conversion" section
    of ``docs/graphs/index.rst``). Formats are explicit strings; the file
    extension is not inspected (an MTX directory is ambiguous with a single
    ``results.mtx`` file).

    Parameters
    ----------
    src : Union[Path, str, MultiDiGraph]
        The source: a path for the file formats (``mtx``, ``txt``, ``rdf``)
        or an in-memory graph for ``graph``.

    dst : Union[Path, str]
        The destination path (a directory for ``mtx``, a file otherwise).

    src_format : str
        The format of ``src``: one of ``mtx``, ``txt``, ``rdf``, ``graph``.

    dst_format : str
        The format of ``dst``: one of ``mtx``, ``txt``, ``rdf``, ``g``.

    **writer_options : Any
        Forwarded to the destination writer (e.g. ``quoting=True`` for
        ``txt``, ``dimension=...`` for ``mtx``).

    Examples
    --------
    >>> import pathlib, tempfile
    >>> d = pathlib.Path(tempfile.mkdtemp()) / "graph"
    >>> _ = d.mkdir(parents=True)
    >>> _ = (d / "a.mtx").write_text(
    ...     "%%MatrixMarket matrix coordinate pattern general\\n"
    ...     "%%GraphBLAS type bool\\n3 3 2\\n0 1\\n1 2\\n"
    ... )
    >>> out = pathlib.Path(tempfile.mkdtemp()) / "g.txt"
    >>> _ = convert_graph(d, out, src_format="mtx", dst_format="txt")
    >>> out.read_text()
    '0 a 1\\n1 a 2\\n'

    Returns
    -------
    path : Path
        The resolved destination path.

    Raises
    ------
    ValueError
        If a format is unknown or the direction is unsupported (``g`` is
        write-only, ``graph`` is read-only).
    """
    if src_format not in _FORMATS:
        raise ValueError(
            f"Unknown src_format {src_format!r}; "
            f"supported formats: {', '.join(sorted(_FORMATS))}"
        )
    if dst_format not in _FORMATS:
        raise ValueError(
            f"Unknown dst_format {dst_format!r}; "
            f"supported formats: {', '.join(sorted(_FORMATS))}"
        )

    read = _FORMATS[src_format]["read"]
    write = _FORMATS[dst_format]["write"]
    if read is None:
        readable = ", ".join(
            sorted(f for f in _FORMATS if _FORMATS[f]["read"] is not None)
        )
        raise ValueError(
            f"{src_format!r} is not a readable format (readable: {readable})"
        )
    if write is None:
        writable = ", ".join(
            sorted(f for f in _FORMATS if _FORMATS[f]["write"] is not None)
        )
        raise ValueError(
            f"{dst_format!r} is not a writable format (writable: {writable})"
        )

    dest = write(read(src), dst, **writer_options)

    logging.info(f"Convert {src=} from {src_format=} to {dst_format=}")

    return dest
