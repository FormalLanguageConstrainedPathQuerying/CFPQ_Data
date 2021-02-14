from argparse import ArgumentParser, Namespace

from tqdm import tqdm

from cfpq_data.config import RELEASE_INFO
from cfpq_data.src.graphs.RDF import RDF
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import clean_dir


class MemoryAliases(RDF, CmdParser):
    """
    MemoryAliases — real-world data for points-to analysis of C code

    - graphs: already builded graphs
    - graph_keys: reserved graph names
    - config: default edge configuration
    """

    graphs = dict()
    graph_keys = RELEASE_INFO['MemoryAliases']
    config = RELEASE_INFO['MemoryAliases_Config']

    @staticmethod
    def init_cmd_parser(parser: ArgumentParser):
        """
        Initializes command line parser

        :param parser: MemoryAliases subparser of command line parser
        :type parser: ArgumentParser
        :return: None
        :rtype: None
        """

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
    def eval_cmd_parser(args: Namespace):
        """
        Evaluates command line parser

        :param args: command line arguments
        :type args: Namespace
        :return: None
        :rtype: None
        """

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
