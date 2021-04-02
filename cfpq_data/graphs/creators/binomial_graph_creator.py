"""Creator of a `G_{n,p}` random graph, also known as an Erdős-Rényi graph or
    a binomial graph.
"""

from __future__ import annotations

from typing import Union, Iterable

import numpy as np
from networkx import MultiDiGraph, gnp_random_graph
from numpy.random import RandomState

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["BinomialGraphCreator"]


class BinomialGraphCreator(GraphCreator):
    """Creator of a `G_{n,p}` random graph, also known as an Erdős-Rényi graph or
    a binomial graph.

    The `G_{n,p}` model chooses each of the possible edges with probability
    ``p``.

    Parameters
    ----------
    number_of_nodes : int
        The number of nodes.

    edge_probability : float
        Probability for edge creation.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See [3]_.

    edge_labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.BinomialGraphCreator(42, 0.84, seed=42).create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (42, 1453)

    Notes
    -----
    This algorithm runs in `O(n^2)` time.  For sparse graphs (that is, for
    small values of `p`), :func:`FastBinomialGraphCreator` is faster.

    References
    ----------
    .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
    .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
    .. [3] https://networkx.org/documentation/stable//reference/randomness.html#randomness
    """

    def __init__(
            self,
            number_of_nodes: int,
            edge_probability: float,
            seed: Union[int, RandomState, None] = None,
            edge_labels: Iterable[str] = "ABCD",
    ):
        """Initialize the creator of a `G_{n,p}` random graph, also known as an Erdős-Rényi graph or
        a binomial graph.

        The `G_{n,p}` model chooses each of the possible edges with probability
        ``p``.

        Parameters
        ----------
        number_of_nodes : int
            The number of nodes.

        edge_probability : float
            Probability for edge creation.

        seed : integer, random_state, or None (default)
            Indicator of random number generation state.
            See [3]_.

        edge_labels: Iterable[str]
            Labels that will be used to mark the edges of the graph.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.BinomialGraphCreator(42, 0.84, seed=42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 1453)

        Notes
        -----
        This algorithm runs in `O(n^2)` time.  For sparse graphs (that is, for
        small values of `p`), :func:`FastBinomialGraphCreator` is faster.

        References
        ----------
        .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
        .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
        .. [3] https://networkx.org/documentation/stable//reference/randomness.html#randomness
        """
        self.number_of_nodes: int = number_of_nodes
        self.edge_probability: float = edge_probability
        self.seed: Union[int, RandomState, None] = seed
        self.edge_labels: Iterable[str] = edge_labels

    def create(self) -> MultiDiGraph:
        """Returns a `G_{n,p}` random graph, also known as an Erdős-Rényi graph or
        a binomial graph.

        The `G_{n,p}` model chooses each of the possible edges with probability
        ``p``.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.BinomialGraphCreator(42, 0.84, seed=42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 1453)

        Notes
        -----
        This algorithm runs in `O(n^2)` time.  For sparse graphs (that is, for
        small values of `p`), :func:`FastBinomialGraphCreator` is a faster algorithm.

        References
        ----------
        .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
        .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
        """
        g = MultiDiGraph(
            gnp_random_graph(
                n=self.number_of_nodes,
                p=self.edge_probability,
                seed=self.seed,
                directed=True,
            )
        )

        np.random.seed(self.seed)

        for edge in g.edges:
            g.edges[edge]["label"] = np.random.choice(list(self.edge_labels))

        return g
