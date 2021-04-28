"""Returns a graph with changed edges
by specified edge labels mapping.
"""
from typing import Any, Dict

from networkx import MultiDiGraph

__all__ = ["change_edges"]


def change_edges(graph: MultiDiGraph, spec: Dict[str, Any]) -> MultiDiGraph:
    """Returns a graph with relabeled edges
    by specified edge labels mapping.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    spec: Dict
        Edge labels mapping.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(42)
    >>> new_g = cfpq_data.change_edges(g, {"a": "b"})
    >>> g.number_of_nodes() == new_g.number_of_nodes()
    True
    >>> g.number_of_edges() == new_g.number_of_edges()
    True

    Returns
    -------
    g : MultiDiGraph
        A graph with changed edges.
    """
    g = MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        g.add_node(node, **node_labels)

    for u, v, edge_labels in graph.edges(data=True):
        changed_edge_labels = dict()
        for key, value in edge_labels.items():
            if str(value) in spec.keys():
                changed_edge_labels[key] = spec[value]
            else:
                changed_edge_labels[key] = value
        g.add_edge(u, v, **changed_edge_labels)

    return g
