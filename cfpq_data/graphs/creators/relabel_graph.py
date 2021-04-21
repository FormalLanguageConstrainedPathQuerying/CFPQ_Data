"""Returns a graph with relabeled edges
by specified edge labels mapping.
"""
from typing import Any, Dict

from networkx import MultiDiGraph

__all__ = ["relabel_graph"]


def relabel_graph(graph: MultiDiGraph, spec: Dict) -> MultiDiGraph:
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
    >>> rg = cfpq_data.relabel_graph(g, {"a": "b"})
    >>> g.number_of_nodes() == rg.number_of_nodes()
    True
    >>> g.number_of_edges() == rg.number_of_edges()
    True

    Returns
    -------
    g : MultiDiGraph
        A graph with relabeled edges.
    """
    g = MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        g.add_node(node, **node_labels)

    for u, v, edge_labels in graph.edges(data=True):
        relabeled_edge_labels = {
            k: v if v not in spec.keys() else spec[v] for k, v in edge_labels.items()
        }
        g.add_edge(u, v, **relabeled_edge_labels)

    return g
