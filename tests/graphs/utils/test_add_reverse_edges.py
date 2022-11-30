import random

import pytest

import cfpq_data

seed = 42
random.seed(seed)

g1 = cfpq_data.labeled_barabasi_albert_graph(42, 3, seed=seed, labels="a")
g2 = cfpq_data.labeled_binomial_graph(42, 0.73, seed=seed, labels=["a"])
g3 = cfpq_data.labeled_two_cycles_graph(42, 29)

rg1 = cfpq_data.add_reverse_edges(g1)
rg2 = cfpq_data.add_reverse_edges(g2, mapping={"a": "b"})
rg3 = cfpq_data.add_reverse_edges(g3)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges",
    [
        (rg1, g1.number_of_nodes(), 2 * g1.number_of_edges()),
        (rg2, g2.number_of_nodes(), 2 * g2.number_of_edges()),
        (rg3, g3.number_of_nodes(), 2 * g3.number_of_edges()),
    ],
)
def test_add_reverse_edges(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
