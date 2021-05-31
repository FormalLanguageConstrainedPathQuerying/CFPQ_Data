import pytest

import cfpq_data

g1 = cfpq_data.labeled_two_cycles_graph(42, 29, verbose=False)
g2 = cfpq_data.labeled_cycle_graph(42, verbose=False)

rg1 = cfpq_data.filter_edges(g1, ["a"], verbose=False)
rg2 = cfpq_data.filter_edges(g2, ["a"], verbose=False)


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
