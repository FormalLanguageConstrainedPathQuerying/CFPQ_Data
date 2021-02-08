import pytest

from cfpq_data.src.utils import get_info

rdfs = get_info()['RDF']


@pytest.fixture(scope='session', params=[
    name
    for name, _ in rdfs.items()
    if name not in {'taxonomy-hierarchy', 'taxonomy'}
])
def rdf_graph_name(request):
    return request.param
