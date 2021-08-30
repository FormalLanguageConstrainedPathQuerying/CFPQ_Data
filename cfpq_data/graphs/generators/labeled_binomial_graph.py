"""Returns a $G_{n,p}$ random graph,
also known as an Erdős-Rényi graph or
a binomial graph. With labeled edges.
"""
import random
from typing import Union, Iterable

from networkx import MultiDiGraph, gnp_random_graph
from tqdm import tqdm

__all__ = ["labeled_binomial_graph"]


def labeled_binomial_graph(
    number_of_nodes: int,
    edge_probability: float,
    seed: Union[int, None] = None,
    edge_labels: Iterable[str] = "a",
    verbose: bool = True,
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

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_binomial_graph(42, 0.84, seed=42, verbose=False)
    >>> g.number_of_nodes()
    42
    >>> g.number_of_edges()
    1453

    Returns
    -------
    g : MultiDiGraph
        An Erdős-Rényi graph random graph.

    Notes
    -----
    This algorithm runs in $O(n^2)$ time.  For sparse graphs (that is, for
    small values of $p$), :func:`fast_labeled_binomial_graph` is faster.

    References
    ----------
    .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
    .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
    .. [3] https://networkx.org/documentation/stable//reference/randomness.html#randomness
    """
    g = MultiDiGraph(
        gnp_random_graph(
            n=number_of_nodes, p=edge_probability, seed=seed, directed=True
        )
    )

    random.seed(seed)

    for edge in tqdm(g.edges, disable=not verbose, desc="Generation..."):
        g.edges[edge]["label"] = random.choice(list(edge_labels))

    return g
