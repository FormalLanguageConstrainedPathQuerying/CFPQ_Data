import json
import os
import random
import shutil
from itertools import product
from pathlib import Path

import networkx as nx
import numpy as np
import requests
from rdflib import Graph
from tqdm import tqdm

from src.tools.base import Tool
from src.tools.rdf_helper import write_to_rdf, add_rdf_edge

SCALEFREE_GRAPH_TO_GEN = list(product(
    [100, 500, 2500, 10000]
    , [1, 3, 5, 10]
))

SPARSE_GRAPH_TO_GEN = [
    [5000, 0.001]
    , [10000, 0.001]
    , [10000, 0.01]
    , [10000, 0.1]
    , [20000, 0.001]
    , [40000, 0.001]
    , [80000, 0.001]
]

FULL_GRAPH_TO_GEN = [
    10
    , 50
    , 100
    , 200
    , 500
    , 1000
    , 2000
    , 5000
    , 10000
    , 25000
    , 50000
    , 80000
]

NUMBER_OF_WORST_CASES = 12

DATA_ROOT_DIR = 'data/'
GRAPHS_DIR = 'Graphs'


def get_info():
    """ Gets release info from release notes """

    with open('release_notes.json', 'r') as input_file:
        data = json.load(input_file)
        return data


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


def download_data(graph_group, graph_name, graph_key):
    dst = add_graph_dir(graph_group)

    arch_dst = Path(os.path.join(dst, f'{graph_name}.tar.xz'))

    download_file_from_google_drive(graph_key, arch_dst)


def to_file(filepath, graph):
    with open(filepath, 'w') as out_file:
        for t in graph:
            s, p, o = t[0], t[1], t[2]
            out_file.write(f'{s} {p} {o}\n')


def unpack_graph(graph_group, graph_name):
    to = Path(os.path.join(DATA_ROOT_DIR, graph_group, GRAPHS_DIR))

    arch = Path(os.path.join(to, f'{graph_name}.tar.xz'))

    shutil.unpack_archive(arch, to)

    os.remove(arch)


def gen_sparse_graph(target_dir, vertices, prob):
    tmp_graph = nx.generators.fast_gnp_random_graph(vertices, prob)

    output_graph = Graph()

    for l in tmp_graph:
        lbl = 'A' if random.randint() % 2 == 0 else 'AR'
        add_rdf_edge(l[0], lbl, l[1], output_graph)

    target = os.path.join(target_dir, f'G{vertices}k-{prob}')

    write_to_rdf(target, output_graph)


def gen_worst_case_graph(target_dir, vertices):
    output_graph = Graph()

    first_cycle = int(vertices / 2) + 1

    for i in range(0, first_cycle - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(first_cycle - 1, 'A', 0, output_graph)
    add_rdf_edge(first_cycle - 1, 'B', first_cycle, output_graph)

    for i in range(first_cycle, vertices - 1):
        add_rdf_edge(i, 'B', i + 1, output_graph)

    add_rdf_edge(vertices - 1, 'B', first_cycle - 1, output_graph)

    target = os.path.join(target_dir, f'worstcase_{vertices}')

    write_to_rdf(target, output_graph)


def gen_cycle_graph(target_dir, vertices):
    output_graph = Graph()

    for i in range(0, vertices - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(vertices - 1, 'A', 0, output_graph)

    target = os.path.join(target_dir, f'fullgraph_{vertices}')

    write_to_rdf(target, output_graph)


def gen_scale_free_graph(target_dir, n, k, labels):
    g = {i: [(j, np.random.choice(labels)) for j in range(k)] for i in range(k)}

    degree = [3] * k

    for i in range(k, n):
        to_vertices = np.random.choice(
            range(i)
            , size=k
            , replace=False
            , p=np.array(degree) / sum(degree)
        )

        g[i] = []
        degree.append(0)
        for to in to_vertices:
            label = np.random.choice(labels)
            g[i].append((to, label))
            degree[to] += 1
            degree[i] += 1

    output_graph = Graph()

    for v in g:
        for to in g[v]:
            add_rdf_edge(v, to[1], to[0], output_graph)

    target = os.path.join(target_dir, f'scale_free_graph_{n}_{k}')

    write_to_rdf(target, output_graph)


def clean_dir(name):
    path = Path(os.path.join(DATA_ROOT_DIR, name, GRAPHS_DIR))
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def add_graph_dir(name):
    dst = Path(os.path.join(DATA_ROOT_DIR, name, GRAPHS_DIR))
    dst.mkdir(parents=True, exist_ok=True)
    return dst


def generate_all_sparse_graphs():
    add_graph_dir('SparseGraph')

    graphs_dir = add_graph_dir('SparseGraph')

    for g in tqdm(SPARSE_GRAPH_TO_GEN, desc='Sparse graphs generation'):
        gen_sparse_graph(graphs_dir, g[0], g[1])


def generate_full_graphs():
    graphs_dir = add_graph_dir('FullGraph')

    for g in tqdm(FULL_GRAPH_TO_GEN, desc='Full graphs generation'):
        gen_cycle_graph(graphs_dir, g)


def generate_worst_case_graphs():
    graphs_dir = add_graph_dir('WorstCase')

    for n in tqdm(range(2, NUMBER_OF_WORST_CASES), desc='WorstCase graphs generation'):
        gen_worst_case_graph(graphs_dir, 2 ** n)


def generate_scale_free_graphs():
    graphs_dir = add_graph_dir('ScaleFree')

    for n, k in tqdm(SCALEFREE_GRAPH_TO_GEN, desc='ScaleFree graphs generation'):
        gen_scale_free_graph(graphs_dir, n, k, ['a', 'b', 'c', 'd'])


def gen_sierpinski_graph(target_dir, degree, predicates=['A']):
    """ Generates a Sierpinski Triangle graph. """

    def sierpinski(t, l, r, deg, preds, g):
        """ Core function for generating the Sierpinski Triangle. """

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
        """ Adds edges between vertices u and v for all predicates. """

        for p in preds:
            g += [[u, p, v]]
            g += [[v, p, u]]

    def _idgen():
        """ Generates integer identifiers for vertices. """

        c = 4
        while True:
            yield c
            c += 1

    ids = _idgen()
    graph = []
    sierpinski(1, 2, 3, degree, predicates, graph)

    with open(os.path.join(target_dir, f'sierpinskigraph_{degree}.txt'), 'w') as out_file:
        for triple in graph:
            out_file.write(f'{triple[0]} {triple[1]} {triple[2]} \n')


class GraphsLoadTool(Tool):
    def init_parser(self, parser):
        parser.add_argument(
            '--group'
            , choices=[
                'ALL'
                , 'RDF'
                , 'ScaleFree'
                , 'FullGraph'
                , 'WorstCase'
                , 'SparseGraph'
                , 'MemoryAliases'
            ]
            , required=True
            , type=str
            , help='Load specific part from dataset'
        )

    def eval(self, args):
        group = args.group

        if group in ('RDF', 'ALL'):
            clean_dir('RDF')
            graphs = get_info()['RDF']
            for graph_name in tqdm(graphs, desc='Downloading RDF'):
                download_data('RDF', graph_name, graphs[graph_name])
                unpack_graph('RDF', graph_name)

        if group in ('MemoryAliases', 'ALL'):
            clean_dir('MemoryAliases')
            graphs = get_info()['MemoryAliases']
            for graph_name in tqdm(graphs, desc='Downloading MemoryAliases'):
                download_data('MemoryAliases', graph_name, graphs[graph_name])
                unpack_graph('MemoryAliases', graph_name)

        if group in ('ScaleFree', 'ALL'):
            clean_dir('ScaleFree')
            generate_scale_free_graphs()

        if group in ('FullGraph', 'ALL'):
            clean_dir('FullGraph')
            generate_full_graphs()

        if group in ('WorstCase', 'ALL'):
            clean_dir('WorstCase')
            generate_worst_case_graphs()

        if group in ('SparseGraph', 'ALL'):
            clean_dir('SparseGraph')
            generate_all_sparse_graphs()
