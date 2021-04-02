"""Serializer of a graph to RDF file.
"""

from pathlib import Path
from typing import Union, Iterable

from networkx import MultiDiGraph
from rdflib import BNode, Literal, XSD, URIRef
from rdflib import Graph as RDFGraph

__all__ = ["RDFGraphSerializer"]

from cfpq_data.graphs.serializers.graph_serializer import GraphSerializer


class RDFGraphSerializer(GraphSerializer):
    """Serializer of the graph.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to serialize.

    path: Union[Path, str]
        The path to the file where the graph will be serialized.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.RDFGraphCreator("pizza").create()
    >>> path = cfpq_data.RDFGraphSerializer(G, "test.xml").serialize()
    """

    def __init__(
            self,
            graph: MultiDiGraph,
            path: Union[Path, str],
            *,
            labels: Iterable[str] = ("label",),
    ):
        """Initialize the serializer of the graph.

        Parameters
        ----------
        graph : MultiDiGraph
            Graph to serialize.

        path: Union[Path, str]
            The path to the file where the graph will be serialized.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.RDFGraphCreator("pizza").create()
        >>> path = cfpq_data.RDFGraphSerializer(G, "test.xml").serialize()
        """
        self.graph: MultiDiGraph = graph
        self.path: Union[Path, str] = path
        self.labels: Iterable[str] = labels

    def serialize(self) -> Path:
        """Returns the path to the file where the graph will be serialized.

        Returns
        -------
        path : Path

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.RDFGraphCreator("pizza").create()
        >>> path = cfpq_data.RDFGraphSerializer(G, "test.xml").serialize()
        """
        path = Path(self.path).resolve()

        tmp = RDFGraph()

        for edge in self.graph.edges:
            subj = BNode(edge[0])
            if isinstance(edge[0], (BNode, URIRef, Literal)):
                subj = edge[0]

            obj = BNode(edge[1])
            if isinstance(edge[1], (BNode, URIRef, Literal)):
                obj = edge[1]

            for label in self.graph.edges[edge].values():
                pred = Literal(f"{label}", datatype=XSD.string)
                tmp.add((subj, pred, obj))

        tmp.serialize(destination=str(path), format="xml")

        return path
