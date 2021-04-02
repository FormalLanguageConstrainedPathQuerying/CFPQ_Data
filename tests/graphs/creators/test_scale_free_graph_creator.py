import cfpq_data


class TestScaleFreeGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        seed = 42
        cls.g1 = cfpq_data.ScaleFreeGraphCreator(29, seed=seed).create()
        cls.g2 = cfpq_data.ScaleFreeGraphCreator(42, seed=seed).create()

    def test_g1(self):
        assert self.g1.number_of_nodes() == 29
        assert self.g1.number_of_edges() == 56

    def test_g2(self):
        assert self.g2.number_of_nodes() == 42
        assert self.g2.number_of_edges() == 88
