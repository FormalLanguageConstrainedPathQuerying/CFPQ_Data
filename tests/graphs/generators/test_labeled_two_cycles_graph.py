import pytest

import cfpq_data

g1 = cfpq_data.labeled_two_cycles_graph(42, 29)
g2 = cfpq_data.labeled_two_cycles_graph(84, 58)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges", [(g1, 72, 73), (g2, 143, 144)]
)
def test_labeled_two_cycles_graph(graph, expected_nodes, expected_edges):
    assert graph.number_of_nodes() == expected_nodes
    assert graph.number_of_edges() == expected_edges
