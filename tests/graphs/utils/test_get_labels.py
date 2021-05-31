import pytest

import cfpq_data

g1 = cfpq_data.graph_from_text("1 A 2", verbose=False)
g2 = cfpq_data.labeled_two_cycles_graph(42, 28, edge_labels=("x", "y"), verbose=False)
g3 = cfpq_data.graph_from_text("1 2\n3", verbose=False)


@pytest.mark.parametrize(
    "graph,expected_labels",
    [
        (g1, {"A"}),
        (g2, {"x", "y"}),
        (g3, set()),
    ],
)
def test_get_labels(graph, expected_labels):
    assert cfpq_data.get_labels(graph, verbose=False) == expected_labels
