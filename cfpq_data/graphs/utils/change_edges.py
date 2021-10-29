"""Returns a graph with changed edges by specified edge labels mapping."""
import logging
from typing import Any, Dict

import networkx as nx

__all__ = ["change_edges"]


def change_edges(
    graph: nx.MultiDiGraph,
    mapping: Dict[Any, Any],
) -> nx.MultiDiGraph:
    """Returns a graph with relabeled edges by specified edge labels mapping.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    mapping: Dict[Any, Any]
        Edge labels mapping.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_cycle_graph(2)
    >>> list(g.edges(data=True))
    [(0, 1, {'label': 'a'}), (1, 0, {'label': 'a'})]
    >>> new_g = change_edges(g, {"a": "b"})
    >>> list(new_g.edges(data=True))
    [(0, 1, {'label': 'b'}), (1, 0, {'label': 'b'})]

    Returns
    -------
    g : MultiDiGraph
        A graph with changed edges.
    """
    new_graph = nx.MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        new_graph.add_node(node, **node_labels)

    for u, v, edge_labels in graph.edges(data=True):
        changed_edge_labels = dict()
        for key, value in edge_labels.items():
            if value in mapping.keys():
                changed_edge_labels[key] = mapping[value]
            else:
                changed_edge_labels[key] = value
        new_graph.add_edge(u, v, **changed_edge_labels)

    logging.info(f"Change labels in {graph=} with {mapping=} to {new_graph=}")

    return new_graph
