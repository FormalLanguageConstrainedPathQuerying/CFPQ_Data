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


@pytest.mark.parametrize("graph", [g1, g2])
def test_graph_to_txt(graph):
    (fd, fname) = tempfile.mkstemp()

    path = cfpq_data.graph_to_txt(graph, fname)
    gin = cfpq_data.txt_graph(path)

    os.close(fd)
    os.unlink(fname)

    assert (
        graph.number_of_nodes() == gin.number_of_nodes()
        and graph.number_of_edges() == gin.number_of_edges()
    )
