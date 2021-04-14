import pytest

import cfpq_data


@pytest.mark.parametrize(
    "graph_name,expected_nodes,expected_edges",
    [("travel", 131, 277), ("skos", 144, 252)],
)
def test_rdf_graph(graph_name, expected_nodes, expected_edges):
    graph = cfpq_data.rdf_graph(graph_name)
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
