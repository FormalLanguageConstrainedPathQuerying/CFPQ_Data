import os
from itertools import product

import pytest

import cfpq_data


@pytest.mark.parametrize(
    "graph_name, verbose",
    list(
        product(
            [
                "people_pets",
                "foaf",
                "pizza",
                "core",
            ],
            [True, False],
        )
    ),
)
def test_rdf(graph_name, verbose):
    graph = cfpq_data.graph_from_dataset(graph_name, verbose=verbose)
    path = cfpq_data.graph_to_rdf(graph, "test.xml", verbose=verbose)
    gin = cfpq_data.graph_from_rdf(path, verbose=verbose)

    os.remove("test.xml")

    assert (
        graph.number_of_nodes() == gin.number_of_nodes()
        and graph.number_of_edges() == gin.number_of_edges()
    )
