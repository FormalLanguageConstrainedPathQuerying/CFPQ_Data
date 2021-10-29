"""Returns a graph with filtered edges."""
import logging
from typing import Iterable, Any

import networkx as nx

__all__ = ["filter_edges"]


def filter_edges(graph: nx.MultiDiGraph, labels: Iterable[Any]) -> nx.MultiDiGraph:
    """Returns a graph with filtered edges.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    labels : Iterable[Any]
        Graph edge labels to be preserved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_two_cycles_graph(1, 1, labels=("a", "b"))
    >>> list(g.edges(data=True))
    [(1, 0, {'label': 'a'}), (0, 1, {'label': 'a'}), (0, 2, {'label': 'b'}), (2, 0, {'label': 'b'})]
    >>> new_g = filter_edges(g, ["a"])
    >>> list(new_g.edges(data=True))
    [(1, 0, {'label': 'a'}), (0, 1, {'label': 'a'})]

    Returns
    -------
    g : MultiDiGraph
        Graph with filtered edges.
    """
    new_graph = nx.MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        new_graph.add_node(node, **node_labels)

    for u, v, edge_labels in graph.edges(data=True):
        filtered_edge_labels = dict()
        for key, value in edge_labels.items():
            if value in labels:
                filtered_edge_labels[key] = value
        if filtered_edge_labels != dict():
            new_graph.add_edge(u, v, **filtered_edge_labels)

    logging.info(f"Filter labels in {graph=} with {labels=} to {new_graph=}")

    return new_graph
