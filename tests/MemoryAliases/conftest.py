import pytest

from cfpq_data.config import RELEASE_INFO

mas = RELEASE_INFO['MemoryAliases']


@pytest.fixture(scope='session', params=[
    name
    for name, _ in mas.items() if name not in {'kernel_afterInline', 'PostgreSQL_8.3.9_pointsto_graph'}
])
def ma_graph_name(request):
    return request.param
