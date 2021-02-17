import os
import shutil

import rdflib
import requests

from cfpq_data.config import *

GRAPHS_DIR = 'Graphs'


def get_graph_info(graph_type, graph_name):
    target = MAIN_FOLDER / 'data' / graph_type / 'Graphs' / f'{graph_name}_meta.json'
    with open(target, 'r') as input_file:
        info = json.load(input_file)
    return info


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

    arch_dst = dst / f'{graph_name}.tar.xz'

    download_file_from_google_drive(graph_key, arch_dst)

    return dst


def unpack_archive_listdir(target_dir, arch):
    tmp = target_dir / 'tmp'
    os.mkdir(tmp)
    shutil.unpack_archive(arch, tmp)
    result = os.listdir(tmp)
    shutil.rmtree(tmp)
    return result


def unpack_graph(graph_group, graph_name):
    to = DATA_FOLDER / graph_group / GRAPHS_DIR

    arch = to / f'{graph_name}.tar.xz'

    shutil.unpack_archive(arch, to)

    graph = unpack_archive_listdir(to, arch)[0]

    os.remove(arch)

    return os.path.join(to, graph)


def clean_dir(name):
    path = DATA_FOLDER / name / GRAPHS_DIR
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def add_graph_dir(name):
    dst = DATA_FOLDER / name / GRAPHS_DIR
    dst.mkdir(parents=True, exist_ok=True)
    return dst


# RDF serialization
def write_to_rdf(target_path, graph: rdflib.Graph):
    graph.serialize(destination=str(target_path), format='xml')


# Edge addition (grapf constructing)
def add_rdf_edge(subj, pred, obj, rdf_graph, config=GENERATORS_CONFIG, reverse=False):
    s = rdflib.BNode(f'id-{subj}')

    p_text = config[pred]
    if not p_text.startswith('http'):
        p_text = f'http://yacc/rdf-schema#{p_text}'
    p = rdflib.URIRef(p_text)

    o = rdflib.BNode(f'id-{obj}')

    rdf_graph.add((s, p, o))

    if reverse is True:
        pr = rdflib.URIRef(p_text + 'R')

        rdf_graph.add((s, pr, o))


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

    with open(target_dir / f'sierpinskigraph_{degree}.txt', 'w') as out_file:
        for triple in graph:
            out_file.write(f'{triple[0]} {triple[1]} {triple[2]} \n')
