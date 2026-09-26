import os
import random
from itertools import product

import pytest

import flpq_data

seed = 42
random.seed(seed)

g1 = flpq_data.labeled_binomial_graph(42, 0.42, seed=seed)
g2 = flpq_data.labeled_binomial_graph(42, 0.73, seed=seed)
g3 = flpq_data.graph_from_text(["1 A 2"])


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
    path = flpq_data.graph_to_txt(graph, "test.txt", quoting=quoting)
    gin = flpq_data.graph_from_txt(path)

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
    g = flpq_data.graph_from_text(graph)
    text = flpq_data.graph_to_text(g, quoting=quoting)
    gin = flpq_data.graph_from_text(text)

    assert g.number_of_nodes() == gin.number_of_nodes()
    assert g.number_of_edges() == gin.number_of_edges()


def test_text_format():
    with pytest.raises(ValueError):
        flpq_data.graph_from_text(["1 2 3 4"])
