"""Returns a graph with nodes converted to integers."""
import logging

import networkx as nx

__all__ = ["nodes_to_integers"]


def nodes_to_integers(graph: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Returns a graph with nodes converted to integers.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = graph_from_text(["FROM LABEL TO"])
    >>> list(g.edges(data=True))
    [('FROM', 'TO', {'label': 'LABEL'})]
    >>> new_g = nodes_to_integers(g)
    >>> list(new_g.edges(data=True))
    [(0, 1, {'label': 'LABEL'})]

    Returns
    -------
    g : MultiDiGraph
        A graph whose vertices are integers.
    """
    node2int = dict()

    for node in graph.nodes():
        if node not in node2int.keys():
            node2int[node] = len(node2int)

    new_graph = nx.MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        new_graph.add_node(node2int[node], **node_labels)

    for u, v, edge_labels in graph.edges(data=True):
        new_graph.add_edge(node2int[u], node2int[v], **edge_labels)

    logging.info(f"Enumerate nodes in {graph=}  to {new_graph=}")

    return new_graph
