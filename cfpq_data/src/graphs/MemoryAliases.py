from tqdm import tqdm

from cfpq_data.config import RELEASE_INFO
from cfpq_data.src.graphs.RDF import RDF
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import *


class MemoryAliases(RDF, CmdParser):
    graphs = dict()
    graph_keys = RELEASE_INFO['MemoryAliases']

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
            , choices=list(RELEASE_INFO['MemoryAliases'].keys())
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
                MemoryAliases.load_from_rdf(graph_name).save_metadata()

        if args.graph is not None:
            graph = MemoryAliases.load_from_rdf(args.graph)
            graph.save_metadata()
            print(f'Loaded {graph.basename} to {graph.dirname}')
