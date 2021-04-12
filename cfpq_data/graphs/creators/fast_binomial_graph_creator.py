"""Creator of a `G_{n,p}` random graph, also known as an Erdős-Rényi graph or
    a binomial graph.
"""

from __future__ import annotations

from typing import Union, Iterable

import numpy as np
from networkx import MultiDiGraph, fast_gnp_random_graph
from numpy.random import RandomState

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["FastBinomialGraphCreator"]


class FastBinomialGraphCreator(GraphCreator):
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
    >>> G = cfpq_data.FastBinomialGraphCreator(42, 0.42, seed=42).create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (42, 722)

    Notes
    -----
    The $G_{n,p}$ graph algorithm chooses each of the $[n (n - 1)] / 2$
    (undirected) or $n (n - 1)$ (directed) possible edges with probability $p$.

    This algorithm [4]_ runs in $O(n + m)$ time, where `m` is the expected number of
    edges, which equals $p n (n - 1) / 2$. This should be faster than
    :func:`BinomialGraphCreator` when $p$ is small and the expected number of edges
    is small (that is, the graph is sparse).

    References
    ----------
    .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
    .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
    .. [3] https://networkx.org/documentation/stable//reference/randomness.html#randomness
    .. [4] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
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
        >>> G = cfpq_data.FastBinomialGraphCreator(42, 0.42, seed=42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 722)

        Notes
        -----
        The $G_{n,p}$ graph algorithm chooses each of the $[n (n - 1)] / 2$
        (undirected) or $n (n - 1)$ (directed) possible edges with probability $p$.

        This algorithm [4]_ runs in $O(n + m)$ time, where `m` is the expected number of
        edges, which equals $p n (n - 1) / 2$. This should be faster than
        :func:`BinomialGraphCreator` when $p$ is small and the expected number of edges
        is small (that is, the graph is sparse).

        References
        ----------
        .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
        .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
        .. [3] https://networkx.org/documentation/stable//reference/randomness.html#randomness
        .. [4] Vladimir Batagelj and Ulrik Brandes,
           "Efficient generation of large random networks",
           Phys. Rev. E, 71, 036113, 2005.
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
        >>> G = cfpq_data.FastBinomialGraphCreator(42, 0.42, seed=42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 722)

        Returns
        -------
        G : MultiDiGraph

        Notes
        -----
        The $G_{n,p}$ graph algorithm chooses each of the $[n (n - 1)] / 2$
        (undirected) or $n (n - 1)$ (directed) possible edges with probability $p$.

        This algorithm [3]_ runs in $O(n + m)$ time, where `m` is the expected number of
        edges, which equals $p n (n - 1) / 2$. This should be faster than
        :func:`BinomialGraphCreator` when $p$ is small and the expected number of edges
        is small (that is, the graph is sparse).

        References
        ----------
        .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
        .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
        .. [3] Vladimir Batagelj and Ulrik Brandes,
           "Efficient generation of large random networks",
           Phys. Rev. E, 71, 036113, 2005.
        """
        g = MultiDiGraph(
            fast_gnp_random_graph(
                n=self.number_of_nodes,
                p=self.edge_probability,
                seed=self.seed,
                directed=True,
            )
        )

        np.random.seed(self.seed)

        for edge in g.edges:
            label = np.random.choice(list(self.edge_labels))
            g.edges[edge]["label"] = label

        return g
