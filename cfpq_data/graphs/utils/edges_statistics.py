"""Returns statistics of graph edges."""
import logging
from collections import defaultdict
from typing import List, Any, DefaultDict

import networkx as nx

__all__ = ["get_labels_frequency", "get_sorted_labels"]


def get_labels_frequency(graph: nx.MultiDiGraph) -> DefaultDict[Any, int]:
    """Returns a dictionary with the number of edge labels used in the graph.

    Parameters
    ----------
    graph : MultiDiGraph
        Given graph.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_two_cycles_graph(1, 1, labels=("a", "b"))
    >>> list(g.edges(data=True))
    [(1, 0, {'label': 'a'}), (0, 1, {'label': 'a'}), (0, 2, {'label': 'b'}), (2, 0, {'label': 'b'})]
    >>> labels_frequency = get_labels_frequency(g)
    >>> labels_frequency
    defaultdict(<class 'int'>, {'a': 2, 'b': 2})

    Returns
    -------
    labels_frequency : DefaultDict[Any, int]
        Dictionary with edge labels usage frequency.
    """
    labels_frequency = defaultdict(int)

    for u, v, edge_labels in graph.edges(data=True):
        for key, value in edge_labels.items():
            labels_frequency[value] += 1

    logging.info(f"Construct {labels_frequency=} for {graph=}")

    return labels_frequency


def get_sorted_labels(
    graph: nx.MultiDiGraph,
    *,
    reverse: bool = False,
) -> List[Any]:
    """Returns a list of edge labels sorted by the number of uses in the graph. The labels with equal number of uses are
    sorted lexicographically.

    Parameters
    ----------
    graph : MultiDiGraph
        Given graph.

    reverse: bool
        If set to True, then the labels are sorted in reverse (ascending) order.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_two_cycles_graph(42, 29)
    >>> sorted_labels = get_sorted_labels(g)
    >>> sorted_labels
    ['a', 'b']

    Returns
    -------
    labels : List[Any]
        Sorted list of graph edge labels.
    """
    sorted_pairs = sorted(
        get_labels_frequency(graph).items(),
        key=lambda x: (-x[1], x[0]),
        reverse=reverse,
    )

    labels = []
    for label, _ in sorted_pairs:
        labels.append(label)

    logging.info(f"Sort edge {labels=} of {graph=}")

    return labels
