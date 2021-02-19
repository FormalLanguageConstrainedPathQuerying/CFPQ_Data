import os

from cfpq_data import WorstCase


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_worstcase(num_of_vertices):
    first_graph = WorstCase.build(num_of_vertices)
    second_graph_path = first_graph.save('tmp')
    second_graph = WorstCase.load_from_rdf(second_graph_path)
    os.remove(second_graph_path)

    assert check_metadata(first_graph, second_graph)


def test_txt(num_of_vertices):
    first_graph = WorstCase.build(num_of_vertices)
    second_graph_path = first_graph.save('tmp', 'txt')
    second_graph = WorstCase.load_from_txt(second_graph_path)

    os.remove(second_graph_path)

    assert check_metadata(first_graph, second_graph)
