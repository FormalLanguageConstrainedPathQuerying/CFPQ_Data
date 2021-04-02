"""Creator of a graph from CFPQ_Data dataset.
"""

from pathlib import Path
from typing import Union

import rdflib
from networkx import MultiDiGraph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

from cfpq_data.config import RELEASE_INFO
from cfpq_data.graphs.creators.graph_creator import GraphCreator
from cfpq_data.utils import download_data
from cfpq_data.utils import unpack_graph

__all__ = ["RDFGraphCreator"]


class RDFGraphCreator(GraphCreator):
    """Creator of a graph from CFPQ_Data dataset.

    Parameters
    ----------
    source : Union[Path, str]
        If source is a str, then the graph will be searched by name among the graphs in the dataset.
        If source is a Path, then the graph will be loaded from a file.

    Examples
    --------
    >>> import cfpq_data
    >>> G = cfpq_data.RDFGraphCreator("pizza").create()
    >>> G.number_of_nodes(), G.number_of_edges()
    (671, 1980)
    """

    def __init__(self, source: Union[Path, str]):
        """Initialize the creator of a graph from CFPQ_Data dataset.

        Parameters
        ----------
        source : Union[Path, str]
            If source is a str, then the graph will be searched by name among the graphs in the dataset.
            If source is a Path, then the graph will be loaded from a file.

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.RDFGraphCreator("pizza").create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (671, 1980)
        """
        self.source: Union[Path, str] = source

    def create(self) -> MultiDiGraph:
        """Returns a graph from CFPQ_Data dataset.

        Returns
        -------
        G : MultiDiGraph

        Examples
        --------
        >>> import cfpq_data
        >>> G = cfpq_data.RDFGraphCreator("pizza").create()
        >>> G.number_of_nodes(), G.number_of_edges()
        (671, 1980)
        """
        path_to_rdf = self.source

        for cls_name in ["RDF", "MemoryAliases"]:
            if (
                isinstance(self.source, str)
                and self.source in RELEASE_INFO[cls_name].keys()
            ):
                download_data("RDF", self.source, RELEASE_INFO[cls_name][self.source])
                path_to_rdf = unpack_graph("RDF", self.source)
                break

        tmp = rdflib.Graph()
        tmp.load(str(path_to_rdf), format="xml")

        g = rdflib_to_networkx_multidigraph(
            graph=tmp, edge_attrs=lambda s, p, o: {p: p}
        )

        return g
