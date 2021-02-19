import os

from cfpq_data import SparseGraph


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_sparse(suit_sparsegraph):
    vertices_number, edge_probability = suit_sparsegraph
    first_graph = SparseGraph.build(vertices_number, edge_probability)
    second_graph_path = first_graph.save('tmp')
    second_graph = SparseGraph.load(second_graph_path)
    os.remove(second_graph_path)

    assert check_metadata(first_graph, second_graph)
