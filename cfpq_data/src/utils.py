import json
import os
import shutil
from pathlib import Path

import requests

DATA_ROOT_DIR = 'data/'
GRAPHS_DIR = 'Graphs'


def get_info():
    """ Gets release info from release notes """

    with open(f'{Path(__file__).parent.parent.absolute()}/release_notes.json', 'r') as input_file:
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

    return dst


def to_file(filepath, graph):
    with open(filepath, 'w') as out_file:
        for t in graph:
            s, p, o = t[0], t[1], t[2]
            out_file.write(f'{s} {p} {o}\n')


def unpack_archive_listdir(dir, arch):
    tmp = f'{dir}/tmp'
    os.mkdir(tmp)
    shutil.unpack_archive(arch, tmp)
    result = os.listdir(tmp)
    shutil.rmtree(tmp)
    return result


def unpack_graph(graph_group, graph_name):
    to = Path(os.path.join(DATA_ROOT_DIR, graph_group, GRAPHS_DIR))

    arch = Path(os.path.join(to, f'{graph_name}.tar.xz'))

    shutil.unpack_archive(arch, to)

    graph = unpack_archive_listdir(to, arch)[0]

    os.remove(arch)

    return os.path.join(to, graph)


def clean_dir(name):
    path = Path(os.path.join(DATA_ROOT_DIR, name, GRAPHS_DIR))
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def add_graph_dir(name):
    dst = Path(os.path.join(DATA_ROOT_DIR, name, GRAPHS_DIR))
    dst.mkdir(parents=True, exist_ok=True)
    return f'{dst}'


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
