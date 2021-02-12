import networkx as nx

from cfpq_data.src.graphs.RDF import RDF
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils import *

SPARSE_GRAPH_TO_GEN = [
    [5000, 0.001]
    , [10000, 0.001]
    , [10000, 0.01]
    , [10000, 0.1]
    , [20000, 0.001]
    , [40000, 0.001]
    , [80000, 0.001]
]


class SparseGraph(RDF, CmdParser):
    graphs = {}

    @classmethod
    def build(cls, vertices_number, edge_probability):
        path_to_graph = gen_sparse_graph(add_graph_dir('SparseGraph'), vertices_number, edge_probability)
        return SparseGraph.load_from_rdf(path_to_graph)

    @staticmethod
    def init_cmd_parser(parser):
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

    @staticmethod
    def eval_cmd_parser(args):
        if args.preset is False and \
                (args.vertices_number is None or args.edge_probability is None):
            print("One of -p/--preset, (-n/--vertices_number and necessarily -с/--edge_probability) required")
            exit()

        if args.preset is True:
            for g in tqdm(SPARSE_GRAPH_TO_GEN, desc='Sparse graphs generation'):
                SparseGraph.build(g[0], g[1]).save_metadata()

        if args.vertices_number is not None and args.edge_probability is not None:
            graph = SparseGraph.build(args.vertices_number, args.edge_probability)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_sparse_graph(target_dir, vertices_number, edge_probability):
    tmp_graph = nx.generators.fast_gnp_random_graph(vertices_number, edge_probability)

    output_graph = rdflib.Graph()

    edges = list()

    for v, to in tmp_graph.edges():
        edges.append((v, 'A', to))
        edges.append((v, 'AR', to))

    for subj, pred, obj in tqdm(edges, desc=f'G{vertices_number}-{edge_probability} generation'):
        add_rdf_edge(subj, pred, obj, output_graph)

    target = target_dir / f'G{vertices_number}-{edge_probability}.xml'

    write_to_rdf(target, output_graph)

    return target
