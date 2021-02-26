import pytest


@pytest.fixture(scope='session', params=[vertices for vertices in range(100, 1000, 100)])
def num_of_vertices(request):
    return request.param
