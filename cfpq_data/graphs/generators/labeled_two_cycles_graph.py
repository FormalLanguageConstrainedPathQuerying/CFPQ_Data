"""Returns a graph with two cycles connected by one node.
With labeled edges.
"""
from typing import Union, Iterable, Any, Tuple

from networkx import MultiDiGraph, compose, path_graph

__all__ = ["labeled_two_cycles_graph"]


def labeled_two_cycles_graph(
    n: Union[int, Iterable[Any]],
    m: Union[int, Iterable[Any]],
    common: Union[int, Any] = 0,
    edge_labels: Tuple[str, str] = ("a", "b"),
) -> MultiDiGraph:
    """Returns a graph with two cycles connected by one node.
    With labeled edges.

    Parameters
    ----------
    n : Union[int, Iterable[Any]]
        The number of nodes in the first cycle without a common node.
        If n is an integer, nodes are from `range(n)`.
        If n is a container of nodes, those nodes appear in the graph.

    m : Union[int, Iterable[Any]]
        The number of nodes in the second cycle without a common node.
        If m is an integer, nodes are from `range(n)`.
        If m is a container of nodes, those nodes appear in the graph.

    common : Union[int, Any]
        The node along which two cycles are connected.

    edge_labels: Tuple[str, str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_two_cycles_graph(42, 29)
    >>> g.number_of_nodes(), g.number_of_edges()
    (72, 73)

    Returns
    -------
    g : MultiDiGraph
        A graph with two cycles connected by one node.
    """
    g1 = path_graph(n=n, create_using=MultiDiGraph)

    if isinstance(n, int):
        g1_number_of_nodes = g1.number_of_nodes()
        g1_nodes = map(lambda x: x + 1, g1.nodes)
        g1 = path_graph(n=g1_nodes, create_using=MultiDiGraph)

    g2 = path_graph(n=m, create_using=MultiDiGraph)

    if isinstance(m, int):
        g1_number_of_nodes = g1.number_of_nodes()
        g2_nodes = map(lambda x: x + g1_number_of_nodes + 1, g2.nodes)
        g2 = path_graph(n=g2_nodes, create_using=MultiDiGraph)

    for tmp in [g1, g2]:
        first_node = list(tmp.nodes)[0]
        last_node = list(tmp.nodes)[-1]
        tmp.add_edge(common, first_node)
        tmp.add_edge(last_node, common)

    for edge in g1.edges:
        g1.edges[edge]["label"] = edge_labels[0]

    for edge in g2.edges:
        g2.edges[edge]["label"] = edge_labels[1]

    g = MultiDiGraph(compose(g1, g2))

    return g
