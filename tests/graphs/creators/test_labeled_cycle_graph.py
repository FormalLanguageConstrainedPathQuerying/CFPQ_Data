import pytest

import cfpq_data

g1 = cfpq_data.labeled_cycle_graph(29)
g2 = cfpq_data.labeled_cycle_graph(42)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges", [(g1, 29, 29), (g2, 42, 42)]
)
def test_labeled_cycle_graph(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
