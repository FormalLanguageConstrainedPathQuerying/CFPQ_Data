from itertools import product
import os
import random

import networkx as nx
import pytest

import cfpq_data

seed = 42
random.seed(seed)

g1 = cfpq_data.labeled_binomial_graph(42, 0.42, seed=seed)
g2 = cfpq_data.labeled_binomial_graph(42, 0.73, seed=seed)
g3 = cfpq_data.graph_from_text(["1 A 2"])


@pytest.mark.parametrize(
    "graph, quoting",
    list(
        product(
            [
                g1,
                g2,
                g3,
            ],
            [True, False],
        )
    ),
)
def test_txt(graph, quoting):
    path = cfpq_data.graph_to_txt(graph, "test.txt", quoting=quoting)
    gin = cfpq_data.graph_from_txt(path)

    os.remove("test.txt")

    assert graph.number_of_nodes() == gin.number_of_nodes()
    assert graph.number_of_edges() == gin.number_of_edges()


@pytest.mark.parametrize(
    "graph, quoting",
    list(
        product(
            [
                ["1 A 2"],
                ["1 A 2", "2 B 3"],
            ],
            [True, False],
        )
    ),
)
def test_text(graph, quoting):
    g = cfpq_data.graph_from_text(graph)
    text = cfpq_data.graph_to_text(g, quoting=quoting)
    gin = cfpq_data.graph_from_text(text)

    assert g.number_of_nodes() == gin.number_of_nodes()
    assert g.number_of_edges() == gin.number_of_edges()


def test_text_format():
    with pytest.raises(ValueError):
        cfpq_data.graph_from_text(["1 2 3 4"])
