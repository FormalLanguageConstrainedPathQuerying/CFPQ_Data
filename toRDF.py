import rdflib
from rdflib.namespace import RDF
from rdflib.namespace import RDFS
from rdflib.namespace import SKOS

from os import listdir
from os.path import isfile, join, splitext, basename

def process_dir (dir, target_dir):

   onlyfiles = [join(dir,f) for f in listdir(dir) if isfile(join(dir, f))]
   for file in onlyfiles:

    g=rdflib.Graph()
    g.load(file)


    l = set()

    for s,p,o in g:
        l.add(s)
        l.add(o)


    d = {x: i for i,x in enumerate(l,0) }

    out_file = join(target_dir, splitext(basename(file))[0])

    with open(out_file, 'a') as the_file:
      for s,p,o in g:        
        if (str(p)[-1] == 'A'):    
           the_file.write('%s a %s \n'%(d[s],d[o]))
        elif (str(p)[-1] == 'R'):
           the_file.write('%s b %s \n'%(d[s],d[o]))

    print ('vertices: ', len(l))



process_dir('/home/gsv/Projects/CFPQ_Data/data/Synthetic/Matrices/SparseGraph','/home/gsv/Projects/DataForFLCourse/SparseGraph/graphs')
