import random

import numpy as np
import pytest

import cfpq_data

seed = 42
random.seed(seed)
np.random.seed(seed)

g1 = cfpq_data.labeled_barabasi_albert_graph(100, 1, seed=seed)
g2 = cfpq_data.labeled_barabasi_albert_graph(100, 3, seed=seed)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges", [(g1, 100, 198), (g2, 100, 582)]
)
def test_labeled_barabasi_albert_graph(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
