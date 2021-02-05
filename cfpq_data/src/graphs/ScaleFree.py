from itertools import product

import numpy as np
import rdflib
from tqdm import tqdm

from cfpq_data.src.graphs.Graph import Graph
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils import *

SCALEFREE_GRAPH_TO_GEN = list(product(
    [100, 500, 2500, 10000]
    , [1, 3, 5, 10]
))


class ScaleFree(Graph, CmdParser):
    graphs = {}

    def __init__(self, vertices_number, vertices_degree):
        self.dirname = add_graph_dir('ScaleFree')
        self.basename = f'scale_free_graph_{vertices_number}_{vertices_degree}.xml'

        path_to_graph = gen_scale_free_graph(self.dirname, vertices_number, vertices_degree)

        self.graph = rdflib.Graph()
        self.graph.load(path_to_graph)

        self.vertices_number = len(self.graph.all_nodes())
        self.number_of_edges = len(self.graph)

        self.file_size = os.path.getsize(path_to_graph)
        self.file_name, self.file_extension = os.path.splitext(self.basename)

        ScaleFree.graphs[self.basename] = path_to_graph

    def get_metadata(self):
        return {
            'name': self.basename
            , 'path': self.dirname
            , 'version': get_info()['version']
            , 'vertices': self.vertices_number
            , 'edges': self.number_of_edges
            , 'size of file': self.file_size
        }

    def save_metadata(self):
        with open(f'{self.dirname}/{self.file_name}_meta.json', 'w') as metadata_file:
            json.dump(self.get_metadata(), metadata_file, indent=4)

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
                ScaleFree(n, k).save_metadata()

        if args.vertices_number is not None and args.vertices_degree is not None:
            graph = ScaleFree(args.vertices_number, args.vertices_degree)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_scale_free_graph(target_dir, n, k, labels=('a', 'b', 'c', 'd')):
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

    return f'{target}.xml'
