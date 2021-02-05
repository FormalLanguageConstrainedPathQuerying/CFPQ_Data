from cfpq_data import RDF


def test_graph(rdf_graph_name):
    rdf_graph = RDF(rdf_graph_name)

    actual_metadata = rdf_graph.get_metadata()

    actual_number_of_vertices = actual_metadata['vertices']
    actual_number_of_edges = actual_metadata['edges']

    expected_number_of_vertices = len(rdf_graph.graph.all_nodes())
    expected_number_of_edges = len(rdf_graph.graph)

    assert actual_number_of_vertices == expected_number_of_vertices
    assert actual_number_of_edges == expected_number_of_edges
