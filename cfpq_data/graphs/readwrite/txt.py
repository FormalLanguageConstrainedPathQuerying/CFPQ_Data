"""Read (and write) a graph
from (and to) TXT file.
"""
from pathlib import Path
from shlex import split as ssplit
from typing import Union

from networkx import MultiDiGraph
from tqdm import tqdm

__all__ = [
    "graph_from_text",
    "graph_to_text",
    "graph_from_txt",
    "graph_to_txt",
]


def graph_from_text(source: str, verbose: bool = True) -> MultiDiGraph:
    """Returns a graph from text.

    Parameters
    ----------
    source : str
        The text with which
        the graph will be created.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.graph_from_text("1 A 2", verbose=False)
    >>> g.number_of_nodes()
    2
    >>> g.number_of_edges()
    1

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    g = MultiDiGraph()

    for edge in tqdm(source.splitlines(), disable=not verbose, desc="Loading..."):
        splitted_edge = ssplit(edge)
        if len(splitted_edge) == 1:
            g.add_node(splitted_edge[0])
        elif len(splitted_edge) == 2:
            u, v = splitted_edge
            g.add_edge(u, v)
        elif len(splitted_edge) == 3:
            u, label, v = splitted_edge
            g.add_edge(u, v, label=label)
        else:
            raise ValueError("only 1, 2, or 3 values per line are allowed")

    return g


def graph_to_text(
    graph: MultiDiGraph, quoting: bool = True, verbose: bool = True
) -> str:
    """Turns a graph into
    its text representation.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to text.

    quoting : bool
        If true, quotes will be added.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(2, edge_label="a", verbose=False)
    >>> cfpq_data.graph_to_text(g, verbose=False)
    "'0' 'a' '1'\\n'1' 'a' '0'\\n"
    >>> cfpq_data.graph_to_text(g, quoting=False, verbose=False)
    '0 a 1\\n1 a 0\\n'

    Returns
    -------
    text : str
        Graph text representation.
    """
    text = ""
    for u, v, edge_labels in tqdm(
        graph.edges(data=True), disable=not verbose, desc="Generation..."
    ):
        if len(edge_labels.values()) > 0:
            for label in edge_labels.values():
                if quoting:
                    text += f"'{u}' '{label}' '{v}'\n"
                else:
                    text += f"{u} {label} {v}\n"
        else:
            if quoting:
                text += f"'{u}' '{v}'\n"
            else:
                text += f"{u} {v}\n"
    return text


def graph_from_txt(source: Union[Path, str], verbose: bool = True) -> MultiDiGraph:
    """Returns a graph loaded from a TXT file.

    Parameters
    ----------
    source : Union[Path, str]
        The path to the TXT file with which
        the graph will be created.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g_1 = cfpq_data.graph_from_text("1 A 2", verbose=False)
    >>> path = cfpq_data.graph_to_txt(g_1, "test.txt", verbose=False)
    >>> g = cfpq_data.graph_from_txt(path, verbose=False)
    >>> g.number_of_nodes()
    2
    >>> g.number_of_edges()
    1

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    with open(source, "r") as fin:
        edges = fin.read()
    return graph_from_text(edges, verbose=verbose)


def graph_to_txt(
    graph: MultiDiGraph,
    path: Union[Path, str],
    quoting: bool = True,
    verbose: bool = True,
) -> Path:
    """Returns a path to the TXT file
    where the graph will be saved.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path: Union[Path, str]
        The path to the file where the graph will be saved.

    quoting : bool
        If true, quotes will be added.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(42, edge_label="a", verbose=False)
    >>> path = cfpq_data.graph_to_txt(g, "test.txt", quoting=False, verbose=False)

    Returns
    -------
    path : Path
        Path to a TXT file where the graph will be saved.
    """
    with open(path, "w") as fout:
        for u, v, edge_labels in tqdm(
            graph.edges(data=True), disable=not verbose, desc="Generation..."
        ):
            if len(edge_labels.values()) > 0:
                for label in edge_labels.values():
                    if quoting:
                        fout.write(f"'{u}' '{label}' '{v}'\n")
                    else:
                        fout.write(f"{u} {label} {v}\n")
            else:
                if quoting:
                    fout.write(f"'{u}' '{v}'\n")
                else:
                    fout.write(f"{u} {v}\n")
    return Path(path).resolve()
