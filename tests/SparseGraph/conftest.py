import pytest

list_of_probabilities = (0.1, 0.2, 0.3, 0.4)


@pytest.fixture(scope='session', params=[
    (vertices_number, edge_probability)
    for vertices_number in range(100, 600, 100)
    for edge_probability in list_of_probabilities
])
def suit_sparsegraph(request):
    return request.param
