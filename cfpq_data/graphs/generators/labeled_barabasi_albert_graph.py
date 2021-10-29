"""Returns a random graph according to the Barabási–Albert preferential attachment model
With labeled edges.

A graph of `n` nodes is grown by attaching new nodes each with
`m` edges that are preferentially attached to existing nodes with high degree.
"""
import logging
import random
from typing import List, Union, Callable

import networkx as nx

__all__ = ["labeled_barabasi_albert_graph"]


def labeled_barabasi_albert_graph(
    n: int,
    m: int,
    *,
    labels: List[str] = "abcd",
    choice: Callable[[List[str]], str] = random.choice,
    seed: Union[int, None] = None,
) -> nx.MultiDiGraph:
    """Returns a random graph according to the Barabási–Albert preferential attachment model.
    With labeled edges.

    A graph of `n` nodes is grown by attaching new nodes each with
    `m` edges that are preferentially attached to existing nodes with high degree.

    Parameters
    ----------
    n : int
        Number of nodes.

    m : int
        Number of edges to attach from a new node to existing nodes.

    labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    choice: Callable[[Iterable[str]], str]
        Function for marking edges.

    seed : Union[int, RandomState, None]
        Indicator of random number generation state.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = labeled_barabasi_albert_graph(42, 29, seed=42)
    >>> g.number_of_nodes()
    42
    >>> g.number_of_edges()
    754

    Returns
    -------
    g : MultiDiGraph
        A random graph according to the Barabási–Albert preferential attachment model.

    Raises
    ------
    NetworkXError
        If `m` does not satisfy ``1 <= m < n``.

    References
    ----------
    .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
       random networks", Science 286, pp 509-512, 1999.
    .. [2] https://networkx.org/documentation/stable//reference/randomness.html#randomness
    """
    graph = nx.MultiDiGraph(nx.barabasi_albert_graph(n=n, m=m, seed=seed))

    random.seed(seed)

    for edge in graph.edges:
        graph.edges[edge]["label"] = choice(labels)

    logging.info(
        f"Create a random {graph=} "
        f"according to the Barabási–Albert preferential attachment model "
        f"with {n=}, {m=}, {labels=}, {choice=}, {seed=}"
    )

    return graph
