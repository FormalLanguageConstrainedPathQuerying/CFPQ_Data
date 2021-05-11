"""Returns a $G_{n,p}$ random graph,
also known as an Erdős-Rényi graph or
a binomial graph. With labeled edges.
"""
import random
from typing import Union, Iterable

import numpy as np
from networkx import MultiDiGraph, fast_gnp_random_graph
from numpy.random import RandomState

__all__ = ["fast_labeled_binomial_graph"]


def fast_labeled_binomial_graph(
    number_of_nodes: int,
    edge_probability: float,
    seed: Union[int, RandomState, None] = None,
    edge_labels: Iterable[str] = "a",
) -> MultiDiGraph:
    """Returns a $G_{n,p}$ random graph,
    also known as an Erdős-Rényi graph or
    a binomial graph. With labeled edges.

    The $G_{n,p}$ model chooses each of the possible edges with probability $p$.

    Parameters
    ----------
    number_of_nodes : int
        The number of nodes.

    edge_probability : float
        Probability for edge creation.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.

    edge_labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.fast_labeled_binomial_graph(42, 0.42, seed=42)
    >>> g.number_of_nodes(), g.number_of_edges()
    (42, 722)

    Returns
    -------
    g : MultiDiGraph
        An Erdős-Rényi graph random graph.

    Notes
    -----
    The $G_{n,p}$ graph algorithm chooses each of the $(n (n - 1)) / 2$
    (undirected) or $n (n - 1)$ (directed) possible edges with probability $p$.

    This algorithm [4]_ runs in $O(n + m)$ time, where $m$ is the expected number of
    edges, which equals $p n (n - 1) / 2$. This should be faster than
    :func:`labeled_binomial_graph` when $p$ is small and the expected number of edges
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
    g = MultiDiGraph(
        fast_gnp_random_graph(
            n=number_of_nodes, p=edge_probability, seed=seed, directed=True
        )
    )

    random.seed(seed)
    np.random.seed(seed)

    for edge in g.edges:
        g.edges[edge]["label"] = np.random.choice(list(edge_labels))

    return g
