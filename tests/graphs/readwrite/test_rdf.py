import os

import pytest

import cfpq_data


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
    path_csv = cfpq_data.download(graph_name)
    graph_csv = cfpq_data.graph_from_csv(path_csv)

    path_rdf = cfpq_data.graph_to_rdf(graph_csv, "test.ttl")
    graph_rdf = cfpq_data.graph_from_rdf(path_rdf)

    os.remove("test.ttl")

    assert graph_csv.number_of_nodes() == graph_rdf.number_of_nodes()
    assert graph_csv.number_of_edges() == graph_rdf.number_of_edges()


def test_nodes():
    tmp = cfpq_data.graph_from_text(["1 A 2"])
    path = cfpq_data.graph_to_rdf(tmp, "test.ttl")
    g = cfpq_data.graph_from_rdf(path)

    os.remove("test.ttl")

    assert tmp.number_of_nodes() == g.number_of_nodes()
    assert tmp.number_of_edges() == g.number_of_edges()
