import os

import pytest

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
