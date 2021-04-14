import os
import tempfile

import pytest

import cfpq_data


@pytest.mark.parametrize("graph_name", ["people_pets", "foaf"])
def test_graph_to_rdf(graph_name):
    (fd, fname) = tempfile.mkstemp()

    graph = cfpq_data.rdf_graph(graph_name)
    path = cfpq_data.graph_to_rdf(graph, fname)
    gin = cfpq_data.rdf_graph(path)

    os.close(fd)
    os.unlink(fname)

    assert (
        graph.number_of_nodes() == gin.number_of_nodes()
        and graph.number_of_edges() == gin.number_of_edges()
    )
