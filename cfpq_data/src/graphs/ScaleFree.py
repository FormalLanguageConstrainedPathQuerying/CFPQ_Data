from itertools import product

import numpy as np

from cfpq_data.src.graphs.RDF import RDF
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils import *

SCALEFREE_GRAPH_TO_GEN = list(product(
    [100, 500, 2500, 10000]
    , [1, 3, 5, 10]
))


class ScaleFree(RDF, CmdParser):
    graphs = {}

    @classmethod
    def build(cls, vertices_number, vertices_degree):
        path_to_graph = gen_scale_free_graph(add_graph_dir('ScaleFree'), vertices_number, vertices_degree)
        return ScaleFree.load_from_rdf(path_to_graph)

    @staticmethod
    def init_cmd_parser(parser):
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

    @staticmethod
    def eval_cmd_parser(args):
        if args.preset is False and \
                (args.vertices_number is None or args.vertices_degree is None):
            print("One of -p/--preset, (-n/--vertices_number and necessarily -k/--vertices_degree) required")
            exit()

        if args.preset is True:
            for n, k in tqdm(SCALEFREE_GRAPH_TO_GEN, desc='ScaleFree graphs generation'):
                ScaleFree.build(n, k).save_metadata()

        if args.vertices_number is not None and args.vertices_degree is not None:
            graph = ScaleFree.build(args.vertices_number, args.vertices_degree)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_scale_free_graph(target_dir, n, k, labels=('A', 'B', 'C', 'D')):
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

    output_graph = rdflib.Graph()

    edges = list()

    for v in g:
        for to in g[v]:
            edges.append((v, to[1], to[0]))

    for subj, pred, obj in tqdm(edges, desc=f'scale_free_graph_{n}_{k} generation'):
        add_rdf_edge(subj, pred, obj, output_graph)

    target = target_dir / f'scale_free_graph_{n}_{k}.xml'

    write_to_rdf(target, output_graph)

    return target
