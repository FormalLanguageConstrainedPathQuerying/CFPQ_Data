"""The edge stream of an in-memory graph."""

import logging
from typing import Any, Iterator, Tuple

import networkx as nx

__all__ = ["iter_edges_from_graph"]


def iter_edges_from_graph(
    graph: nx.MultiDiGraph,
) -> Iterator[Tuple[Any, str, Any]]:
    """Yields the edges of an in-memory graph as a stream.

    Each edge key yields ``(u, label, v)`` with the label taken from the
    edge's ``label`` attribute — the one every ``graph_from_*`` reader sets
    and every ``graph_to_*`` writer consumes.

    Parameters
    ----------
    graph : MultiDiGraph
        The graph whose edges will be yielded.

    Examples
    --------
    >>> import networkx as nx
    >>> g = nx.MultiDiGraph()
    >>> _ = g.add_edges_from([(0, 1, {"label": "a"}), (1, 2, {"label": "b_5"})])
    >>> list(iter_edges_from_graph(g))
    [(0, 'a', 1), (1, 'b_5', 2)]

    Returns
    -------
    edges : Iterator[Tuple[Any, str, Any]]
        The ``(u, label, v)`` edge tuples in graph order.
    """
    for u, v, data in graph.edges(data=True):
        yield u, data["label"], v

    logging.info(f"Stream edges from {graph=}")
