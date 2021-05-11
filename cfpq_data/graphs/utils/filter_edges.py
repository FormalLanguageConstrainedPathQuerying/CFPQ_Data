"""Returns a graph with filtered edges.
"""
from typing import Iterable

from networkx import MultiDiGraph

__all__ = [
    "filter_edges",
]


def filter_edges(graph: MultiDiGraph, labels: Iterable[str]) -> MultiDiGraph:
    """Returns a graph
    with filtered edges.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    labels : Optional[Iterable[str]]
        Graph edge labels to be preserved.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_two_cycles_graph(42, 29)
    >>> new_g = cfpq_data.filter_edges(g, ["a"])
    >>> new_g.number_of_nodes()
    72
    >>> new_g.number_of_edges()
    43

    Returns
    -------
    g : MultiDiGraph
        Graph with filtered edges.
    """
    g = MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        g.add_node(node, **node_labels)

    for u, v, edge_labels in graph.edges(data=True):
        filtered_edge_labels = dict()
        for key, value in edge_labels.items():
            if str(value) in labels:
                filtered_edge_labels[key] = value
        if filtered_edge_labels != dict():
            g.add_edge(u, v, **filtered_edge_labels)

    return g
