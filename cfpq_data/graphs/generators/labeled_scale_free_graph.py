"""Returns a scale-free directed graph. With labeled edges."""
import logging
import random
from typing import Union, Iterable, Callable

import networkx as nx

__all__ = ["labeled_scale_free_graph"]


def labeled_scale_free_graph(
    n: int,
    *,
    alpha: float = 0.41,
    beta: float = 0.54,
    gamma: float = 0.05,
    delta_in: float = 0.2,
    delta_out: float = 0,
    labels: Iterable[str] = "abcd",
    choice: Callable[[Iterable[str]], str] = random.choice,
    seed: Union[int, None] = None,
) -> nx.MultiDiGraph:
    """Returns a scale-free directed graph. With labeled edges.

    Parameters
    ----------
    n : integer
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

    labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    choice: Callable[[Iterable[str]], str]
        Function for marking edges.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_scale_free_graph(42, seed=42)
    >>> g.number_of_nodes()
    42
    >>> g.number_of_edges()
    81

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
    graph = nx.scale_free_graph(
        n=n,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        delta_in=delta_in,
        delta_out=delta_out,
        seed=seed,
        create_using=nx.MultiDiGraph,
    )

    random.seed(seed)

    for edge in graph.edges:
        graph.edges[edge]["label"] = choice(labels)

    logging.info(
        f"Create a scale-free directed {graph=} "
        f"with {n=}, {alpha=}, {beta=}, {gamma=}, {delta_in=}, {delta_out=}, "
        f"{labels=}, {choice=}, {seed=}"
    )

    return graph
