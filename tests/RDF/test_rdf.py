from cfpq_data import rdf_graph


def check_metadata(first_graph, second_graph):
    for field in ['vertices', 'edges']:
        if first_graph.get_metadata()[field] != second_graph.get_metadata()[field]:
            return False
    return True


def test_rdf(rdf_graph_name):
    first_graph = rdf_graph.build(rdf_graph_name)

    second_graph = rdf_graph.build(rdf_graph_name)

    assert check_metadata(first_graph, second_graph)
