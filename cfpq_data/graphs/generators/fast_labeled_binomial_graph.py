"""Returns a $G_{n,p}$ random graph, also known as an Erdős-Rényi graph or
a binomial graph. With labeled edges."""
import logging
import random
from typing import Union, List, Callable

import networkx as nx

__all__ = ["fast_labeled_binomial_graph"]


def fast_labeled_binomial_graph(
    n: int,
    p: float,
    *,
    labels: List[str] = "a",
    choice: Callable[[List[str]], str] = random.choice,
    seed: Union[int, None] = None,
) -> nx.MultiDiGraph:
    """Returns a $G_{n,p}$ random graph, also known as an Erdős-Rényi graph or
    a binomial graph. With labeled edges.

    The $G_{n,p}$ model chooses each of the possible edges with probability $p$.

    Parameters
    ----------
    n : int
        The number of nodes.

    p : float
        Probability for edge creation.

    labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    choice: Callable[[Iterable[str]], str]
        Function for marking edges.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = fast_labeled_binomial_graph(42, 0.42, seed=42)
    >>> g.number_of_nodes()
    42
    >>> g.number_of_edges()
    722

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
    graph = nx.MultiDiGraph(
        nx.fast_gnp_random_graph(n=n, p=p, seed=seed, directed=True)
    )

    random.seed(seed)

    for edge in graph.edges:
        graph.edges[edge]["label"] = choice(labels)

    logging.info(
        f"[FAST GNP] Create a Erdős-Rényi {graph=} "
        f"with {n=}, {p=}, {labels=}, {choice=}, {seed=}"
    )

    return graph
