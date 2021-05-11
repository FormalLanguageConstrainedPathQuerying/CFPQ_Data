"""Returns a graph from txt file.
"""
from pathlib import Path
from shlex import split as ssplit
from typing import Union

from networkx import MultiDiGraph

__all__ = [
    "graph_from_text",
    "graph_to_text",
    "graph_from_txt",
    "graph_to_txt",
]


def graph_from_text(source: str) -> MultiDiGraph:
    """Returns a graph from text.

    Parameters
    ----------
    source : str
        The text with which
        the graph will be created.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.graph_from_text("1 A 2")
    >>> g.number_of_nodes(), g.number_of_edges()
    (2, 1)

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    g = MultiDiGraph()

    for edge in source.splitlines():
        u, label, v = ssplit(edge)
        g.add_edge(u, v, label=label)

    return g


def graph_to_text(graph: MultiDiGraph) -> str:
    """Turns a graph into
    its text representation.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to text.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(2)
    >>> cfpq_data.graph_to_text(g)
    "'0' 'a' '1'\\n'1' 'a' '0'\\n"

    Returns
    -------
    text : str
        Graph text representation.
    """
    text = ""
    for u, v, edge_labels in graph.edges(data=True):
        for label in edge_labels.values():
            text += f"'{u}' '{label}' '{v}'\n"
    return text


def graph_from_txt(source: Union[Path, str]) -> MultiDiGraph:
    """Returns a graph from txt file.

    Parameters
    ----------
    source : Union[Path, str]
        The path to the TXT file with which
        the graph will be created.

    Examples
    --------
    >>> import cfpq_data
    >>> g_1 = cfpq_data.graph_from_text("1 A 2")
    >>> path = cfpq_data.graph_to_txt(g_1, "test.txt")
    >>> g = cfpq_data.graph_from_txt(path)
    >>> g.number_of_nodes(), g.number_of_edges()
    (2, 1)

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    with open(source, "r") as fin:
        edges = fin.read()
    return graph_from_text(edges)


def graph_to_txt(graph: MultiDiGraph, path: Union[Path, str]) -> Path:
    """Returns a path to the TXT file
    where the graph will be saved.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path: Union[Path, str]
        The path to the file where the graph will be saved.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(42)
    >>> path = cfpq_data.graph_to_txt(g, "test.txt")

    Returns
    -------
    path : Path
        Path to a TXT file where the graph will be saved.
    """
    with open(path, "w") as fout:
        for u, v, edge_labels in graph.edges(data=True):
            for label in edge_labels.values():
                fout.write(f"'{u}' '{label}' '{v}'\n")
    return Path(path).resolve()
