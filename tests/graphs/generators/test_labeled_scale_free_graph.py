import random

import numpy as np
import pytest

import cfpq_data

seed = 42
random.seed(seed)
np.random.seed(seed)

g1 = cfpq_data.labeled_scale_free_graph(29, seed=seed, verbose=False)
g2 = cfpq_data.labeled_scale_free_graph(42, seed=seed, verbose=False)


@pytest.mark.parametrize(
    "graph,expected_nodes,expected_edges", [(g1, 29, 56), (g2, 42, 88)]
)
def test_labeled_scale_free_graph(graph, expected_nodes, expected_edges):
    assert (
        graph.number_of_nodes() == expected_nodes
        and graph.number_of_edges() == expected_edges
    )
