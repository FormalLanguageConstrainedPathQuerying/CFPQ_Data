import cfpq_data


class TestCycleGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        cls.g1 = cfpq_data.CycleGraphCreator(29).create()
        cls.g2 = cfpq_data.CycleGraphCreator(42).create()

    def test_g1(self):
        assert self.g1.number_of_nodes() == 29
        assert self.g1.number_of_edges() == 29

    def test_g2(self):
        assert self.g2.number_of_nodes() == 42
        assert self.g2.number_of_edges() == 42
