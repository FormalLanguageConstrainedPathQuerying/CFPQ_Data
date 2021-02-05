import networkx as nx
import rdflib
from tqdm import tqdm

from src.graphs.Graph import Graph
from src.tools.CmdParser import CmdParser
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


class SparseGraph(Graph, CmdParser):
    graphs = {}

    def __init__(self, vertices_number, edge_probability):
        self.dirname = add_graph_dir('SparseGraph')
        self.basename = f'G{vertices_number}-{edge_probability}'

        path_to_graph = gen_sparse_graph(self.dirname, vertices_number, edge_probability)

        self.graph = rdflib.Graph()
        self.graph.load(path_to_graph)

        self.vertices_number = len(self.graph.all_nodes())
        self.number_of_edges = len(self.graph)

        self.file_size = os.path.getsize(path_to_graph)
        self.file_name, self.file_extension = os.path.splitext(self.basename)

        SparseGraph.graphs[self.basename] = path_to_graph

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
                SparseGraph(g[0], g[1]).save_metadata()

        if args.vertices_number is not None and args.edge_probability is not None:
            graph = SparseGraph(args.vertices_number, args.edge_probability)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_sparse_graph(target_dir, vertices_number, edge_probability):
    tmp_graph = nx.generators.fast_gnp_random_graph(vertices_number, edge_probability)

    output_graph = Graph()

    for v, to in tmp_graph.edges():
        add_rdf_edge(v, 'A', to, output_graph)
        add_rdf_edge(to, 'AR', v, output_graph)

    target = os.path.join(target_dir, f'G{vertices_number}-{edge_probability}')

    write_to_rdf(target, output_graph)

    return f'{target}.xml'
