"""Read (and write) a graph from (and to) RDF file."""
import logging
import pathlib
from typing import Union

import networkx as nx
import rdflib

__all__ = [
    "graph_from_rdf",
    "graph_to_rdf",
]


def graph_from_rdf(path: Union[pathlib.Path, str]) -> nx.MultiDiGraph:
    """Loads a graph from RDF file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the RDF file with which the graph will be created.

    Examples
    --------
    >>> from cfpq_data import *
    >>> p = download("generations")
    >>> g = graph_from_csv(path=p)
    >>> path = graph_to_rdf(g, "test.ttl")
    >>> generations = graph_from_rdf(path)
    >>> generations.number_of_nodes()
    129
    >>> generations.number_of_edges()
    273

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    tmp = rdflib.Graph()
    tmp.parse(str(path))

    graph = nx.MultiDiGraph()

    for subj, pred, obj in tmp:
        graph.add_edge(
            u_for_edge=subj,
            v_for_edge=obj,
            label=pred,
        )

    logging.info(f"Load {graph=} from {path=}")

    return graph


def graph_to_rdf(
    graph: nx.MultiDiGraph, path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Saves the `graph` to the RDF file by `path`.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path : Union[Path, str]
        The path to the file where the graph will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> p = download("generations")
    >>> g = graph_from_csv(p)
    >>> path = graph_to_rdf(g, "test.ttl")

    Returns
    -------
    path : Path
        Path to the RDF file where the graph will be saved.
    """
    tmp = rdflib.Graph()

    for u, v, edge_labels in graph.edges(data=True):
        subj = rdflib.BNode(u)
        obj = rdflib.BNode(v)

        for label in edge_labels.values():
            pred = rdflib.Literal(f"{label}", datatype=rdflib.XSD.string)
            tmp.add((subj, pred, obj))

    dest = pathlib.Path(path).resolve()
    tmp.serialize(destination=str(dest))

    logging.info(f"Save {graph=} to {dest=}")

    return dest
