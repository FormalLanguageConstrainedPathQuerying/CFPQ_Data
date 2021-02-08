import json
import glob

def get_info():
    with open('./cfpq_data/release_notes.json', 'r') as input_file:
        data = json.load(input_file)
        return data

def rdf_dict():
    data_RDF = dict()
    names_RDF = get_info()['RDF']
    for name in names_RDF:
        if name == "taxonomy-hierarchy" or name == "taxonomy":
            continue
        with open(f'./cfpq_data/data/RDF/Graphs/{name}_meta.json', 'r') as graph_info:
            data_RDF[name] = json.load(graph_info)
    return data_RDF

def ma_dict():
    data_MA = dict()
    names_MA = get_info()['MemoryAliases']
    for name in names_MA:
        name_ = glob.glob('./cfpq_data/data/MemoryAliases/Graphs/' + name + '*')[0]
        with open(name_, 'r') as graph_info:
            data_MA[name] = json.load(graph_info)
    return data_MA

def create_table():
    column_names = ["name", "vertices", "edges", "size of file"]
    table_RDF = '''
| Name | Vertices | Edges | Size of file (Bytes) |
|:---:|:---:|:---:|:---:|
'''
    table_MA = '''
| Name | Vertices | Edges | Size of file (Bytes) |
|:---:|:---:|:---:|:---:|
'''
    rdf = rdf_dict()
    memory_aliases = ma_dict()
    names_rdf = get_info()['RDF']
    names_ma = get_info()['MemoryAliases']

    for name in names_rdf:
        if name == "taxonomy-hierarchy" or name == "taxonomy":
            continue
        for cname in column_names:
            table_RDF += "| " + str(rdf[name][cname]) + " "
        table_RDF += "|\n"
    for name in names_ma:
        for cname in column_names:
            table_MA += "| " + str(memory_aliases[name][cname]) + " "
        table_MA += "|\n"

    with open('./docs/README.md', 'rt') as input_file:
        lines = input_file.readlines()
    with open('./docs/README.md', 'wt') as output_file:
        for line in lines:
            if "#### RDF" in line:
                output_file.write(line)
                output_file.write(table_RDF)
                output_file.write("\n")
                continue
            elif "#### MemoryAliases" in line:
                output_file.write(line)
                output_file.write(table_MA)
                output_file.write("\n")
                continue
            output_file.write(line)

def clean_table():
    tmp = 0
    with open('./docs/README.md', 'rt') as input_file:
        lines = input_file.readlines()
    with open('./docs/README.md', 'wt') as output_file:
        for line in lines:
            if "#### RDF" in line or "#### MemoryAliases" in line:
                output_file.write(line)
                tmp = 1
            if "### Reference values" in line:
                tmp = 0
            if tmp == 0:
                output_file.write(line)



clean_table()
create_table()