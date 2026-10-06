"""Returns a graph with added reverse edges."""

import logging
from typing import Any, Dict, Union

import networkx as nx

__all__ = ["add_reverse_edges", "reverse_label"]


def reverse_label(label: str) -> str:
    """Returns the reverse of an edge label.

    Non-indexed labels get a ``_r`` suffix (``a`` -> ``a_r``).
    Indexed labels (ending in ``_i``) insert ``_r`` before the suffix
    (``load_i`` -> ``load_r_i``).

    Examples
    --------
    >>> reverse_label("a")
    'a_r'
    >>> reverse_label("alloc")
    'alloc_r'
    >>> reverse_label("load_i")
    'load_r_i'
    >>> reverse_label("f_r_i")
    'f_r_r_i'
    """
    if label.endswith("_i"):
        return label[:-2] + "_r_i"
    return label + "_r"


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
    >>> from flpq_data import *
    >>> g = labeled_cycle_graph(1)
    >>> list(g.edges(data=True))
    [(0, 0, {'label': 'a'})]
    >>> new_g = add_reverse_edges(g)
    >>> list(new_g.edges(data=True))
    [(0, 0, {'label': 'a'}), (0, 0, {'label': 'a_r'})]

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
                reverse_edge_labels[key] = reverse_label(value)
            elif value in mapping.keys():
                reverse_edge_labels[key] = mapping[value]

        if reverse_edge_labels != dict():
            new_graph.add_edge(v, u, **reverse_edge_labels)

    logging.info(f"Add reverse edges in {graph=} with {mapping=} to {new_graph=}")

    return new_graph
