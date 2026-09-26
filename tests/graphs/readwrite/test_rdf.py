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
    graph_dir = flpq_data.download(graph_name)
    graph = flpq_data.graph_from_mtx_dir(graph_dir / "graph")

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
