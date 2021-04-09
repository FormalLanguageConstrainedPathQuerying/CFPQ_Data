"""Creator of a scale-free directed graph.
"""

from __future__ import annotations

from typing import Union, Iterable

import numpy as np
from networkx import MultiDiGraph, scale_free_graph
from numpy.random import RandomState

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["ScaleFreeGraphCreator"]


class ScaleFreeGraphCreator(GraphCreator):
    """Creator of a scale-free directed graph.

    Parameters
    ----------
    number_of_nodes : integer
        Number of nodes in graph.

    alpha : float
        Probability for adding a new node connected to an existing node
        chosen randomly according to the in-degree distribution.

    beta : float
        Probability for adding an edge between two existing nodes.
        One existing node is chosen randomly according the in-degree
        distribution and the other chosen randomly according to the out-degree
        distribution.

    gamma : float
        Probability for adding a new node connected to an existing node
        chosen randomly according to the out-degree distribution.

    delta_in : float
        Bias for choosing nodes from in-degree distribution.

    delta_out : float
        Bias for choosing nodes from out-degree distribution.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See [2]_.

    edge_labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.ScaleFreeGraphCreator(42, seed=42).create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (42, 88)

    Notes
    -----
    The sum of `alpha`, `beta`, and `gamma` must be 1.

    References
    ----------
    .. [1] B. Bollobás, C. Borgs, J. Chayes, and O. Riordan,
           Directed scale-free graphs,
           Proceedings of the fourteenth annual ACM-SIAM Symposium on
           Discrete Algorithms, 132--139, 2003.
    .. [2] https://networkx.org/documentation/stable//reference/randomness.html#randomness
    """

    def __init__(
        self,
        number_of_nodes: int,
        alpha: float = 0.41,
        beta: float = 0.54,
        gamma: float = 0.05,
        delta_in: float = 0.2,
        delta_out: float = 0,
        seed: Union[int, RandomState, None] = None,
        edge_labels: Iterable[str] = "ABCD",
    ):
        """Initialize the creator of a scale-free directed graph.

        Parameters
        ----------
        number_of_nodes : integer
            Number of nodes in graph.

        alpha : float
            Probability for adding a new node connected to an existing node
            chosen randomly according to the in-degree distribution.

        beta : float
            Probability for adding an edge between two existing nodes.
            One existing node is chosen randomly according the in-degree
            distribution and the other chosen randomly according to the out-degree
            distribution.

        gamma : float
            Probability for adding a new node connected to an existing node
            chosen randomly according to the out-degree distribution.

        delta_in : float
            Bias for choosing nodes from in-degree distribution.

        delta_out : float
            Bias for choosing nodes from out-degree distribution.

        seed : integer, random_state, or None (default)
            Indicator of random number generation state.
            See [2]_.

        edge_labels: Iterable[str]
            Labels that will be used to mark the edges of the graph.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.ScaleFreeGraphCreator(42, seed=42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 88)

        Notes
        -----
        The sum of `alpha`, `beta`, and `gamma` must be 1.

        References
        ----------
        .. [1] B. Bollobás, C. Borgs, J. Chayes, and O. Riordan,
               Directed scale-free graphs,
               Proceedings of the fourteenth annual ACM-SIAM Symposium on
               Discrete Algorithms, 132--139, 2003.
        .. [2] https://networkx.org/documentation/stable//reference/randomness.html#randomness
        """
        self.number_of_nodes: int = number_of_nodes
        self.alpha: float = alpha
        self.beta: float = beta
        self.gamma: float = gamma
        self.delta_in: float = delta_in
        self.delta_out: float = delta_out
        self.seed: Union[int, RandomState, None] = seed
        self.edge_labels: Iterable[str] = edge_labels

    def create(self) -> MultiDiGraph:
        """Returns a scale-free directed graph.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.ScaleFreeGraphCreator(42, seed=42).create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (42, 88)

        Returns
        -------
        G : MultiDiGraph
        """
        g = MultiDiGraph(
            scale_free_graph(
                n=self.number_of_nodes,
                alpha=self.alpha,
                beta=self.beta,
                gamma=self.gamma,
                delta_in=self.delta_in,
                delta_out=self.delta_out,
                seed=self.seed,
            )
        )

        np.random.seed(self.seed)

        for edge in g.edges:
            label = np.random.choice(list(self.edge_labels))
            g.edges[edge]["label"] = label

        return g
