import glob
import json

from cfpq_data.config import RELEASE_INFO


def rdf_dict():
    data_rdf = dict()
    names_rdf = RELEASE_INFO['RDF']
    for name in names_rdf:
        with open(f'./cfpq_data/data/RDF/Graphs/{name}_meta.json', 'r') as graph_info:
            data_rdf[name] = json.load(graph_info)
    return data_rdf


def memoryaliases_dict():
    data_memoryaliases = dict()
    names_memoryaliases = RELEASE_INFO['MemoryAliases']
    for name in names_memoryaliases:
        name_of_file = glob.glob('./cfpq_data/data/MemoryAliases/Graphs/' + name + '*')[0]
        with open(name_of_file, 'r') as graph_info:
            data_memoryaliases[name] = json.load(graph_info)
    return data_memoryaliases


def create_table():
    column_names = ["name", "vertices", "edges", "size of file"]
    table_rdf = \
        "| Name | Vertices | Edges | Size of file (Bytes) |\n" + \
        "|:---|:---|:---|:---|\n"

    table_memoryaliases = \
        "| Name | Vertices | Edges | Size of file (Bytes) |\n" + \
        "|:---|:---|:---|:---|\n"

    rdf = rdf_dict()
    memory_aliases = memoryaliases_dict()
    names_rdf = RELEASE_INFO['RDF']
    names_memoryaliases = RELEASE_INFO['MemoryAliases']

    for name in sorted(names_rdf, key=lambda x: int(rdf[x]["size of file"])):
        for column_name in column_names:
            table_rdf += "| " + str(rdf[name][column_name]) + " "
        table_rdf += "|\n"
    for name in sorted(names_memoryaliases, key=lambda x: int(memory_aliases[x]["size of file"])):
        for column_name in column_names:
            table_memoryaliases += "| " + str(memory_aliases[name][column_name]) + " "
        table_memoryaliases += "|\n"

    with open('./docs/README.md', 'rt') as input_file:
        lines = input_file.readlines()
    with open('./docs/README.md', 'wt') as output_file:
        for line in lines:
            if "#### RDF" in line:
                output_file.write(line)
                output_file.write(table_rdf)
                output_file.write("\n")
                continue
            elif "#### MemoryAliases" in line:
                output_file.write(line)
                output_file.write(table_memoryaliases)
                output_file.write("\n")
                continue
            output_file.write(line)


def clean_table():
    flag = 0
    with open('./docs/README.md', 'rt') as input_file:
        lines = input_file.readlines()
    with open('./docs/README.md', 'wt') as output_file:
        for line in lines:
            if "#### RDF" in line or "#### MemoryAliases" in line:
                output_file.write(line)
                flag = 1
            if "### Reference values" in line:
                flag = 0
            if flag == 0:
                output_file.write(line)


clean_table()
create_table()
