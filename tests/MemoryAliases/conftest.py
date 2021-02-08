import pytest

from cfpq_data.src.utils import get_info

mas = get_info()['MemoryAliases']


@pytest.fixture(scope='session', params=[
    name
    for name, _ in mas.items()
])
def ma_graph_name(request):
    return request.param
