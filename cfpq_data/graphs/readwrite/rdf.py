"""Read (and write) a graph
from (and to) RDF file.
"""
from os import path, remove
from pathlib import Path
from shutil import unpack_archive
from typing import Union

from boto3 import client
from networkx import MultiDiGraph
from rdflib import Graph as RDFGraph, BNode, URIRef, Literal, XSD

from cfpq_data import __version__ as VERSION
from cfpq_data.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    MAIN_FOLDER,
    BUCKET_NAME,
)
from cfpq_data.dataset import DATASET

__all__ = [
    "graph_from_dataset",
    "graph_from_rdf",
    "graph_to_rdf",
]


def graph_from_dataset(graph_name: str) -> MultiDiGraph:
    """Returns a graph from
    an RDF file loaded from
    a dataset by name.

    Parameters
    ----------
    graph_name : str
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
    for graph_class in DATASET.keys():
        if graph_name in DATASET[graph_class].keys():
            dst = MAIN_FOLDER / "data" / graph_class / "Graphs"
            dst.mkdir(parents=True, exist_ok=True)
            graph_file = graph_name + DATASET[graph_class][graph_name]["FileExtension"]
            graph_file_path = str(dst / graph_file)

            if not path.isfile(graph_file_path):
                graph_archive = (
                    graph_file + DATASET[graph_class][graph_name]["ArchiveExtension"]
                )
                graph_archive_path = str(dst / graph_archive)

                s3 = client(
                    "s3",
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                )
                s3.download_file(
                    Bucket=BUCKET_NAME,
                    Key=f"{VERSION}/{graph_class}/{graph_archive}",
                    Filename=graph_archive_path,
                    ExtraArgs={
                        "VersionId": DATASET[graph_class][graph_name]["VersionId"],
                    },
                )

                unpack_archive(graph_archive_path, dst)

                remove(graph_archive_path)

            return graph_from_rdf(graph_file_path)


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
    >>> g = cfpq_data.graph_from_dataset("generations")
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
