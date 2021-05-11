import os
import random
import tempfile

import numpy as np
import pytest

import cfpq_data

seed = 42
random.seed(seed)
np.random.seed(seed)

g1 = cfpq_data.labeled_binomial_graph(42, 0.42, seed=seed)
g2 = cfpq_data.labeled_binomial_graph(42, 0.73, seed=seed)


@pytest.mark.parametrize(
    "graph",
    [
        g1,
        g2,
    ],
)
def test_txt(graph):
    (fd, fname) = tempfile.mkstemp()

    path = cfpq_data.graph_to_txt(graph, fname)
    gin = cfpq_data.graph_from_txt(path)

    os.close(fd)
    os.unlink(fname)

    assert (
        graph.number_of_nodes() == gin.number_of_nodes()
        and graph.number_of_edges() == gin.number_of_edges()
    )


@pytest.mark.parametrize(
    "graph",
    [
        "1 A 2",
        "1 A 2\n2 B 3",
    ],
)
def test_text(graph):
    g = cfpq_data.graph_from_text(graph)
    text = cfpq_data.graph_to_text(g)
    gin = cfpq_data.graph_from_text(text)

    assert (
        g.number_of_nodes() == gin.number_of_nodes()
        and g.number_of_edges() == gin.number_of_edges()
    )
