"""Serializer of a graph to TXT file.
"""

from pathlib import Path
from typing import Union

from networkx import MultiDiGraph

__all__ = ["TXTGraphSerializer"]

from cfpq_data.graphs.serializers.graph_serializer import GraphSerializer


class TXTGraphSerializer(GraphSerializer):
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
    >>> G = cfpq_data.CycleGraphCreator(42).create()
    >>> path = cfpq_data.TXTGraphSerializer(G, "test.txt").serialize()
    """

    def __init__(self, graph: MultiDiGraph, path: Union[Path, str]):
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
        >>> G = cfpq_data.CycleGraphCreator(42).create()
        >>> path = cfpq_data.TXTGraphSerializer(G, "test.txt").serialize()
        """
        self.graph: MultiDiGraph = graph
        self.path: Union[Path, str] = path

    def serialize(self) -> Path:
        """Returns the path to the file where the graph will be serialized.

        Returns
        -------
        path : Path

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.CycleGraphCreator(42).create()
        >>> path = cfpq_data.TXTGraphSerializer(G, "test.txt").serialize()
        """
        path = Path(self.path).resolve()
        with open(path, "w") as fout:
            for edge in self.graph.edges:
                fout.write(f"{edge[0]} {self.graph.edges[edge]['label']} {edge[1]}\n")
        return path
