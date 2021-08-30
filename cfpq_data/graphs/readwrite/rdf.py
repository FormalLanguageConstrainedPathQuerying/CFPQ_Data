"""Read (and write) a graph
from (and to) RDF file.
"""
import re
from os import path, remove
from pathlib import Path
from shutil import unpack_archive
from typing import Union

from boto3 import client
from networkx import MultiDiGraph
from rdflib import Graph as RDFGraph, BNode, URIRef, Literal, XSD
from tqdm import tqdm

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


def graph_from_dataset(graph_name: str, verbose: bool = True) -> MultiDiGraph:
    """Returns a graph from
    an RDF file loaded from
    a dataset by name.

    Parameters
    ----------
    graph_name : str
        The name of the graph from the dataset.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.graph_from_dataset("generations", verbose=False)
    >>> g.number_of_nodes()
    129
    >>> g.number_of_edges()
    273

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    for graph_class in DATASET.keys():
        if graph_name in DATASET[graph_class].keys():
            destination_dir = MAIN_FOLDER / "data" / graph_class / "Graphs"
            destination_dir.mkdir(parents=True, exist_ok=True)

            graph_file = graph_name + DATASET[graph_class][graph_name]["FileExtension"]
            graph_file_path = str(destination_dir / graph_file)

            if not path.isfile(graph_file_path):

                DATASET_VERSION = VERSION

                if re.match(r"^(\d+)\.(\d+)\.(\d+)$", DATASET_VERSION) is not None:
                    DATASET_VERSION = (
                        str(
                            re.match(r"^(\d+)\.(\d+)\.(\d+)$", DATASET_VERSION).group(1)
                        )
                        + ".0.0"
                    )

                graph_archive = (
                    graph_file + DATASET[graph_class][graph_name]["ArchiveExtension"]
                )
                graph_archive_path = str(destination_dir / graph_archive)

                s3 = client(
                    "s3",
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                )

                if verbose is True:

                    def _hook(t):
                        def _inner(bytes_amount):
                            t.update(bytes_amount)

                        return _inner

                    file_size_in_bytes = s3.head_object(
                        Bucket=BUCKET_NAME,
                        Key=f"{DATASET_VERSION}/{graph_class}/{graph_archive}",
                    )["ContentLength"]

                    with tqdm(
                        total=file_size_in_bytes,
                        unit="B",
                        unit_scale=True,
                        desc=f"Downloading '{graph_name}'...",
                    ) as t:
                        s3.download_file(
                            Bucket=BUCKET_NAME,
                            Key=f"{DATASET_VERSION}/{graph_class}/{graph_archive}",
                            Filename=graph_archive_path,
                            Callback=_hook(t),
                        )
                else:
                    s3.download_file(
                        Bucket=BUCKET_NAME,
                        Key=f"{DATASET_VERSION}/{graph_class}/{graph_archive}",
                        Filename=graph_archive_path,
                    )

                unpack_archive(graph_archive_path, destination_dir)

                remove(graph_archive_path)

            return graph_from_rdf(graph_file_path, verbose=verbose)


def graph_from_rdf(source: Union[Path, str], verbose: bool = True) -> MultiDiGraph:
    """Returns a graph from RDF file.

    Parameters
    ----------
    source : Union[Path, str]
        The path to the RDF file with which
        the graph will be created.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> generations = cfpq_data.graph_from_dataset("generations", verbose=False)
    >>> path = cfpq_data.graph_to_rdf(generations, "test.xml", verbose=False)
    >>> g = cfpq_data.graph_from_rdf(path, verbose=False)
    >>> g.number_of_nodes()
    129
    >>> g.number_of_edges()
    273

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    tmp = RDFGraph()
    tmp.parse(str(source), format="xml")

    g = MultiDiGraph()

    for subj, pred, obj in tqdm(tmp, disable=not verbose, desc="Loading..."):
        g.add_edge(subj, obj, label=pred)

    return g


def graph_to_rdf(
    graph: MultiDiGraph, path: Union[Path, str], verbose: bool = True
) -> Path:
    """Returns the path to the RDF file
    where the graph will be saved.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path : Union[Path, str]
        The path to the file where the graph will be saved.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.graph_from_dataset("generations", verbose=False)
    >>> path = cfpq_data.graph_to_rdf(g, "test.xml", verbose=False)

    Returns
    -------
    path : Path
        Path to the RDF file where the graph will be saved.
    """
    tmp = RDFGraph()

    for u, v, edge_labels in tqdm(
        graph.edges(data=True), disable=not verbose, desc="Generation..."
    ):
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
