import random

import numpy as np

import cfpq_data


class TestSpecifiedGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        seed = 42
        random.seed(seed)
        np.random.seed(seed)
        cls.g1 = cfpq_data.BarabasiAlbertGraphCreator(
            100, 1, seed=seed, edge_labels="A"
        ).create()
        cls.g2 = cfpq_data.BinomialGraphCreator(
            42, 0.73, seed=seed, edge_labels="A"
        ).create()

    def test_g1(self):
        gin = cfpq_data.SpecifiedGraphCreator(self.g1, {"A": "B"}).create()

        assert gin.number_of_nodes() == self.g1.number_of_nodes()
        assert gin.number_of_edges() == self.g1.number_of_edges()

        number_of_a = sum(
            [1 for u, v, labels in self.g1.edges(data=True) if labels["label"] == "A"]
        )
        number_of_b = sum(
            [1 for u, v, labels in gin.edges(data=True) if labels["label"] == "B"]
        )

        assert number_of_a == number_of_b

    def test_g2(self):
        gin = cfpq_data.SpecifiedGraphCreator(self.g2, {"A": "B"}).create()

        assert gin.number_of_nodes() == self.g2.number_of_nodes()
        assert gin.number_of_edges() == self.g2.number_of_edges()

        number_of_a = sum(
            [1 for u, v, labels in self.g2.edges(data=True) if labels["label"] == "A"]
        )
        number_of_b = sum(
            [1 for u, v, labels in gin.edges(data=True) if labels["label"] == "B"]
        )

        assert number_of_a == number_of_b
