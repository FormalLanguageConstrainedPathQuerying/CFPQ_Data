import pytest

import cfpq_data

g1 = cfpq_data.labeled_two_cycles_graph(42, 29)
g2 = cfpq_data.labeled_cycle_graph(42)

rg1 = cfpq_data.filter_edges(g1, ["a"])
rg2 = cfpq_data.filter_edges(g2, ["a"])


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges",
    [
        (rg1, g1.number_of_nodes(), 43),
        (rg2, g2.number_of_nodes(), 42),
    ],
)
def test_change_edges(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
