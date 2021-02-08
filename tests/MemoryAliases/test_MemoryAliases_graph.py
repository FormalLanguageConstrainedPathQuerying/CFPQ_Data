from cfpq_data import MemoryAliases


def test_graph(ma_graph_name):
    ma_graph = MemoryAliases(ma_graph_name)

    actual_metadata = ma_graph.get_metadata()

    actual_number_of_vertices = actual_metadata['vertices']
    actual_number_of_edges = actual_metadata['edges']

    expected_number_of_vertices = len(ma_graph.graph.all_nodes())
    expected_number_of_edges = len(ma_graph.graph)

    assert actual_number_of_vertices == expected_number_of_vertices
    assert actual_number_of_edges == expected_number_of_edges
