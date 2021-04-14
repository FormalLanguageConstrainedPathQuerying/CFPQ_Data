import pytest

import cfpq_data

g1 = cfpq_data.txt_graph(
    "\n".join(
        [f"{u} {label} {v}" for u, label, v in [(1, "A", 2), (2, "A", 3), (3, "A", 1)]]
    )
)
g2 = cfpq_data.txt_graph(
    "\n".join([f"{u} {label} {v}" for u, label, v in [(1, "A", 2)]])
)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges", [(g1, 3, 3), (g2, 2, 1)]
)
def test_txt_graph(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
