import pytest


@pytest.fixture(scope='session', params=[1, 2, 3])
def num_of_vertices(request):
    return request.param
