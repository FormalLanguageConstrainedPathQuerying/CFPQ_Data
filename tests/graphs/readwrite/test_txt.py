from itertools import product
import os
import random

import networkx as nx
import numpy as np
import pytest

import cfpq_data

seed = 42
random.seed(seed)
np.random.seed(seed)

g1 = cfpq_data.labeled_binomial_graph(42, 0.42, seed=seed, verbose=False)
g2 = cfpq_data.labeled_binomial_graph(42, 0.73, seed=seed, verbose=False)
g3 = cfpq_data.graph_from_text("1 2", verbose=False)
g4 = nx.path_graph(42, create_using=nx.MultiDiGraph)


@pytest.mark.parametrize(
    "graph, quoting, verbose",
    list(
        product(
            [
                g1,
                g2,
                g3,
                g4,
            ],
            [True, False],
            [True, False],
        )
    ),
)
def test_txt(graph, quoting, verbose):
    path = cfpq_data.graph_to_txt(graph, "test.txt", quoting=quoting, verbose=verbose)
    gin = cfpq_data.graph_from_txt(path, verbose=verbose)

    os.remove("test.txt")

    assert (
        graph.number_of_nodes() == gin.number_of_nodes()
        and graph.number_of_edges() == gin.number_of_edges()
    )


@pytest.mark.parametrize(
    "graph, quoting, verbose",
    list(
        product(
            [
                "1 A 2",
                "1 A 2\n2 B 3",
                "1 2\n2 3",
            ],
            [True, False],
            [True, False],
        )
    ),
)
def test_text(graph, quoting, verbose):
    g = cfpq_data.graph_from_text(graph, verbose=verbose)
    text = cfpq_data.graph_to_text(g, quoting=quoting, verbose=verbose)
    gin = cfpq_data.graph_from_text(text, verbose=verbose)

    assert (
        g.number_of_nodes() == gin.number_of_nodes()
        and g.number_of_edges() == gin.number_of_edges()
    )
