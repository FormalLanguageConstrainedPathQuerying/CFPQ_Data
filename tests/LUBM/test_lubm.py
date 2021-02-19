import os

from cfpq_data import LUBM


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_fullgraph(num_of_vertices):
    first_graph = LUBM.build(num_of_vertices)
    second_graph_path = first_graph.save('tmp')
    second_graph = LUBM.load_from_rdf(second_graph_path)
    os.remove(second_graph_path)

    assert check_metadata(first_graph, second_graph)
