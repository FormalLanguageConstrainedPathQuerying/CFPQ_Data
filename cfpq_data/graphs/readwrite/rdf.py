"""Read (and write) a graph
from (and to) RDF file.
"""
from pathlib import Path
from typing import Union

from networkx import MultiDiGraph
from rdflib import Graph as RDFGraph, BNode, URIRef, Literal, XSD

from cfpq_data.config import DATASET
from cfpq_data.utils import download_data
from cfpq_data.utils import unpack_graph

__all__ = [
    "graph_from_dataset",
    "graph_from_rdf",
    "graph_to_rdf",
]


def graph_from_rdf(source: Union[Path, str]) -> MultiDiGraph:
    """Returns a graph from RDF file.

    Parameters
    ----------
    source : Union[Path, str]
        The path to the RDF file with which
        the graph will be created.

    Examples
    --------
    >>> import cfpq_data
    >>> generations = cfpq_data.graph_from_dataset("generations")
    >>> path = cfpq_data.graph_to_rdf(generations, "test.xml")
    >>> g = cfpq_data.graph_from_rdf(path)
    >>> generations.number_of_nodes() == g.number_of_nodes()
    True
    >>> generations.number_of_edges() == g.number_of_edges()
    True

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    tmp = RDFGraph()
    tmp.load(str(source), format="xml")

    g = MultiDiGraph()
    for subj, pred, obj in tmp:
        g.add_edge(subj, obj, label=pred)

    return g


def graph_from_dataset(source: str) -> MultiDiGraph:
    """Returns a graph from
    an RDF file loaded from
    a dataset by name.

    Parameters
    ----------
    source : str
        The name of the graph from the dataset.

    Examples
    --------
    >>> import cfpq_data
    >>> generations = cfpq_data.graph_from_dataset("generations")
    >>> generations.number_of_nodes()
    129
    >>> generations.number_of_edges()
    273

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    for cls_name in DATASET.keys():
        if source in DATASET[cls_name].keys():
            download_data(cls_name, source, DATASET[cls_name][source])
            path_to_rdf = unpack_graph(cls_name, source)
            return graph_from_rdf(path_to_rdf)


def graph_to_rdf(graph: MultiDiGraph, path: Union[Path, str]) -> Path:
    """Returns the path to the RDF file
    where the graph will be saved.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path : Union[Path, str]
        The path to the file where the graph will be saved.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.graph_from_dataset("univ-bench")
    >>> path = cfpq_data.graph_to_rdf(g, "test.xml")

    Returns
    -------
    path : Path
        Path to the RDF file where the graph will be saved.
    """
    tmp = RDFGraph()

    for u, v, edge_labels in graph.edges(data=True):
        subj = BNode(u)
        if isinstance(u, (BNode, URIRef, Literal)):
            subj = u

        obj = BNode(v)
        if isinstance(v, (BNode, URIRef, Literal)):
            obj = v

        for label in edge_labels.values():
            pred = Literal(f"{label}", datatype=XSD.string)
            tmp.add((subj, pred, obj))

    path = Path(path).resolve()
    tmp.serialize(destination=str(path), format="xml")

    return path
