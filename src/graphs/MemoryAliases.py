from tqdm import tqdm

from src.tools.base import Tool
from src.utils import *


class MemoryAliases(Tool):
    def init_parser(self, parser):
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

    def eval(self, args):
        if args.all is False and args.graph is None:
            print('One of -a/--all, -g/--graph required')
            exit()

        graphs = get_info()['MemoryAliases']

        if args.all is True:
            clean_dir('MemoryAliases')
            for graph_name in tqdm(graphs, desc='Downloading MemoryAliases'):
                download_data('MemoryAliases', graph_name, graphs[graph_name])
                unpack_graph('MemoryAliases', graph_name)

        if args.graph is not None:
            path = download_data('MemoryAliases', args.graph, graphs[args.graph])
            unpack_graph('MemoryAliases', args.graph)
            print(f'Loaded {args.graph} to {path}')
