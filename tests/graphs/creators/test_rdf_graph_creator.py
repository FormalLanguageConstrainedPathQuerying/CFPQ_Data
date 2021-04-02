import cfpq_data


class TestRDFGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        cls.g1 = cfpq_data.RDFGraphCreator("pizza").create()
        cls.g2 = cfpq_data.RDFGraphCreator("geospecies").create()

    def test_g1(self):
        assert self.g1.number_of_nodes() == 671
        assert self.g1.number_of_edges() == 1980

    def test_g2(self):
        assert self.g2.number_of_nodes() == 450609
        assert self.g2.number_of_edges() == 2201532
