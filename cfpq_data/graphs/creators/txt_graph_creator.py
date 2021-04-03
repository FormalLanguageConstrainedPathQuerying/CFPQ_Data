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
        edges = self.source
        if os.path.isfile(self.source):
            with open(self.source, "r") as fin:
                edges = fin.read().strip()

        g = MultiDiGraph()

        for edge in edges.split("\n"):
            units = ssplit(edge)

            if len(units) == 0:
                continue

            u = units[0]
            v = units[-1]

            labels = dict()
            if len(units) > 2:
                labels = {label: label for label in units[1:-1]}

            g.add_edge(u, v, **labels)

        return g
