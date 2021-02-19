import pytest

from cfpq_data.config import RELEASE_INFO

rdfs = RELEASE_INFO['RDF']


@pytest.fixture(scope='session', params=[
    'atom-primitive'
    , 'biomedical-mesure-primitive'
    , 'core'
    , 'foaf'
    , 'funding'
    , 'generations'
    , 'people_pets'
    , 'skos'
    , 'travel'
    , 'univ-bench'
    , 'wine'
])
def rdf_graph_name(request):
    return request.param
