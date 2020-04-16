from os import listdir
from os.path import isfile, join
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

def convert_file(in_file_path, out_file_path):
    output_graph = Graph()
    with open(in_file_path) as in_file:       
        for l in in_file.readlines():
        	a = list(filter(None, l.split()))
        	if len(a) > 0 and a[2][0] != '-':
        		add_rdf_edge(a[0], a[2].upper(), a[1], output_graph)
	
    write_to_rdf(out_file_path, output_graph)

def process_folder(folder):
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

    for file in onlyfiles:
        print('Start: ' + file)
        full_path = join(folder, file)
        convert_file(full_path, full_path)