"""
    RDF merger and converter for LUBM dataset.
    Database is stored in files <prefix><id>_<sub_id>.owl
    This files are merged for specified number of universities (ids range),
    and edges are replaced with specified mapping.
    Also vertices labels also replaces with integer based names.
    
    Usage:
    - Create a conversion configuration file. Each line must contain an IRI,
      a whitespace character and a string to replace the IRI by.
    - Run converter.py <prefix> <count> <config>
    - Result will have name <pefix><count><vertices count><indices count>.xml
    
    The graph will contain explicit inverted edges added an 'R'.
"""

import rdflib, sys, os

URI_PREFIX = 'http://yacc/'
MAX_FILES_PER_UNI = 30

# RDF serialization
def write_to_rdf(target, graph):
    graph.serialize(target + '.xml', format='xml')

# Edge addition (grapf constructing)
def add_rdf_edge(subj, pred, obj, graph):
    s = rdflib.BNode('id-%s' % (subj))
    p = rdflib.URIRef(URI_PREFIX + pred)
    o = rdflib.BNode('id-%s' % (obj))
    graph.add((s, p, o))

if len(sys.argv) < 3:
    print('Usage: converter.py <prefix> <count> <config>')
    exit()

replace = {} # map for replacing predicates
config = sys.argv[3]
for l in open(config,'r').readlines():
    pair = l.split(' ')
    old = rdflib.URIRef(pair[0].strip(' '))
    new = pair[1].strip('\n').strip(' ')
    replace[old] = new

print(replace)

res = {}        # map from resources to integer ids
next_id = 0     # id counter
edges_count = 0 # Total edges 

graph = rdflib.Graph()
prefix = sys.argv[1]
count = int(sys.argv[2])

processed = []

for i in range(0,count):
  for j in range(0,MAX_FILES_PER_UNI):
    filename = prefix + str(i) + '_' + str(j) + '.owl'
    try:
      g = rdflib.Graph()
      g.parse(filename)
      graph = graph + g           # Merge graphs here (if 1 file with sub-graph - OK)
      processed.append(filename)
    except Exception:
      pass

output = rdflib.Graph()
for s,p,o in graph:
  for r in [s,o]:
    if r not in res:
      res[r] = str(next_id)
      next_id += 1
  if p in replace:
    add_rdf_edge(res[s], replace[p], res[o], output)
    add_rdf_edge(res[s], replace[p] + 'R', res[o], output)
    edges_count += 2
  else:
    add_rdf_edge(res[s], 'OTHER', res[o], output)
    edges_count += 1

target = prefix + str(count) + 'v' + str(next_id) + 'e' + edges_count  # output file
write_to_rdf(target,output)

print('Total vertices:', next_id)
print('Total edges:', edges_count)
print('Processed files:\n', processed)
