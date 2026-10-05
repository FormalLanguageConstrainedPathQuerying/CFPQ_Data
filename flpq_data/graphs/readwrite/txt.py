"""Read (and write) a graph from (and to) TXT file."""

import logging
import pathlib
import shlex
from typing import Iterable, Iterator, Tuple, Union

import networkx as nx

__all__ = [
    "iter_edges_from_text",
    "iter_edges_from_txt",
    "txt_from_edges",
    "graph_from_text",
    "graph_to_text",
    "graph_from_txt",
    "graph_to_txt",
]


def iter_edges_from_text(text: Iterable[str]) -> Iterator[Tuple[str, str, str]]:
    """Yields the edges of a text representation as a stream.

    Each line is ``FROM LABEL TO`` — three whitespace-separated tokens;
    quoting is allowed, as in shell syntax.

    Parameters
    ----------
    text : Iterable[str]
        The lines with which the edges will be created.

    Examples
    --------
    >>> list(iter_edges_from_text(["1 A 2", "'3' 'b_5' '4'"]))
    [('1', 'A', '2'), ('3', 'b_5', '4')]

    Returns
    -------
    edges : Iterator[Tuple[str, str, str]]
        The ``(u, label, v)`` edge tuples in line order.

    Raises
    ------
    ValueError
        If a line does not match the ``FROM LABEL TO`` format.
    """
    for edge in text:
        try:
            u, label, v = shlex.split(edge.strip())
        except Exception as e:
            raise ValueError(
                f"{edge} does not match the input format: FROM LABEL TO"
            ) from e
        yield u, label, v


def iter_edges_from_txt(
    path: Union[pathlib.Path, str],
) -> Iterator[Tuple[str, str, str]]:
    """Yields the edges of a TXT file as a stream.

    The file holds one ``FROM LABEL TO`` edge per line (see
    :func:`iter_edges_from_text`).

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with which the edges will be created.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "g.txt"
    >>> _ = p.write_text("1 A 2\\n3 b_5 4\\n")
    >>> list(iter_edges_from_txt(p))
    [('1', 'A', '2'), ('3', 'b_5', '4')]

    Returns
    -------
    edges : Iterator[Tuple[str, str, str]]
        The ``(u, label, v)`` edge tuples in line order.
    """
    with open(path, "r") as f:
        yield from iter_edges_from_text(f)

    logging.info(f"Stream edges from {path=}")


def txt_from_edges(
    edges: Iterable[Tuple[str, str, str]],
    path: Union[pathlib.Path, str],
    *,
    quoting: bool = False,
) -> pathlib.Path:
    """Writes an edge stream to a TXT file.

    One ``FROM LABEL TO`` line per edge (the format of
    :func:`iter_edges_from_text`); the memory stays O(1) in the number of
    edges.

    Parameters
    ----------
    edges : Iterable[Tuple[str, str, str]]
        The ``(u, label, v)`` edge tuples to write.

    path : Union[Path, str]
        The path to the TXT file where the edges will be saved.

    quoting : bool
        If true, quotes will be added.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "g.txt"
    >>> _ = txt_from_edges([("1", "A", "2")], p)
    >>> p.read_text()
    '1 A 2\\n'

    Returns
    -------
    path : Path
        Path to the TXT file where the edges will be saved.
    """
    with open(path, "w") as f:
        for u, label, v in edges:
            if quoting:
                f.write(f"'{u}' '{label}' '{v}'\n")
            else:
                f.write(f"{u} {label} {v}\n")

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save edges to {dest=}")

    return dest


def graph_from_text(text: Iterable[str]) -> nx.MultiDiGraph:
    """Returns a graph from text.

    Parameters
    ----------
    text : Iterable[str]
        The text with which the graph will be created.

    Examples
    --------
    >>> from flpq_data import *
    >>> g = graph_from_text(["1 A 2"])
    >>> g.number_of_nodes()
    2
    >>> g.number_of_edges()
    1

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    graph = nx.MultiDiGraph()

    for edge in text:
        try:
            u, label, v = shlex.split(edge.strip())
            graph.add_edge(
                u_for_edge=u,
                v_for_edge=v,
                label=label,
            )
        except Exception as e:
            raise ValueError(
                f"{edge} does not match the input format: FROM LABEL TO"
            ) from e

    logging.info(f"Load {graph=} from {text=}")

    return graph


def graph_to_text(graph: nx.MultiDiGraph, *, quoting: bool = False) -> Iterator[str]:
    """Turns a graph into its text representation.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to text.

    quoting : bool
        If true, quotes will be added.

    Examples
    --------
    >>> from flpq_data import *
    >>> g = labeled_cycle_graph(2)
    >>> list(graph_to_text(g, quoting=True))
    ["'0' 'a' '1'", "'1' 'a' '0'"]
    >>> list(graph_to_text(g, quoting=False))
    ['0 a 1', '1 a 0']

    Returns
    -------
    text : str
        Generator of graph edges.
    """
    for u, v, edge_labels in graph.edges(data=True):
        for label in edge_labels.values():
            if quoting:
                yield f"'{u}' '{label}' '{v}'"
            else:
                yield f"{u} {label} {v}"

    logging.info(f"Turn {graph=} into text with {quoting=}")


def graph_from_txt(path: Union[pathlib.Path, str]) -> nx.MultiDiGraph:
    """Returns a graph loaded from a TXT file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with which the graph will be created.

    Examples
    --------
    >>> from flpq_data import *
    >>> g_1 = graph_from_text(["1 A 2"])
    >>> p = graph_to_txt(g_1, "test.txt")
    >>> g = graph_from_txt(p)
    >>> g.number_of_nodes()
    2
    >>> g.number_of_edges()
    1

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    with open(path, "r") as f:
        graph = graph_from_text(f)

    logging.info(f"Load {graph=} from {path=}")

    return graph


def graph_to_txt(
    graph: nx.MultiDiGraph,
    path: Union[pathlib.Path, str],
    *,
    quoting: bool = False,
) -> pathlib.Path:
    """Returns a path to the TXT file where the graph will be saved.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path: Union[Path, str]
        The path to the file where the graph will be saved.

    quoting : bool
        If true, quotes will be added.

    Examples
    --------
    >>> from flpq_data import *
    >>> g = labeled_cycle_graph(42, label="a")
    >>> path = graph_to_txt(g, "test.txt", quoting=False)

    Returns
    -------
    path : Path
        Path to a TXT file where the graph will be saved.
    """
    with open(path, "w") as f:
        for edge in graph_to_text(graph=graph, quoting=quoting):
            f.write(edge + "\n")

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {graph=} to {dest=}")

    return dest
