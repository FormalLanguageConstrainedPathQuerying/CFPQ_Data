import rdflib
from tqdm import tqdm

from cfpq_data.src.graphs.Graph import Graph
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import *


class MemoryAliases(Graph, CmdParser):
    graphs = dict()
    graph_keys = get_info()['MemoryAliases']

    def __init__(self, graph_name):
        download_data('MemoryAliases', graph_name, MemoryAliases.graph_keys[graph_name])
        path_to_graph = unpack_graph('MemoryAliases', graph_name)

        self.graph = rdflib.Graph()
        self.graph.load(path_to_graph)

        self.dirname = os.path.dirname(path_to_graph)
        self.basename = os.path.basename(path_to_graph)

        self.number_of_vertices = len(self.graph.all_nodes())
        self.number_of_edges = len(self.graph)

        self.file_size = os.path.getsize(path_to_graph)
        self.file_name, self.file_extension = os.path.splitext(self.basename)

        MemoryAliases.graphs[self.basename] = path_to_graph

    def get_metadata(self):
        return {
            'name': self.basename
            , 'path': self.dirname
            , 'version': get_info()['version']
            , 'vertices': self.number_of_vertices
            , 'edges': self.number_of_edges
            , 'size of file': self.file_size
        }

    def save_metadata(self):
        with open(f'{self.dirname}/{self.file_name}_meta.json', 'w') as metadata_file:
            json.dump(self.get_metadata(), metadata_file, indent=4)

    @staticmethod
    def init_cmd_parser(parser):
        parser.add_argument(
            '-a'
            , '--all'
            , action='store_true'
            , help='Load all MemoryAliases graphs from dataset'
        )
        parser.add_argument(
            '-g'
            , '--graph'
            , choices=list(get_info()['MemoryAliases'].keys())
            , required=False
            , type=str
            , help='Load specific MemoryAliases graph from dataset'
        )

    @staticmethod
    def eval_cmd_parser(args):
        if args.all is False and args.graph is None:
            print('One of -a/--all, -g/--graph required')
            exit()

        if args.all is True:
            clean_dir('MemoryAliases')
            for graph_name in tqdm(MemoryAliases.graph_keys, desc='Downloading MemoryAliases'):
                MemoryAliases(graph_name).save_metadata()

        if args.graph is not None:
            graph = MemoryAliases(args.graph)
            graph.save_metadata()
            print(f'Loaded {graph.basename} to {graph.dirname}')
