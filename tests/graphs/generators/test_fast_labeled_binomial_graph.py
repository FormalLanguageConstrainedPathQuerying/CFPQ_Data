import random

import pytest

import cfpq_data

seed = 42
random.seed(seed)

g1 = cfpq_data.fast_labeled_binomial_graph(29, 0.1, seed=seed)
g2 = cfpq_data.fast_labeled_binomial_graph(42, 0.1, seed=seed)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges", [(g1, 29, 85), (g2, 42, 177)]
)
def test_fast_labeled_binomial_graph(graph, expected_nodes, expected_edges):
    assert graph.number_of_nodes() == expected_nodes
    assert graph.number_of_edges() == expected_edges
