import argparse
import configparser

import rdflib
from tqdm import tqdm

from cfpq_data_devtools.data_wrapper import *
from src.tools.base import Tool

GRAPH2TXT_PATH = 'src/tools/graph2txt'
CONVERTER_CONF_PATH = os.path.join(GRAPH2TXT_PATH, 'converter.conf')
DEFAULT_SECTION = 'DEFAULT'


def convert(path, replace=None, reverse_edges=False):
    res = {}
    next_id = 0

    graph_from = rdflib.Graph()
    graph_from.parse(path)

    graph_to = f'{os.path.splitext(path)[0]}.txt'

    with open(graph_to, 'w') as out:
        for s, p, o in tqdm(graph_from, desc=f'Converting {graph_from} to {graph_to}'):
            for r in [s, o]:
                if r not in res:
                    res[r] = str(next_id)
                    next_id += 1

            v, e, to = res[s], p, res[o]
            if replace:
                if e in replace:
                    e = replace[p]
                    if reverse_edges:
                        out.write(f'{to} {e}_R {v}\n')
                else:
                    e = 'OTHER'

            out.write(f'{v} {e} {to}\n')


class Graph2TxtTool(Tool):
    def init_parser(self, parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(required=True, dest='mode')
        file_parser = subparsers.add_parser('file')
        set_parser = subparsers.add_parser('set')

        file_parser.add_argument('path')
        file_parser.add_argument('--conf')

        set_parser.add_argument('suite', nargs='*', choices=DataWrapper().get_suites())

    def eval(self, args: argparse.Namespace):
        config = configparser.ConfigParser(delimiters=('=',))

        if args.mode == 'set':
            data = DataWrapper()
            config.read(CONVERTER_CONF_PATH)
            for suite in args.suite:
                replacing = config[suite]
                for graph in data.get_graphs(suite, exclude_extensions=['txt'], max_file_size=1000):
                    convert(graph, replace=replacing, reverse_edges=True)
        elif args.mode == 'file':
            if args.conf:
                config.read(args.conf)
                replacing = config[DEFAULT_SECTION]
            else:
                replacing = None
            convert(args.path, replace=replacing, reverse_edges=True)
