"""Returns a scale-free directed graph.
With labeled edges.
"""
import random
from typing import Union, Iterable

import numpy as np
from networkx import MultiDiGraph, scale_free_graph
from numpy.random import RandomState

__all__ = ["labeled_scale_free_graph"]


def labeled_scale_free_graph(
    number_of_nodes: int,
    alpha: float = 0.41,
    beta: float = 0.54,
    gamma: float = 0.05,
    delta_in: float = 0.2,
    delta_out: float = 0,
    seed: Union[int, RandomState, None] = None,
    edge_labels: Iterable[str] = "abcd",
) -> MultiDiGraph:
    """Returns a scale-free directed graph.
    With labeled edges.

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

    edge_labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_scale_free_graph(42, seed=42)
    >>> g.number_of_nodes(), g.number_of_edges()
    (42, 88)

    Returns
    -------
    g : MultiDiGraph
        A scale-free directed graph.

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
    g = scale_free_graph(
        n=number_of_nodes,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        delta_in=delta_in,
        delta_out=delta_out,
        seed=seed,
        create_using=MultiDiGraph,
    )

    random.seed(seed)
    np.random.seed(seed)

    for edge in g.edges:
        label = np.random.choice(list(edge_labels))
        g.edges[edge]["label"] = label

    return g
