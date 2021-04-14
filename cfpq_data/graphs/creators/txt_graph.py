"""Returns a graph from txt file.
"""
import os
from pathlib import Path
from shlex import split as ssplit
from typing import Union

from networkx import MultiDiGraph

__all__ = ["txt_graph"]


def txt_graph(source: Union[Path, str]) -> MultiDiGraph:
    """Returns a graph from txt file.

    Parameters
    ----------
    source : Union[Path, str]
        If source is a str, then the graph will be loaded from a text.
        If source is a Path, then the graph will be loaded from a file.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.txt_graph("1 A 2")
    >>> g.number_of_nodes(), g.number_of_edges()
    (2, 1)

    Returns
    -------
    g : MultiDiGraph
        A graph from txt file.
    """
    edges = str(source).splitlines()
    if os.path.isfile(source):
        with open(source, "r") as fin:
            edges = fin.read().splitlines()

    g = MultiDiGraph()

    for edge in edges:
        u, label, v = ssplit(edge)
        g.add_edge(u, v, label=label)

    return g
