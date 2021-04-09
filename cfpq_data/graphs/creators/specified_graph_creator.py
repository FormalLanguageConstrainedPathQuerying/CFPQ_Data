"""Creator of the graph with specified edge labels mapping.
"""
from typing import Any, Dict

from networkx import MultiDiGraph

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["SpecifiedGraphCreator"]


class SpecifiedGraphCreator(GraphCreator):
    """Creator of the graph with specified edge labels mapping.

    Parameters
    ----------
    graph : MultiDiGraph

    spec: Dict
        Edge labels mapping.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.CycleGraphCreator(42).create()
    >>> sum([1 for u, v, labels in G.edges(data=True) if labels["label"] == "A"])
    42
    >>> H = cfpq_data.SpecifiedGraphCreator(G, {"A": "B"}).create()
    >>> sum([1 for u, v, labels in H.edges(data=True) if labels["label"] == "B"])
    42
    """

    def __init__(
            self,
            graph: MultiDiGraph,
            spec: Dict[Any, Any],
    ):
        """Initialize the creator of the graph with specified edge labels mapping.

        Parameters
        ----------
        graph : MultiDiGraph

        spec: Dict
            Edge labels mapping.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.CycleGraphCreator(42).create()
        >>> sum([1 for u, v, labels in G.edges(data=True) if labels["label"] == "A"])
        42
        >>> H = cfpq_data.SpecifiedGraphCreator(G, {"A": "B"}).create()
        >>> sum([1 for u, v, labels in H.edges(data=True) if labels["label"] == "B"])
        42
        """
        self.graph: MultiDiGraph = graph
        self.spec: Dict[Any, Any] = spec

    def create(self) -> MultiDiGraph:
        """Returns the graph with mapped edge labels.

        Returns
        -------
        G : MultiDiGraph

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.CycleGraphCreator(42).create()
        >>> sum([1 for u, v, labels in G.edges(data=True) if labels["label"] == "A"])
        42
        >>> H = cfpq_data.SpecifiedGraphCreator(G, {"A": "B"}).create()
        >>> sum([1 for u, v, labels in H.edges(data=True) if labels["label"] == "B"])
        42
        """
        g = MultiDiGraph()

        for node, node_labels in self.graph.nodes(data=True):
            g.add_node(node, **node_labels)

        for u, v, edge_labels in self.graph.edges(data=True):
            mapped_edge_labels = {
                k: v if v not in self.spec.keys() else self.spec[v]
                for k, v in edge_labels.items()
            }
            g.add_edge(u, v, **mapped_edge_labels)

        return g
