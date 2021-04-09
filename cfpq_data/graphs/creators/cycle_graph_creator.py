"""Creator of the cycle graph $C_n$ of cyclically connected nodes.

$C_n$ is a path with its two end-nodes connected.
"""

from typing import Union, Iterable, Any

from networkx import MultiDiGraph, cycle_graph

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["CycleGraphCreator"]


class CycleGraphCreator(GraphCreator):
    """Creator of the cycle graph $C_n$ of cyclically connected nodes.

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
    >>> G = cfpq_data.CycleGraphCreator(42).create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (42, 42)
    """

    def __init__(
            self,
            number_of_nodes: Union[int, Iterable[Any]],
            edge_label: str = "A",
    ):
        """Initialize the creator of the cycle graph $C_n$ of cyclically connected nodes.

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
        >>> G = cfpq_data.CycleGraphCreator(42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 42)
        """
        self.number_of_nodes: Union[int, Iterable[Any]] = number_of_nodes
        self.edge_label: str = edge_label

    def create(self) -> MultiDiGraph:
        """Returns the cycle graph $C_n$ of cyclically connected nodes.

        $C_n$ is a path with its two end-nodes connected.

        Returns
        -------
        G : MultiDiGraph

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.CycleGraphCreator(42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 42)
        """
        g = cycle_graph(n=self.number_of_nodes, create_using=MultiDiGraph)

        for edge in g.edges:
            g.edges[edge]["label"] = self.edge_label

        return g
