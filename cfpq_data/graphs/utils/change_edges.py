"""Returns a graph with changed edges
by specified edge labels mapping.
"""
from typing import Any, Dict

from networkx import MultiDiGraph
from tqdm import tqdm

__all__ = ["change_edges"]


def change_edges(
    graph: MultiDiGraph,
    spec: Dict[str, Any],
    verbose: bool = True,
) -> MultiDiGraph:
    """Returns a graph with relabeled edges
    by specified edge labels mapping.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    spec: Dict
        Edge labels mapping.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(42, edge_label="a", verbose=False)
    >>> new_g = cfpq_data.change_edges(g, {"a": "b"}, verbose=False)
    >>> new_g.number_of_nodes()
    42
    >>> new_g.number_of_edges()
    42

    Returns
    -------
    g : MultiDiGraph
        A graph with changed edges.
    """
    g = MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        g.add_node(node, **node_labels)

    for u, v, edge_labels in tqdm(
        graph.edges(data=True), disable=not verbose, desc="Generation..."
    ):
        changed_edge_labels = dict()
        for key, value in edge_labels.items():
            if str(value) in spec.keys():
                changed_edge_labels[key] = spec[str(value)]
            else:
                changed_edge_labels[key] = value
        g.add_edge(u, v, **changed_edge_labels)

    return g
