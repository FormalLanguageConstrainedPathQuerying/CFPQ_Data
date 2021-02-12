from cfpq_data import memory_aliases_graph

def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True

def test_graph(ma_graph_name):
    first_graph = memory_aliases_graph.build(ma_graph_name)

    second_graph = memory_aliases_graph.build(ma_graph_name)

    assert check_metadata(first_graph, second_graph)
