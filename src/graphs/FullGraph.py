import rdflib
from tqdm import tqdm

from src.graphs.Graph import Graph
from src.tools.CmdParser import CmdParser
from src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from src.utils import *

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


class FullGraph(Graph, CmdParser):
    graphs = {}

    def __init__(self, vertices_number):
        self.dirname = add_graph_dir('FullGraph')
        self.basename = f'fullgraph_{vertices_number}.xml'

        path_to_graph = gen_cycle_graph(self.dirname, vertices_number)

        self.graph = rdflib.Graph()
        self.graph.load(path_to_graph)

        self.vertices_number = len(self.graph.all_nodes())
        self.number_of_edges = len(self.graph)

        self.file_size = os.path.getsize(path_to_graph)
        self.file_name, self.file_extension = os.path.splitext(self.basename)

        FullGraph.graphs[self.basename] = path_to_graph

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
            , help='Load preset FullGraph graphs from dataset'
        )
        parser.add_argument(
            '-n'
            , '--vertices_number'
            , required=False
            , type=int
            , help='Number of vertices of FullGraph graph'
        )

    @staticmethod
    def eval_cmd_parser(args):
        if args.preset is False and args.vertices_number is None:
            print("One of -p/--preset, -n/--vertices_number required")
            exit()

        if args.preset is True:
            for n in tqdm(FULL_GRAPH_TO_GEN, desc='Full graphs generation'):
                FullGraph(n).save_metadata()

        if args.vertices_number is not None:
            graph = FullGraph(args.vertices_number)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_cycle_graph(target_dir, vertices_number):
    output_graph = rdflib.Graph()

    for i in range(0, vertices_number - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(vertices_number - 1, 'A', 0, output_graph)

    target = os.path.join(target_dir, f'fullgraph_{vertices_number}')

    write_to_rdf(target, output_graph)

    return f'{target}.xml'
