"""Returns a path to the RDF file
where the graph will be saved.
"""
from pathlib import Path
from typing import Union, Iterable, Optional

from networkx import MultiDiGraph
from rdflib import BNode, Literal, XSD, URIRef
from rdflib import Graph as RDFGraph

__all__ = ["graph_to_rdf"]


def graph_to_rdf(
    graph: MultiDiGraph, path: Union[Path, str], labels: Optional[Iterable[str]] = None
) -> Path:
    """Returns the path to the file
    where the graph will be saved.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path : Union[Path, str]
        The path to the file where the graph will be saved.

    labels : Optional[Iterable[str]]
        Graph edge labels to be preserved.
        `None` for all edge labels.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.rdf_graph("univ-bench")
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
            if labels is None or str(label) in labels:
                pred = Literal(f"{label}", datatype=XSD.string)
                tmp.add((subj, pred, obj))

    path = Path(path).resolve()
    tmp.serialize(destination=str(path), format="xml")
    return path
