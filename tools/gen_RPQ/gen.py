import numpy,sys 

templates = [(1,'%s*'), (2,'%s %s*'), (3,'%s %s* %s*'), (2,'(%s | %s)*'), (3,'(%s | %s | %s)*'), (4,'(%s | %s | %s | %s)*'), 
             (5,'(%s | %s | %s | %s | %s)*'), (3,'%s %s* %s'), (2,'%s* %s*'), (3,'%s %s %s*'), (2,'%s? %s*'),
             (2,'(%s | %s)+'), (3,'(%s | %s | %s)+'), (4,'(%s | %s | %s | %s)+'), (5,'(%s | %s | %s | %s | %s)+'),
             (3,'(%s | %s) %s*'), (4,'(%s | %s | %s) %s*'), (5,'(%s | %s | %s | %s) %s*'), (6,'(%s | %s | %s | %s | %s) %s*'),
             (2,'%s %s'), (3,'%s %s %s'), (4,'%s %s %s %s'), (5,'%s %s %s %s %s')]

def gen (tpl, n, lst, k):
    res = set()
    while (len(res) < n):
        perm = numpy.random.permutation(lst)
        res.add(tpl % tuple(perm[0:k]))
    return res

def gen_from_config(config, num_of_lalbels, num_of_queries):
    lbls = [ l.split(' ')[1].rstrip() for l in open(config,'r').readlines()]
    return [gen (tpl[1], num_of_queries, lbls[0:num_of_lalbels], tpl[0]) for tpl in templates]

r = gen_from_config(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))

for s in r:
	for q in s:
		print(q)