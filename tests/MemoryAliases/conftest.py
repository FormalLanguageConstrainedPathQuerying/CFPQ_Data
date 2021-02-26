import pytest


@pytest.fixture(scope='session', params=[
    'bzip2'
    , 'gzip'
    , 'ls'
    , 'pr'
    , 'wc'
])
def ma_graph_name(request):
    return request.param
