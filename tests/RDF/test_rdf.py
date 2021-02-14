import os

from cfpq_data import rdf_graph


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_rdf(rdf_graph_name):
    first_graph = rdf_graph.build(rdf_graph_name).save('tmp1')
    first_graph_obj = rdf_graph.build(first_graph)
    second_graph = rdf_graph.build(rdf_graph_name).save('tmp2')
    second_graph_obj = rdf_graph.build(second_graph)

    os.remove(first_graph)
    os.remove(second_graph)

    assert check_metadata(first_graph_obj, second_graph_obj)
