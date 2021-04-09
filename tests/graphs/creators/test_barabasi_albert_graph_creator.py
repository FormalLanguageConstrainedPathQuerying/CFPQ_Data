import random

import numpy as np

import cfpq_data


class TestBarabasiAlbertGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        seed = 42
        random.seed(seed)
        np.random.seed(seed)
        cls.g1 = cfpq_data.BarabasiAlbertGraphCreator(100, 1, seed=seed).create()
        cls.g2 = cfpq_data.BarabasiAlbertGraphCreator(100, 3, seed=seed).create()

    def test_g1(self):
        assert self.g1.number_of_nodes() == 100
        assert self.g1.number_of_edges() == 99 * 2

    def test_g2(self):
        assert self.g2.number_of_nodes() == 100
        assert self.g2.number_of_edges() == (100 - 3) * 3 * 2
