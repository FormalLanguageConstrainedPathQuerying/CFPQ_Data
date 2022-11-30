"""Returns a graph with added reverse edges."""
import logging
from typing import Any, Dict, Union

import networkx as nx

__all__ = ["add_reverse_edges"]


def add_reverse_edges(
    graph: nx.MultiDiGraph,
    *,
    mapping: Union[Dict[Any, Any], None] = None,
) -> nx.MultiDiGraph:
    """Returns a graph with added reverse edges (with suffix '_r' by default).

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    mapping: Dict[Any, Any]
        Edge labels mapping for reverse edges that must be added.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_cycle_graph(2)
    >>> list(g.edges(data=True))
    [(0, 1, {'label': 'a'}), (1, 0, {'label': 'a'})]
    >>> new_g = add_reverse_edges(g)
    >>> list(new_g.edges(data=True))
    [(0, 1, {'label': 'a'}), (0, 1, {'label': 'a_r'}), (1, 0, {'label': 'a_r'}), (1, 0, {'label': 'a'})]

    Returns
    -------
    g : MultiDiGraph
        A graph with added reverse edges.
    """
    new_graph = nx.MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        new_graph.add_node(node, **node_labels)

    for u, v, edge_labels in graph.edges(data=True):
        new_graph.add_edge(u, v, **edge_labels)
        reverse_edge_labels = dict()
        for key, value in edge_labels.items():
            if not mapping:
                reverse_edge_labels[key] = value + "_r"
            elif value in mapping.keys():
                reverse_edge_labels[key] = mapping[value]

        if reverse_edge_labels != dict():
            new_graph.add_edge(v, u, **reverse_edge_labels)

    logging.info(f"Add reverse edges in {graph=} with {mapping=} to {new_graph=}")

    return new_graph
