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

        for u, v, labels in self.graph.edges(data=True):
            subj = BNode(u)
            if isinstance(u, (BNode, URIRef, Literal)):
                subj = u

            obj = BNode(v)
            if isinstance(v, (BNode, URIRef, Literal)):
                obj = v

            for label in labels.values():
                pred = Literal(f"{label}", datatype=XSD.string)
                tmp.add((subj, pred, obj))

        tmp.serialize(destination=str(path), format="xml")

        return path
