"""Returns a random graph according to
the Barabási–Albert preferential attachment model
With labeled edges.

A graph of `number_of_nodes` nodes is grown by attaching new nodes each with
`number_of_edges` edges that are preferentially attached to existing nodes with high degree.
"""
import random
from typing import Iterable, Union

import numpy as np
from networkx import MultiDiGraph, barabasi_albert_graph
from numpy.random import RandomState

__all__ = ["labeled_barabasi_albert_graph"]


def labeled_barabasi_albert_graph(
    number_of_nodes: int,
    number_of_edges: int,
    seed: Union[int, RandomState, None] = None,
    edge_labels: Iterable[str] = "abcd",
) -> MultiDiGraph:
    """Returns a random graph according
    to the Barabási–Albert preferential attachment model
    With labeled edges.

    A graph of `number_of_nodes` nodes is grown by attaching new nodes each with
    `number_of_edges` edges that are preferentially attached to existing nodes with high degree.

    Parameters
    ----------
    number_of_nodes : int
        Number of nodes.

    number_of_edges : int
        Number of edges to attach from a new node to existing nodes.

    seed : Union[int, RandomState, None]
        Indicator of random number generation state.

    edge_labels: Iterable[str]
        Labels that will be used to mark the edges of the graph.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_barabasi_albert_graph(42, 29, 42)
    >>> g.number_of_nodes(), g.number_of_edges()
    (42, 754)

    Returns
    -------
    g : MultiDiGraph
        A random graph according
        to the Barabási–Albert preferential attachment model.

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
    g = MultiDiGraph(
        barabasi_albert_graph(n=number_of_nodes, m=number_of_edges, seed=seed)
    )

    random.seed(seed)
    np.random.seed(seed)

    for edge in g.edges:
        label = np.random.choice(list(edge_labels))
        g.edges[edge]["label"] = label

    return g
