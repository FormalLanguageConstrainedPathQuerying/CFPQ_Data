import random

import numpy as np

import cfpq_data


class TestFastBinomialGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        seed = 42
        random.seed(seed)
        np.random.seed(seed)
        cls.g1 = cfpq_data.FastBinomialGraphCreator(29, 0.1, seed=seed).create()
        cls.g2 = cfpq_data.FastBinomialGraphCreator(42, 0.1, seed=seed).create()

    def test_g1(self):
        assert self.g1.number_of_nodes() == 29
        assert self.g1.number_of_edges() == 91

    def test_g2(self):
        assert self.g2.number_of_nodes() == 42
        assert self.g2.number_of_edges() == 182
