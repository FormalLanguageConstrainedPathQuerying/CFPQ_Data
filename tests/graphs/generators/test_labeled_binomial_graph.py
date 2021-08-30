import random

import pytest

import cfpq_data

seed = 42
random.seed(seed)

g1 = cfpq_data.labeled_binomial_graph(42, 0.42, seed=seed, verbose=False)
g2 = cfpq_data.labeled_binomial_graph(42, 0.73, seed=seed, verbose=False)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges", [(g1, 42, 692), (g2, 42, 1255)]
)
def test_labeled_binomial_graph(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
