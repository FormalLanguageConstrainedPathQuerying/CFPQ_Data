import os

from cfpq_data import ScaleFree


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_scalefree(suit_scalefree):
    vertices_number, vertices_degree = suit_scalefree
    first_graph = ScaleFree.build(vertices_number, vertices_degree)
    second_graph_path = first_graph.save('tmp')
    second_graph = ScaleFree.load(second_graph_path)
    os.remove(second_graph_path)

    assert check_metadata(first_graph, second_graph)


def test_txt(suit_scalefree):
    vertices_number, vertices_degree = suit_scalefree
    first_graph = ScaleFree.build(vertices_number, vertices_degree)
    first_graph_path = first_graph.save('tmp1', 'txt')
    second_graph = ScaleFree.load_from_txt(first_graph_path)

    os.remove(first_graph_path)

    assert check_metadata(first_graph, second_graph)
