import pytest


@pytest.fixture(scope='session', params=[
    (vertices_number, vertices_degree)
    for vertices_number in range(100, 1000, 100)
    for vertices_degree in range(3, 10)
])
def suit_scalefree(request):
    return request.param
