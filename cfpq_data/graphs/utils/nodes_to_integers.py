"""Returns a graph with
nodes converted to integers.
"""
from networkx import MultiDiGraph

from tqdm import tqdm

__all__ = ["nodes_to_integers"]


def nodes_to_integers(graph: MultiDiGraph, verbose: bool = True) -> MultiDiGraph:
    """Returns a graph with
    nodes converted to integers.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.graph_from_text("29 A 42", verbose=False)
    >>> new_g = cfpq_data.nodes_to_integers(g, verbose=False)
    >>> g.edges(data=True)
    OutMultiEdgeDataView([('29', '42', {'label': 'A'})])
    >>> new_g.edges(data=True)
    OutMultiEdgeDataView([(0, 1, {'label': 'A'})])

    Returns
    -------
    g : MultiDiGraph
        A graph whose vertices are integers.
    """
    node2int = dict()

    for node in graph.nodes():
        if node not in node2int.keys():
            node2int[node] = len(node2int)

    g = MultiDiGraph()

    for node, node_labels in graph.nodes(data=True):
        g.add_node(node2int[node], **node_labels)

    for u, v, edge_labels in tqdm(
        graph.edges(data=True), disable=not verbose, desc="Generation..."
    ):
        g.add_edge(node2int[u], node2int[v], **edge_labels)

    return g
