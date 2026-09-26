import pytest

import flpq_data

foaf = flpq_data.download("foaf")
core = flpq_data.download("core")

g1 = flpq_data.graph_from_mtx_dir(foaf / "graph")
g2 = flpq_data.graph_from_mtx_dir(core / "graph")


@pytest.mark.parametrize(
    "graph",
    [
        g1,
        g2,
    ],
)
def test_nodes_to_integers(graph):
    actual = list(flpq_data.nodes_to_integers(graph).nodes())

    expected = list(range(graph.number_of_nodes()))

    assert actual == expected
