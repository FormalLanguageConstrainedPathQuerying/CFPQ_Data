from tqdm import tqdm

from src.tools.base import Tool
from src.utils import *


class RDF(Tool):
    def init_parser(self, parser):
        parser.add_argument(
            '-a'
            , '--all'
            , action='store_true'
            , help='Load all RDF graphs from dataset'
        )
        parser.add_argument(
            '-g'
            , '--graph'
            , choices=list(get_info()['RDF'].keys())
            , required=False
            , type=str
            , help='Load specific RDF graph from dataset'
        )

    def eval(self, args):
        if args.all is False and args.graph is None:
            print('One of -a/--all, -g/--graph required')
            exit()

        graphs = get_info()['RDF']

        if args.all is True:
            clean_dir('RDF')
            for graph_name in tqdm(graphs, desc='Downloading RDF'):
                download_data('RDF', graph_name, graphs[graph_name])
                unpack_graph('RDF', graph_name)

        if args.graph is not None:
            path = download_data('RDF', args.graph, graphs[args.graph])
            unpack_graph('RDF', args.graph)
            print(f'Loaded {args.graph} to {path}')
