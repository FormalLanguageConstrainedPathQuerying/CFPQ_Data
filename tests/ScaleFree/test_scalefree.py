from cfpq_data import scale_free_graph
import os

def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True

def test_scalefree(suit_scalefree):
    vertices_number, vertices_degree = suit_scalefree
    first_graph = scale_free_graph.build(vertices_number, vertices_degree)
    second_graph_path = first_graph.save('tmp')
    second_graph = scale_free_graph.load(second_graph_path)
    os.remove(second_graph_path)

    assert check_metadata(first_graph, second_graph)