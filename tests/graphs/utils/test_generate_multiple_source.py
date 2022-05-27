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
@pytest.mark.parametrize(
    "chunk_size",
    [
        10,
        20,
        30,
    ],
)
def test_nodes_to_integers(graph, chunk_size):
    actual = len(cfpq_data.generate_multiple_source(graph, chunk_size))

    expected = chunk_size

    assert actual == expected