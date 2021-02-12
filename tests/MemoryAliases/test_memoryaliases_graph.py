from cfpq_data import memory_aliases_graph
import os

def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True

def test_graph(ma_graph_name):
    first_graph = memory_aliases_graph.build(ma_graph_name).save('tmp1')
    first_graph_obj = memory_aliases_graph.build(first_graph)
    second_graph = memory_aliases_graph.build(ma_graph_name).save('tmp2')
    second_graph_obj = memory_aliases_graph.build(second_graph)

    os.remove(first_graph)
    os.remove(second_graph)

    assert check_metadata(first_graph_obj, second_graph_obj)
