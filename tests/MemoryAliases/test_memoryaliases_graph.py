import os

from cfpq_data import MemoryAliases


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_graph(ma_graph_name):
    first_graph = MemoryAliases.build(ma_graph_name).save('tmp1')
    first_graph_obj = MemoryAliases.build(first_graph)
    second_graph = MemoryAliases.build(ma_graph_name).save('tmp2')
    second_graph_obj = MemoryAliases.build(second_graph)

    os.remove(first_graph)
    os.remove(second_graph)

    assert check_metadata(first_graph_obj, second_graph_obj)


def test_txt(ma_graph_name):
    first_graph = MemoryAliases.build(ma_graph_name)
    first_graph_path = first_graph.save('tmp1', 'txt')
    second_graph = MemoryAliases.build(first_graph_path, 'txt')

    os.remove(first_graph_path)

    assert check_metadata(first_graph, second_graph)
