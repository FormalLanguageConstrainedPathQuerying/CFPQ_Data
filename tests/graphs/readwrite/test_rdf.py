import os

import pytest
import rdflib

import flpq_data


@pytest.mark.parametrize(
    "graph_name",
    [
        "people",
        "foaf",
        "pizza",
        "core",
    ],
)
def test_rdf(graph_name):
    path = flpq_data.graph_dir(graph_name)
    graph = flpq_data.graph_from_mtx_dir(path / "graph")

    path_rdf = flpq_data.graph_to_rdf(graph, "test.ttl")
    graph_rdf = flpq_data.graph_from_rdf(path_rdf)

    os.remove("test.ttl")

    assert graph.number_of_nodes() == graph_rdf.number_of_nodes()
    assert graph.number_of_edges() == graph_rdf.number_of_edges()


def test_nodes():
    tmp = flpq_data.graph_from_text(["1 A 2"])
    path = flpq_data.graph_to_rdf(tmp, "test.ttl")
    g = flpq_data.graph_from_rdf(path)

    os.remove("test.ttl")

    assert tmp.number_of_nodes() == g.number_of_nodes()
    assert tmp.number_of_edges() == g.number_of_edges()


def test_iter_edges_from_rdf_current_encoding(tmp_path):
    p = tmp_path / "g.ttl"
    p.write_text(
        "<urn:flpq:node:0> <urn:flpq:label:a> <urn:flpq:node:1> .\n"
        "<urn:flpq:node:1> <urn:flpq:label:b_5> <urn:flpq:node:2> .\n"
    )

    # rdflib iterates in store order, not file order.
    assert sorted(flpq_data.iter_edges_from_rdf(p)) == [
        ("0", "a", "1"),
        ("1", "b_5", "2"),
    ]


def test_iter_edges_from_rdf_legacy_encoding(tmp_path):
    # The legacy form written by older graph_to_rdf: blank-node endpoints
    # (serialized as anonymous) and a Literal predicate. Node ids are opaque;
    # the label survives.
    p = tmp_path / "g.ttl"
    p.write_text('[] "a"^^<http://www.w3.org/2001/XMLSchema#string> [ ] .\n')

    edges = list(flpq_data.iter_edges_from_rdf(p))
    assert len(edges) == 1
    u, label, v = edges[0]
    assert label == "a"
    assert u != v


def test_iter_edges_from_rdf_rejects_foreign_terms(tmp_path):
    p = tmp_path / "g.ttl"
    p.write_text(
        "<http://example.org/s> <http://example.org/p> <http://example.org/o> .\n"
    )

    with pytest.raises(ValueError, match="Unrecognized"):
        list(flpq_data.iter_edges_from_rdf(p))


def test_rdf_from_edges_valid_encoding(tmp_path):
    p = tmp_path / "g.ttl"
    flpq_data.rdf_from_edges([(0, "a b", 1), (1, 'q"<{}|^`#', 2)], p)

    g = rdflib.Graph()
    g.parse(str(p))
    assert len(list(g)) == 2
    for subj, pred, obj in g:
        # Valid RDF 1.1: IRI endpoints and predicates (no Literals).
        assert isinstance(subj, rdflib.URIRef)
        assert isinstance(pred, rdflib.URIRef)
        assert isinstance(obj, rdflib.URIRef)
        assert str(subj).startswith("urn:flpq:node:")
        assert str(obj).startswith("urn:flpq:node:")
        assert str(pred).startswith("urn:flpq:label:")


def test_rdf_from_edges_round_trip(tmp_path):
    p = tmp_path / "g.ttl"
    edges = [(0, "a", 1), (1, "b_5", 2), (2, "label with space", 0)]
    flpq_data.rdf_from_edges(edges, p)

    assert sorted(flpq_data.iter_edges_from_rdf(p)) == sorted(
        (str(u), label, str(v)) for u, label, v in edges
    )
