import os
import tempfile

import cfpq_data


class TestRDFGraphSerializer:
    @classmethod
    def setup_class(cls):
        cls.build_graphs()

    @classmethod
    def build_graphs(cls):
        cls.g1 = cfpq_data.RDFGraphCreator("pizza").create()
        cls.g2 = cfpq_data.RDFGraphCreator("foaf").create()

    def test_g1(self):
        (fd, fname) = tempfile.mkstemp()
        path = cfpq_data.RDFGraphSerializer(self.g1, fname).serialize()
        gin = cfpq_data.RDFGraphCreator(path).create()

        assert self.g1.number_of_nodes() == gin.number_of_nodes()
        assert self.g1.number_of_edges() == gin.number_of_edges()

        os.close(fd)
        os.unlink(fname)

    def test_g2(self):
        (fd, fname) = tempfile.mkstemp()
        path = cfpq_data.RDFGraphSerializer(self.g2, fname).serialize()
        gin = cfpq_data.RDFGraphCreator(path).create()

        assert self.g2.number_of_nodes() == gin.number_of_nodes()
        assert self.g2.number_of_edges() == gin.number_of_edges()

        os.close(fd)
        os.unlink(fname)
