def get_labels_count (rdf):
    d = {}
    for s,p,o in rdf:     
       d[p] = d.get(p,0) + 1
    
    sorted_d = [(k, v) for k, v in sorted(d.items(), key=lambda item: item[1])] 	
    sorted_d.reverse()

    return sorted_d

def print_config(lst, path_to_config):
    i = 0
    with open(path_to_config,'w') as config:
       for x in lst:
           config.write(x[0] + ' ' + str(i) + '\n')
           i = i + 1
