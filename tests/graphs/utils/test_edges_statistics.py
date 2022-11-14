import pytest

import cfpq_data

g1 = cfpq_data.labeled_two_cycles_graph(42, 29)
g2 = cfpq_data.labeled_cycle_graph(42)
g3 = cfpq_data.labeled_two_cycles_graph(42, 42, labels=("b", "a"))


@pytest.mark.parametrize(
    "graph,expected_frequency",
    [
        (g1, {"a": 43, "b": 30}),
        (g2, {"a": 42}),
        (g3, {"a": 43, "b": 43}),
    ],
)
def test_get_labels_frequency(graph, expected_frequency):
    assert cfpq_data.get_labels_frequency(graph) == expected_frequency


@pytest.mark.parametrize(
    "graph,expected_list",
    [(g1, ["a", "b"]), (g2, ["a"]), (g3, ["a", "b"])],
)
def test_get_sorted_labels(graph, expected_list):
    assert cfpq_data.get_sorted_labels(graph) == expected_list
