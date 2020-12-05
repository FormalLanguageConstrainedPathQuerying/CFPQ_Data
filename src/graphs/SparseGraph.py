import networkx as nx
from rdflib import Graph
from tqdm import tqdm

from src.tools.base import Tool
from src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from src.utils import *

SPARSE_GRAPH_TO_GEN = [
    [5000, 0.001]
    , [10000, 0.001]
    , [10000, 0.01]
    , [10000, 0.1]
    , [20000, 0.001]
    , [40000, 0.001]
    , [80000, 0.001]
]


class SparseGraph(Tool):
    def init_parser(self, parser):
        parser.add_argument(
            '-p'
            , '--preset'
            , action='store_true'
            , help='Load preset SparseGraph graphs from dataset'
        )
        parser.add_argument(
            '-n'
            , '--vertices_number'
            , required=False
            , type=int
            , help='Number of vertices of SparseGraph graph'
        )
        parser.add_argument(
            '-pr'
            , '--edge_probability'
            , required=False
            , type=float
            , help='Probability of edge occurrence in graph'
        )

    def eval(self, args):
        if args.preset is False and \
                (args.vertices_number is None or args.edge_probability is None):
            print("One of -p/--preset, (-n/--vertices_number and necessarily -с/--edge_probability) required")
            exit()

        graphs_dir = add_graph_dir('SparseGraph')

        if args.preset is True:
            for g in tqdm(SPARSE_GRAPH_TO_GEN, desc='Sparse graphs generation'):
                gen_sparse_graph(graphs_dir, g[0], g[1])

        if args.vertices_number is not None and args.edge_probability is not None:
            graph = gen_sparse_graph(graphs_dir, args.vertices_number, args.edge_probability)
            print(f'Generated {graph}')


def gen_sparse_graph(target_dir, vertices, prob):
    tmp_graph = nx.generators.fast_gnp_random_graph(vertices, prob)

    output_graph = Graph()

    for v, to in tmp_graph.edges():
        add_rdf_edge(v, 'A', to, output_graph)
        add_rdf_edge(to, 'AR', v, output_graph)

    target = os.path.join(target_dir, f'G{vertices}-{prob}')

    write_to_rdf(target, output_graph)

    return target
