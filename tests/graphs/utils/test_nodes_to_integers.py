import pytest

import cfpq_data

foaf = cfpq_data.download("foaf")
core = cfpq_data.download("core")

g1 = cfpq_data.graph_from_csv(foaf)
g2 = cfpq_data.graph_from_csv(core)


@pytest.mark.parametrize(
    "graph",
    [
        g1,
        g2,
    ],
)
def test_nodes_to_integers(graph):
    actual = list(cfpq_data.nodes_to_integers(graph).nodes())

    expected = list(range(graph.number_of_nodes()))

    assert actual == expected
