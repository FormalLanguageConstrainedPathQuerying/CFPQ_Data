import cfpq_data


class TestTXTGraphCreator:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        cls.g1 = cfpq_data.TXTGraphCreator(
            "\n".join([
                f"{u} {label} {v}"
                for u, label, v in [
                    (1, 'A', 2),
                    (2, 'A', 3),
                    (3, 'A', 1)
                ]
            ])
        ).create()
        cls.g2 = cfpq_data.TXTGraphCreator(
            "\n".join([
                f"{u} {label} {v}"
                for u, label, v in [
                    (1, 'A', 2),
                ]
            ])
        ).create()

    def test_g1(self):
        assert self.g1.number_of_nodes() == 3
        assert self.g1.number_of_edges() == 3

    def test_g2(self):
        assert self.g2.number_of_nodes() == 2
        assert self.g2.number_of_edges() == 1
