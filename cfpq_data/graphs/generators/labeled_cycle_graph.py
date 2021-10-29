"""Returns a cycle graph $C_n$ of cyclically connected nodes. With labeled edges.

$C_n$ is a path with its two end-nodes connected.
"""
import logging
from typing import Union, Iterable, Any

import networkx as nx

__all__ = ["labeled_cycle_graph"]


def labeled_cycle_graph(
    n: Union[int, Iterable[Any]],
    label: str = "a",
) -> nx.MultiDiGraph:
    """Returns a cycle graph $C_n$ of cyclically connected nodes.
    With labeled edges.

    $C_n$ is a path with its two end-nodes connected.

    Parameters
    ----------
    n : Union[int, Iterable[Any]]
        If n is an integer, nodes are from `range(n)`.
        If n is a container of nodes, those nodes appear in the graph.

    label: str
        Label that will be used to mark the edges of the graph.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_cycle_graph(42)
    >>> g.number_of_nodes()
    42
    >>> g.number_of_edges()
    42

    Returns
    -------
    g : MultiDiGraph
        A cycle graph $C_n$.
    """
    graph = nx.cycle_graph(n=n, create_using=nx.MultiDiGraph)

    for edge in graph.edges:
        graph.edges[edge]["label"] = label

    logging.info(f"Create a cycle {graph=} with {n=}, {label=}")

    return graph
