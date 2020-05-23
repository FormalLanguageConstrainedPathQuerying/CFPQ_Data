import numpy, sys, os,  shutil

templates = [(1, '%s*', 'q1'), (2, '%s %s*', 'q2'), (3, '%s %s* %s*', 'q3'), 
             (2, '(%s | %s)*' , 'q4_2'), (3, '(%s | %s | %s)*', 'q4_3'), (4, '(%s | %s | %s | %s)*', 'q4_4'), (5, '(%s | %s | %s | %s | %s)*', 'q4_5'),
             (3, '%s %s* %s', 'q5'), (2, '%s* %s*', 'q6'), (3, '%s %s %s*', 'q7'), (2, '%s? %s*', 'q8'),
             (2, '(%s | %s)+', 'q9_2'), (3, '(%s | %s | %s)+', 'q9_3'), (4, '(%s | %s | %s | %s)+', 'q9_4'), (5, '(%s | %s | %s | %s | %s)+', 'q9_5'),
             (3, '(%s | %s) %s*', 'q10_2'), (4, '(%s | %s | %s) %s*', 'q10_3'), (5, '(%s | %s | %s | %s) %s*', 'q10_4'), (6, '(%s | %s | %s | %s | %s) %s*', 'q10_5'),
             (2, '%s %s', 'q11_2'), (3, '%s %s %s', 'q11_3'), (4, '%s %s %s %s', 'q11_4'), (5, '%s %s %s %s %s', 'q11_5')]

def gen (tpl, n, lst, k):
    res = set()
    while (len(res) < n):
        perm = numpy.random.permutation(lst)
        res.add(((tpl % tuple(perm[0:k])),tuple(perm[0:k])))
    return res

def gen_from_config(config, num_of_lalbels, num_of_queries):
    lbls = [ l.split(' ')[1].rstrip() for l in open(config,'r').readlines()]
    return [(tpl[2], gen (tpl[1], num_of_queries, lbls[0:num_of_lalbels], tpl[0])) for tpl in templates]

def print_qs (qs, root_dir):
    for qd in qs:
        path = os.path.join(root_dir, qd[0])
        if os.path.exists(path):
           shutil.rmtree(path)
        os.mkdir(path)
        i = 0
        for q in qd[1]:
            with open(os.path.join(path,str(i)),'w') as out:
                out.write('S\n')
                out.write(' '.join(q[1]) + '\n')
                out.write('S -> ' + q[0] + '\n')
                i = i + 1

r = gen_from_config(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))

print_qs(r, sys.argv[4])

for s in r:
	for q in s:
		print(q)