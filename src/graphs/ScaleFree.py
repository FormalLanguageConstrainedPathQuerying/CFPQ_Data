from itertools import product

import numpy as np
from rdflib import Graph
from tqdm import tqdm

from src.tools.base import Tool
from src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from src.utils import *

SCALEFREE_GRAPH_TO_GEN = list(product(
    [100, 500, 2500, 10000]
    , [1, 3, 5, 10]
))


class ScaleFree(Tool):
    def init_parser(self, parser):
        parser.add_argument(
            '-p'
            , '--preset'
            , action='store_true'
            , help='Load preset ScaleFree graphs from dataset'
        )
        parser.add_argument(
            '-n'
            , '--vertices_number'
            , required=False
            , type=int
            , help='Number of vertices of ScaleFree graph'
        )
        parser.add_argument(
            '-k'
            , '--vertices_degree'
            , required=False
            , type=int
            , help='Degree of vertices in a graph'
        )

    def eval(self, args):
        if args.preset is False and \
                (args.vertices_number is None or args.vertices_degree is None):
            print("One of -p/--preset, (-n/--vertices_number and necessarily -k/--vertices_degree) required")
            exit()

        graphs_dir = add_graph_dir('ScaleFree')

        if args.preset is True:
            for n, k in tqdm(SCALEFREE_GRAPH_TO_GEN, desc='ScaleFree graphs generation'):
                gen_scale_free_graph(graphs_dir, n, k, ['a', 'b', 'c', 'd'])

        if args.vertices_number is not None and args.vertices_degree is not None:
            graph = gen_scale_free_graph(
                graphs_dir
                , args.vertices_number
                , args.vertices_degree
                , ['a', 'b', 'c', 'd']
            )
            print(f'Generated {graph}')


def gen_scale_free_graph(target_dir, n, k, labels):
    g = {
        i: [(j, np.random.choice(labels)) for j in range(k)]
        for i in range(k)
    }

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

    return target
