"""Returns a graph from CFPQ_Data dataset or RDF file.
"""
import os
from pathlib import Path
from typing import Union

from networkx import MultiDiGraph
from rdflib import Graph as RDFGraph

from cfpq_data.config import DATASET
from cfpq_data.utils import download_data
from cfpq_data.utils import unpack_graph

__all__ = ["rdf_graph"]


def rdf_graph(source: Union[Path, str]) -> MultiDiGraph:
    """Returns a graph from CFPQ_Data dataset.

    Parameters
    ----------
    source : Union[Path, str]
        If source is a str, then the graph will be searched by name among the graphs in the dataset.
        If source is a Path, then the graph will be loaded from a file.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.rdf_graph("generations")
    >>> g.number_of_nodes(), g.number_of_edges()
    (129, 273)

    Returns
    -------
    g : MultiDiGraph
        A graph from CFPQ_Data dataset or RDF file.
    """
    path_to_rdf = source

    for cls_name in ["RDF", "MemoryAliases"]:
        if not os.path.isfile(source) and source in DATASET[cls_name].keys():
            download_data("RDF", source, DATASET[cls_name][source])
            path_to_rdf = unpack_graph("RDF", source)
            break

    tmp = RDFGraph()
    tmp.load(str(path_to_rdf), format="xml")

    g = MultiDiGraph()

    for subj, pred, obj in tmp:
        g.add_edge(subj, obj, label=pred)

    return g
