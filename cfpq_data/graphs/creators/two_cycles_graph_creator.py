"""Creator of the two cycles graph $C_{n, m}(s)$.

$C_n$ is a path with its two end-nodes connected.
$C_{n, m}(s)$ is a graph composed from $C_n$ and $C_m$ connected by node s.
"""

from typing import Union, Iterable, Any, Tuple

from networkx import MultiDiGraph, compose, path_graph

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["TwoCyclesGraphCreator"]


class TwoCyclesGraphCreator(GraphCreator):
    """Creator of the two cycles graph $C_{n, m}(s)$.

    $C_n$ is a path with its two end-nodes connected.
    $C_{n, m}(s)$ is a graph composed from $C_n$ and $C_m$ connected by node s.

    Parameters
    ----------
    number_of_nodes_in_first_cycle : Union[int, Iterable[Any]]
        If n is an integer, nodes are from `range(n)`.
        If n is a container of nodes, those nodes appear in the graph.

    number_of_nodes_in_second_cycle : Union[int, Iterable[Any]]
        If n is an integer, nodes are from `range(n)`.
        If n is a container of nodes, those nodes appear in the graph.

    common_node_of_two_cycles : Union[int, Any]
        The node along which two cycles are connected.

    edge_labels: Tuple[str, str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.TwoCyclesGraphCreator(42, 29).create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (72, 73)
    """

    def __init__(
            self,
            number_of_nodes_in_first_cycle: Union[int, Iterable[Any]],
            number_of_nodes_in_second_cycle: Union[int, Iterable[Any]],
            common_node_of_two_cycles: Union[int, Any] = 0,
            edge_labels: Tuple[str, str] = ("A", "B"),
    ):
        """Initialize the creator of the two cycles graph $C_{n, m}(s)$.

        $C_n$ is a path with its two end-nodes connected.
        $C_{n, m}(s)$ is a graph composed from $C_n$ and $C_m$ connected by node s.

        Parameters
        ----------
        number_of_nodes_in_first_cycle : Union[int, Iterable[Any]]
            If n is an integer, nodes are from `range(n)`.
            If n is a container of nodes, those nodes appear in the graph.

        number_of_nodes_in_second_cycle : Union[int, Iterable[Any]]
            If n is an integer, nodes are from `range(n)`.
            If n is a container of nodes, those nodes appear in the graph.

        common_node_of_two_cycles : Union[int, Any]
            The node along which two cycles are connected.

        edge_labels: Tuple[str, str]
            Labels that will be used to mark the edges of the graph.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.TwoCyclesGraphCreator(42, 29).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (72, 73)
        """
        self.number_of_nodes_in_first_cycle: Union[
            int, Iterable[Any]
        ] = number_of_nodes_in_first_cycle
        self.number_of_nodes_in_second_cycle: Union[
            int, Iterable[Any]
        ] = number_of_nodes_in_second_cycle
        self.common_node_of_two_cycles: Union[int, Any] = common_node_of_two_cycles
        self.edge_labels: Tuple[str, str] = edge_labels

    def create(self) -> MultiDiGraph:
        """Returns the two cycles graph $C_{n, m}(s)$.

        $C_n$ is a path with its two end-nodes connected.
        $C_{n, m}(s)$ is a graph composed from $C_n$ and $C_m$ connected by node s.

        Returns
        -------
        G : MultiDiGraph

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.TwoCyclesGraphCreator(42, 29).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (72, 73)
        """
        g1 = path_graph(
            n=self.number_of_nodes_in_first_cycle, create_using=MultiDiGraph
        )

        if isinstance(self.number_of_nodes_in_first_cycle, int):
            g1_number_of_nodes = g1.number_of_nodes()
            g1_nodes = map(lambda x: x + 1, g1.nodes)
            g1 = path_graph(n=g1_nodes, create_using=MultiDiGraph)

        g2 = path_graph(
            n=self.number_of_nodes_in_second_cycle, create_using=MultiDiGraph
        )

        if isinstance(self.number_of_nodes_in_second_cycle, int):
            g1_number_of_nodes = g1.number_of_nodes()
            g2_nodes = map(lambda x: x + g1_number_of_nodes + 1, g2.nodes)
            g2 = path_graph(n=g2_nodes, create_using=MultiDiGraph)

        for tmp in [g1, g2]:
            first_node = list(tmp.nodes)[0]
            last_node = list(tmp.nodes)[-1]
            tmp.add_edge(self.common_node_of_two_cycles, first_node)
            tmp.add_edge(last_node, self.common_node_of_two_cycles)

        for edge in g1.edges:
            g1.edges[edge]["label"] = self.edge_labels[0]

        for edge in g2.edges:
            g2.edges[edge]["label"] = self.edge_labels[1]

        g = MultiDiGraph(compose(g1, g2))

        return g
