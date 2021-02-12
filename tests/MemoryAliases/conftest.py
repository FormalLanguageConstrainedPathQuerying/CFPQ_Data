import pytest

from cfpq_data.config import RELEASE_INFO

mas = RELEASE_INFO['MemoryAliases']


@pytest.fixture(scope='session', params=[
    'bzip2'
    , 'gzip'
    , 'ls'
    , 'pr'
    , 'wc'
])
def ma_graph_name(request):
    return request.param
