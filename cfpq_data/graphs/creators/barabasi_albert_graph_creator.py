"""Сreator of a random graph according to the Barabási–Albert preferential attachment model.

A graph of $number_of_nodes$ nodes is grown by attaching new nodes each with
$number_of_edges$ edges that are preferentially attached to existing nodes with high degree.
"""

from typing import Iterable, Union

import numpy as np
from networkx import MultiDiGraph, barabasi_albert_graph
from numpy.random import RandomState

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["BarabasiAlbertGraphCreator"]


class BarabasiAlbertGraphCreator(GraphCreator):
    """Сreator of a random graph according to the Barabási–Albert preferential attachment model.

    A graph of $number_of_nodes$ nodes is grown by attaching new nodes each with
    $number_of_edges$ edges that are preferentially attached to existing nodes with high degree.

    Parameters
    ----------
    number_of_nodes : int
        Number of nodes
    number_of_edges : int
        Number of edges to attach from a new node to existing nodes
    seed : Union[int, RandomState, None]
        Indicator of random number generation state.
        See [2]_.
    edge_labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.BarabasiAlbertGraphCreator(42, 29, 42).create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (42, 377)

    References
    ----------
    .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
       random networks", Science 286, pp 509-512, 1999.
    .. [2] https://networkx.org/documentation/stable//reference/randomness.html#randomness
    """

    def __init__(
        self,
        number_of_nodes: int,
        number_of_edges: int,
        seed: Union[int, RandomState, None] = None,
        edge_labels: Iterable[str] = "ABCD",
    ):
        """Initialize the creator of a random graph according
        to the Barabási–Albert preferential attachment model.

        A graph of $number_of_nodes$ nodes is grown by attaching new nodes each with
        $number_of_edges$ edges that are preferentially attached to existing nodes with high degree.

        Parameters
        ----------
        number_of_nodes : int
            Number of nodes
        number_of_edges : int
            Number of edges to attach from a new node to existing nodes
        seed : Union[int, RandomState, None]
            Indicator of random number generation state.
            See [2]_.
        edge_labels: Iterable[str]
            Labels that will be used to mark the edges of the graph.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.BarabasiAlbertGraphCreator(42, 29, seed=42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 377)

        References
        ----------
        .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
           random networks", Science 286, pp 509-512, 1999.
        .. [2] https://networkx.org/documentation/stable//reference/randomness.html#randomness
        """
        self.number_of_nodes: int = number_of_nodes
        self.number_of_edges: int = number_of_edges
        self.seed: Union[int, RandomState, None] = seed
        self.edge_labels: Iterable[str] = edge_labels

    def create(self) -> MultiDiGraph:
        """Returns a random graph according to the Barabási–Albert preferential

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.BarabasiAlbertGraphCreator(42, 29, 42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 377)

        Returns
        -------
        G : MultiDiGraph

        Raises
        ------
        NetworkXError
            If `m` does not satisfy ``1 <= m < n``.
        """
        g = barabasi_albert_graph(
            n=self.number_of_nodes, m=self.number_of_edges, seed=self.seed
        )

        np.random.seed(self.seed)

        for edge in g.edges:
            g.edges[edge]["label"] = np.random.choice(list(self.edge_labels))

        return g
