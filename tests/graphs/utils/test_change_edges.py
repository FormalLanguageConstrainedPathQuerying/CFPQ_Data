import random

import numpy as np
import pytest

import cfpq_data

seed = 42
random.seed(seed)
np.random.seed(seed)

g1 = cfpq_data.labeled_barabasi_albert_graph(42, 3, seed, edge_labels="a")
g2 = cfpq_data.labeled_binomial_graph(42, 0.73, seed, edge_labels="a")

rg1 = cfpq_data.change_edges(g1, {"a": "b"})
rg2 = cfpq_data.change_edges(g2, {"a": "b"})


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges",
    [
        (rg1, g1.number_of_nodes(), g1.number_of_edges()),
        (rg2, g2.number_of_nodes(), g2.number_of_edges()),
    ],
)
def test_change_edges(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
