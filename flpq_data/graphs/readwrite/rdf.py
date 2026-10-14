"""Read (and write) a graph from (and to) RDF file."""

import logging
import pathlib
import urllib.parse
from typing import Any, Iterable, Iterator, Tuple, Union

import networkx as nx
import rdflib
from rdflib.term import Node as RdfNode

from flpq_data.graphs.readwrite.graph import iter_edges_from_graph

__all__ = [
    "iter_edges_from_rdf",
    "rdf_from_edges",
    "graph_from_rdf",
    "graph_to_rdf",
]

#: The IRI prefixes of the RDF encoding (the "RDF encoding" section of
#: ``docs/graphs/index.rst``).
_NODE_IRI_PREFIX = "urn:flpq:node:"
_LABEL_IRI_PREFIX = "urn:flpq:label:"


def _node_id(term: RdfNode) -> str:
    """Returns the node id behind an RDF endpoint term.

    The current encoding uses IRIs ``urn:flpq:node:<id>`` (the percent-encoded
    id is decoded); the legacy form used blank nodes, which the Turtle
    serializer writes as anonymous — their ids are opaque, so the full term
    string is returned.

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
    return urllib.parse.unquote(text[len(_NODE_IRI_PREFIX) :])


def _label(term: RdfNode) -> str:
    """Returns the edge label behind an RDF predicate term.

    The current encoding uses IRIs ``urn:flpq:label:<label>`` (the
    percent-encoded label is decoded); the legacy form used Literals.

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
    return urllib.parse.unquote(text[len(_LABEL_IRI_PREFIX) :])


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
    # The format is always Turtle (the writer emits it); parse it explicitly
    # instead of guessing from the file extension (.rdf means RDF/XML).
    tmp = rdflib.Graph()
    tmp.parse(str(path), format="turtle")

    for subj, pred, obj in tmp:
        yield _node_id(subj), _label(pred), _node_id(obj)

    logging.info(f"Stream edges from {path=}")


def _iri(prefix: str, value: Any) -> str:
    """Returns the IRI ``prefix + value`` with the variable part encoded."""
    return prefix + urllib.parse.quote(str(value), safe="")


def rdf_from_edges(
    edges: Iterable[Tuple[Any, str, Any]], path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Writes an edge stream to an RDF file.

    Emits valid RDF 1.1 Turtle — one triple per line with IRI nodes
    ``urn:flpq:node:<id>`` and IRI predicates ``urn:flpq:label:<label>``, the
    variable components percent-encoded (the "RDF encoding" section of
    ``docs/graphs/index.rst``). The file is written line by line without an
    in-memory RDF store, so the memory stays O(1) in the number of edges.

    Parameters
    ----------
    edges : Iterable[Tuple[Any, str, Any]]
        The ``(u, label, v)`` edge tuples to write.

    path : Union[Path, str]
        The path to the RDF file where the edges will be saved.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "g.ttl"
    >>> _ = rdf_from_edges([(0, "a b", 1)], p)
    >>> p.read_text().strip()
    '<urn:flpq:node:0> <urn:flpq:label:a%20b> <urn:flpq:node:1> .'

    Returns
    -------
    path : Path
        Path to the RDF file where the edges will be saved.
    """
    with open(path, "w") as f:
        for u, label, v in edges:
            f.write(
                f"<{_iri(_NODE_IRI_PREFIX, u)}> "
                f"<{_iri(_LABEL_IRI_PREFIX, label)}> "
                f"<{_iri(_NODE_IRI_PREFIX, v)}> .\n"
            )

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save edges to {dest=}")

    return dest


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
    >>> g = graph_from_text(["0 a 1", "1 b 2"])
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
    graph = nx.MultiDiGraph()

    for u, label, v in iter_edges_from_rdf(path):
        graph.add_edge(u, v, label=label)

    logging.info(f"Load {graph=} from {path=}")

    return graph


def graph_to_rdf(
    graph: nx.MultiDiGraph, path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Saves the ``graph`` to the RDF file by ``path``.

    The file holds valid RDF 1.1 Turtle — one triple per edge with IRI nodes
    and predicates (see :func:`rdf_from_edges` and the "RDF encoding" section
    of ``docs/graphs/index.rst``).

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
    >>> g = graph_from_text(["0 a 1", "1 b 2"])
    >>> path = graph_to_rdf(g, d / "g.ttl")

    Returns
    -------
    path : Path
        Path to the file where the graph will be saved.
    """
    dest = rdf_from_edges(iter_edges_from_graph(graph), path)

    logging.info(f"Save {graph=} to {dest=}")

    return dest
