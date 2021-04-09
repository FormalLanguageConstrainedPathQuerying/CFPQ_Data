"""Creator of a graph from txt file.
"""
import os
from pathlib import Path
from shlex import split as ssplit
from typing import Union

from networkx import MultiDiGraph

from cfpq_data.graphs.creators.graph_creator import GraphCreator

__all__ = ["TXTGraphCreator"]


class TXTGraphCreator(GraphCreator):
    """Creator of a graph from txt file.

    Parameters
    ----------
    source : Union[Path, str]
        If source is a str, then the graph will be loaded from a text.
        If source is a Path, then the graph will be loaded from a file.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.TXTGraphCreator("1 A 2").create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (2, 1)
    """

    def __init__(self, source: Union[Path, str]):
        """Initialize the creator of a graph from txt file.

        Parameters
        ----------
        source : Union[Path, str]
            If source is a str, then the graph will be loaded from a text.
            If source is a Path, then the graph will be loaded from a file.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.TXTGraphCreator("1 A 2").create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (2, 1)
        """
        self.source: Union[Path, str] = source

    def create(self) -> MultiDiGraph:
        """Returns a graph from txt file.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.TXTGraphCreator("1 A 2").create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (2, 1)

        Returns
        -------
        G : MultiDiGraph
        """
        edges = str(self.source).splitlines()
        if os.path.isfile(self.source):
            with open(self.source, "r") as fin:
                edges = fin.read().splitlines()

        g = MultiDiGraph()

        for edge in edges:
            u, label, v = ssplit(edge)

            g.add_edge(u, v, label=label)

        return g
