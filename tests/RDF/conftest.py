import pytest

from cfpq_data.config import RELEASE_INFO

rdfs = RELEASE_INFO['RDF']


@pytest.fixture(scope='session', params=[
    name
    for name, _ in rdfs.items()
    if name not in {'taxonomy-hierarchy', 'taxonomy'}
])
def rdf_graph_name(request):
    return request.param
