import os

from cfpq_data import RDF


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_rdf(rdf_graph_name):
    first_graph = RDF.build(rdf_graph_name).save('tmp1')
    first_graph_obj = RDF.build(first_graph)
    second_graph = RDF.build(rdf_graph_name).save('tmp2')
    second_graph_obj = RDF.build(second_graph)

    os.remove(first_graph)
    os.remove(second_graph)

    assert check_metadata(first_graph_obj, second_graph_obj)
