import pytest

from cfpq_data.config import RELEASE_INFO
from cfpq_data.src.utils import get_graph_info

rdfs = RELEASE_INFO['RDF']


@pytest.fixture(scope='session', params=[
    name
    for name, _ in rdfs.items()
    if name not in {'taxonomy-hierarchy', 'taxonomy'}
    if get_graph_info('RDF', name)['size of file'] < 1e7
])
def rdf_graph_name(request):
    return request.param
