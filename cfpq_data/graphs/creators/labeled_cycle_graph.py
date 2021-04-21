"""Returns a cycle graph $C_n$
of cyclically connected nodes.
With labeled edges.

$C_n$ is a path with its two end-nodes connected.
"""
from typing import Union, Iterable, Any

from networkx import MultiDiGraph, cycle_graph

__all__ = ["labeled_cycle_graph"]


def labeled_cycle_graph(
    number_of_nodes: Union[int, Iterable[Any]], edge_label: str = "a"
) -> MultiDiGraph:
    """Returns a cycle graph $C_n$
    of cyclically connected nodes.
    With labeled edges.

    $C_n$ is a path with its two end-nodes connected.

    Parameters
    ----------
    number_of_nodes : Union[int, Iterable[Any]]
        If n is an integer, nodes are from `range(n)`.
        If n is a container of nodes, those nodes appear in the graph.

    edge_label: str
        Label that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(42)
    >>> g.number_of_nodes(), g.number_of_edges()
    (42, 42)

    Returns
    -------
    g : MultiDiGraph
        A cycle graph $C_n$.
    """
    g = cycle_graph(n=number_of_nodes, create_using=MultiDiGraph)

    for edge in g.edges:
        g.edges[edge]["label"] = edge_label

    return g
