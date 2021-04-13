import cfpq_data


class TestTwoCyclesGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        cls.g1 = cfpq_data.TwoCyclesGraphCreator(42, 29).create()
        cls.g2 = cfpq_data.TwoCyclesGraphCreator(84, 58).create()

    def test_g1(self):
        assert self.g1.number_of_nodes() == 72
        assert self.g1.number_of_edges() == 73

    def test_g2(self):
        assert self.g2.number_of_nodes() == 143
        assert self.g2.number_of_edges() == 144
