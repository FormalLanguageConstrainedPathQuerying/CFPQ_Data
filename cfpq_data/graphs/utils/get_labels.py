"""Returns the set of
all edge labels in the graph.
"""
from networkx import MultiDiGraph

from tqdm import tqdm

__all__ = ["get_labels"]


def get_labels(graph: MultiDiGraph, verbose: bool = True) -> set:
    """Returns the set of
    all edge labels in the graph.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_two_cycles_graph(42, 29, edge_labels=("x", "x"), verbose=False)
    >>> cfpq_data.get_labels(g, verbose=False)
    {'x'}

    Returns
    -------
    g : MultiDiGraph
        A set of all edge labels in the graph.
    """
    res = set()

    for _, _, edge_labels in tqdm(
        graph.edges(data=True), disable=not verbose, desc="Loading..."
    ):
        res |= set(edge_labels.values())

    return res
