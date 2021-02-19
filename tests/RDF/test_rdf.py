import os

from cfpq_data import RDF


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_rdf(rdf_graph_name):
    first_graph_path = RDF.build(rdf_graph_name).save('tmp1')
    first_graph = RDF.build(first_graph_path)
    second_graph_path = RDF.build(rdf_graph_name).save('tmp2')
    second_graph = RDF.build(second_graph_path)

    os.remove(first_graph_path)
    os.remove(second_graph_path)

    assert check_metadata(first_graph, second_graph)


def test_txt(rdf_graph_name):
    first_graph = RDF.build(rdf_graph_name)
    first_graph_path = first_graph.save('tmp1.txt', 'txt')
    second_graph = RDF.load_from_txt(first_graph_path)

    os.remove(first_graph_path)

    assert check_metadata(first_graph, second_graph)
