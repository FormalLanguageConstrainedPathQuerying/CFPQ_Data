from rdflib import Graph, URIRef, BNode

URI_PREFIX = 'http://yacc/'

# RDF serialization
def write_to_rdf(target, graph):
    graph.serialize(target + '.xml', format='xml')


def add_rdf_edge(subj, pred, obj, graph):
    s = BNode('id-%s' % (subj))
    p = URIRef(URI_PREFIX + pred)
    o = BNode('id-%s' % (obj))
    graph.add((s, p, o))