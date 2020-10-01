from src.tools.base import Tool
import lzma
import tarfile
import os
import shutil
import requests
import numpy as np
import networkx as nx
import random
from rdflib import Graph
from src.tools.rdf_helper import write_to_rdf, add_rdf_edge


MEMORY_ALIASES_DOWNLOAD_ID = '1gZA4x3Nep7IiRv5j3MZlZF7git2sTMEo'
RDF_DOWNLOAD_ID = '1x4cELJ7kSwhqlLC0zrOcuxaF3c19qRnK'

SPARSE_GRAPH_TO_GEN = [
    [5000, 0.001],
    [10000, 0.001],
    [10000, 0.01],
    [10000, 0.1],
    [20000, 0.001],
    [40000, 0.001],
    [80000, 0.001],
]

FULL_GRAPH_TO_GEN = [
    10, 50, 100, 200,
    500, 1000, 2000,
    5000, 10000, 25000,
    50000, 80000,
]

NUMBER_OF_WORST_CASES = 12

RDF = 'RDF'
DATA_ROOT_DIR = 'data/'
MATRICES_DIR = 'Matrices'
MEMORY_ALIASES = 'MemoryAliases'

DATA_TO_UNPACK = {
    MEMORY_ALIASES: MEMORY_ALIASES_DOWNLOAD_ID,
    RDF: RDF_DOWNLOAD_ID
}


def download_file_from_google_drive(id, destination):
    URL = 'https://docs.google.com/uc?export=download'

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download_data(graph_key):
    print('Downloading from GDrive is started.')
    dst = os.path.join(DATA_ROOT_DIR, graph_key, MATRICES_DIR)
    clean_dir(dst)
    arch_dst = os.path.join(dst + '.tar.xz')
    print('Download archive to ' + arch_dst)
    download_file_from_google_drive(DATA_TO_UNPACK[graph_key], arch_dst)
    print('Downloading from GDrive is finished.')


def unpack(file_from, path_to):
    with lzma.open(file_from) as f:
        with tarfile.open(fileobj=f) as tar:
            tar.extractall(path_to)


def to_file(filepath, graph):
    with open(filepath, 'w') as out_file:
        for t in graph:
            s = t[0]
            p = t[1]
            o = t[2]
            out_file.write('%s %s %s\n' % (s, p, o))


def unpack_graphs(graph_key):
    to = os.path.join(DATA_ROOT_DIR, graph_key)
    arch = os.path.join(to, '%s.tar.xz' % MATRICES_DIR)
    print('Unpack ', arch, ' to ', to)
    unpack(arch, to)


def gen_sparse_graph(target_dir, vertices, prob):
    tmp_graph = nx.generators.fast_gnp_random_graph(vertices, prob)
    output_graph = Graph()
    target = os.path.join(target_dir, 'G%sk-%s' % (int(vertices / 1000), prob))
    for l in tmp_graph:
        lbl = 'A' if random.randint() % 2 == 0 else 'AR'
        add_rdf_edge(l[0], lbl, l[1], output_graph)
    write_to_rdf(target, output_graph)


def gen_worst_case_graph(target_dir, vertices):
    first_cycle = int(vertices / 2) + 1
    output_graph = Graph()
    target = os.path.join(target_dir, 'worstcase_%s' % (vertices))

    for i in range(0, first_cycle - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(first_cycle - 1, 'A', 0, output_graph)
    add_rdf_edge(first_cycle - 1, 'B', first_cycle, output_graph)
    for i in range(first_cycle, vertices - 1):
        add_rdf_edge(i, 'B', i + 1, output_graph)

    add_rdf_edge(vertices - 1, 'B', first_cycle - 1, output_graph)

    write_to_rdf(target, output_graph)


def gen_cycle_graph(target_dir, vertices):
    output_graph = Graph()
    target = os.path.join(target_dir, 'fullgraph_%s' % (vertices))

    for i in range(0, vertices - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)
    add_rdf_edge(vertices - 1, 'A', 0, output_graph)

    write_to_rdf(target, output_graph)


def gen_scale_free_graph(target_dir, n, k, labels):
    g = {i: [(j, np.random.choice(labels)) for j in range(k)] for i in range(k)}
    degree = [3] * k

    for i in range(k, n):
        to_vertices = np.random.choice(
            range(i), size=k, replace=False, p=np.array(degree) / sum(degree)
        )

        g[i] = []
        degree.append(0)
        for to in to_vertices:
            label = np.random.choice(labels)
            g[i].append((to, label))
            degree[to] += 1
            degree[i] += 1

    output_graph = Graph()
    target = os.path.join(target_dir, 'scale_free_graph_%s_%s') % (n, k)
    for v in g:
        for to in g[v]:
            add_rdf_edge(v, to[1], to[0], output_graph)

    write_to_rdf(target, output_graph)


def clean_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def add_graph_dir(name):
    matrices_dir = os.path.join(DATA_ROOT_DIR, name, MATRICES_DIR)
    clean_dir(matrices_dir)
    return matrices_dir


def generate_all_sparse_graphs():
    print('Sparse graphs generation is started.')
    add_graph_dir('SparseGraph')
    matrices_dir = add_graph_dir('SparseGraph')
    for g in SPARSE_GRAPH_TO_GEN:
        gen_sparse_graph(matrices_dir, g[0], g[1])
    print('Sparse graphs generation is finished.')


def generate_full_graphs():
    print('Full graphs generation is started.')
    matrices_dir = add_graph_dir('FullGraph')
    for g in FULL_GRAPH_TO_GEN:
        gen_cycle_graph(matrices_dir, g)
    print('Full graphs generation is finished.')


def generate_worst_case_graphs():
    print('Worst case graphs generation is started.')
    matrices_dir = add_graph_dir('WorstCase')
    for n in range(2, NUMBER_OF_WORST_CASES):
        gen_worst_case_graph(matrices_dir, 2 ** n)
    print('Worst case graphs generation is finished.')


def generate_scale_free_graphs():
    print('Scale free graphs generation is started.')
    matrices_dir = add_graph_dir('ScaleFree')
    for k in 1, 3, 5, 10:
        for n in 100, 500, 2500, 10000:
            gen_scale_free_graph(matrices_dir, n, k, ['a', 'b', 'c', 'd'])
    print('Scale free graphs generation is finished.')


def gen_sierpinski_graph(target_dir, degree, predicates=['A']):
    ''' Generates a Sierpinski Triangle graph. '''

    def sierpinski(t, l, r, deg, preds, g):
        ''' Core function for generating the Sierpinski Triangle. '''
        if deg > 0:
            lt = next(ids)
            tr = next(ids)
            rl = next(ids)
            sierpinski(l, lt, rl, deg - 1, preds, g)
            sierpinski(lt, t, tr, deg - 1, preds, g)
            sierpinski(rl, tr, r, deg - 1, preds, g)
        else:
            add_edges(l, t, preds, g)
            add_edges(t, r, preds, g)
            add_edges(r, l, preds, g)

    def add_edges(u, v, preds, g):
        ''' Adds edges between vertices u and v for all predicates. '''
        for p in preds:
            g += [[u, p, v]]
            g += [[v, p, u]]

    def _idgen():
        ''' Generates integer identifiers for vertices. '''
        c = 4
        while True:
            yield c
            c += 1

    ids = _idgen()
    graph = []
    sierpinski(1, 2, 3, degree, predicates, graph)
    with open(
            os.path.join(target_dir, 'sierpinskigraph_%s.txt' % (degree)), 'w'
    ) as out_file:
        for triple in graph:
            out_file.write('%s %s %s \n' % (triple[0], triple[1], triple[2]))


class InitTool(Tool):
    def init_parser(self, parser):
        parser.add_argument(
            '--update',
            choices=[
                'rdf', 'scalefree', 'full', 'worstcase', 'sparse', 'memoryaliases'
            ],
            required=False,
            type=str,
            help='partial dataset update',
        )

    def eval(self, args):
        prt = args.update
        if prt == 'rdf':
            download_data(RDF)
            unpack_graphs(RDF)
        elif prt == 'memoryaliases':
            download_data(MEMORY_ALIASES)
            unpack_graphs(MEMORY_ALIASES)
        elif prt == 'scalefree':
            generate_scale_free_graphs()
        elif prt == 'full':
            generate_full_graphs()
        elif prt == 'worstcase':
            generate_worst_case_graphs()
        elif prt == 'sparse':
            generate_all_sparse_graphs()
        else:
            for graph_key in DATA_TO_UNPACK:
                download_data(graph_key)
                unpack_graphs(graph_key)
            generate_all_sparse_graphs()
            generate_full_graphs()
            generate_worst_case_graphs()
            generate_scale_free_graphs()
