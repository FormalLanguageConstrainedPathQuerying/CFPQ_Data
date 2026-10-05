"""Read (and write) a graph from (and to) RDF file."""

import logging
import pathlib
from typing import Iterator, Tuple, Union

import networkx as nx
import rdflib
from rdflib.term import Node as RdfNode

__all__ = [
    "iter_edges_from_rdf",
    "graph_from_rdf",
    "graph_to_rdf",
]

#: The IRI prefixes of the RDF encoding (the "RDF encoding" section of
#: ``docs/graphs/index.rst``).
_NODE_IRI_PREFIX = "urn:flpq:node:"
_LABEL_IRI_PREFIX = "urn:flpq:label:"


def _node_id(term: RdfNode) -> str:
    """Returns the node id behind an RDF endpoint term.

    The current encoding uses IRIs ``urn:flpq:node:<id>``; the legacy form
    used blank nodes, which the Turtle serializer writes as anonymous — their
    ids are opaque, so the full term string is returned.

    Parameters
    ----------
    term : Node
        An RDF endpoint (subject or object) term.

    Returns
    -------
    node_id : str
        The node id of the term.

    Raises
    ------
    ValueError
        If the term is neither a blank node nor a ``urn:flpq:node:`` IRI.
    """
    if isinstance(term, rdflib.BNode):
        return str(term)
    text = str(term)
    if not text.startswith(_NODE_IRI_PREFIX):
        raise ValueError(f"Unrecognized node term {term!r}")
    return text[len(_NODE_IRI_PREFIX) :]


def _label(term: RdfNode) -> str:
    """Returns the edge label behind an RDF predicate term.

    The current encoding uses IRIs ``urn:flpq:label:<label>``; the legacy
    form used Literals.

    Parameters
    ----------
    term : Node
        An RDF predicate term.

    Returns
    -------
    label : str
        The edge label of the term.

    Raises
    ------
    ValueError
        If the term is neither a Literal nor a ``urn:flpq:label:`` IRI.
    """
    if isinstance(term, rdflib.Literal):
        return str(term)
    text = str(term)
    if not text.startswith(_LABEL_IRI_PREFIX):
        raise ValueError(f"Unrecognized predicate term {term!r}")
    return text[len(_LABEL_IRI_PREFIX) :]


def iter_edges_from_rdf(
    path: Union[pathlib.Path, str],
) -> Iterator[Tuple[str, str, str]]:
    """Yields the edges of an RDF file as a stream.

    Reads both the current encoding (IRI nodes ``urn:flpq:node:<id>`` and IRI
    predicates ``urn:flpq:label:<label>``) and the legacy form written by
    older versions (blank-node endpoints and Literal predicates). rdflib has
    no streaming parser, so the file is materialized in memory.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the RDF file with which the edges will be created.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> d = pathlib.Path(tempfile.mkdtemp())
    >>> p = d / "g.ttl"
    >>> _ = p.write_text(
    ...     "<urn:flpq:node:0> <urn:flpq:label:a> <urn:flpq:node:1> .\\n"
    ...     "<urn:flpq:node:1> <urn:flpq:label:b_5> <urn:flpq:node:2> .\\n"
    ... )
    >>> sorted(iter_edges_from_rdf(p))
    [('0', 'a', '1'), ('1', 'b_5', '2')]

    Returns
    -------
    edges : Iterator[Tuple[str, str, str]]
        The ``(u, label, v)`` edge tuples (the order is not guaranteed —
        rdflib iterates in store order).
    """
    tmp = rdflib.Graph()
    tmp.parse(str(path))

    for subj, pred, obj in tmp:
        yield _node_id(subj), _label(pred), _node_id(obj)

    logging.info(f"Stream edges from {path=}")


def graph_from_rdf(path: Union[pathlib.Path, str]) -> nx.MultiDiGraph:
    """Loads a graph from RDF file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the RDF file with which the graph will be created.

    Examples
    --------
    >>> from flpq_data import *
    >>> import pathlib, tempfile
    >>> d = pathlib.Path(tempfile.mkdtemp())
    >>> p = d / "g.csv"
    >>> _ = p.write_text("0 1 a\\n1 2 b\\n")
    >>> g = graph_from_csv(path=p)
    >>> path = graph_to_rdf(g, d / "g.ttl")
    >>> generations = graph_from_rdf(path)
    >>> generations.number_of_nodes()
    3
    >>> generations.number_of_edges()
    2

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
    """Saves the ``graph`` to the RDF file by ``path``.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path : Union[Path, str]
        The path to the file where the graph will be saved.

    Examples
    --------
    >>> from flpq_data import *
    >>> import pathlib, tempfile
    >>> d = pathlib.Path(tempfile.mkdtemp())
    >>> p = d / "g.csv"
    >>> _ = p.write_text("0 1 a\\n1 2 b\\n")
    >>> g = graph_from_csv(p)
    >>> path = graph_to_rdf(g, d / "g.ttl")

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
