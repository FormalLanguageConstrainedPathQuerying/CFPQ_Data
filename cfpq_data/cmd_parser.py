import argparse

from cfpq_data.src.graphs.FullGraph import FullGraph
from cfpq_data.src.graphs.MemoryAliases import MemoryAliases
from cfpq_data.src.graphs.RDF import RDF
from cfpq_data.src.graphs.ScaleFree import ScaleFree
from cfpq_data.src.graphs.SparseGraph import SparseGraph
from cfpq_data.src.graphs.WorstCase import WorstCase
from cfpq_data.src.tools.LUBM.converter import LUBMGraph
from cfpq_data.src.tools.gen_RPQ.gen import GenRPQGraph
from cfpq_data.src.tools.grammar2cnf.grammar2cnf import Grammar2Cnf
from cfpq_data.src.tools.graph2txt.graph2txt import Graph2TxtGraph
from cfpq_data.src.tools.redis_rdf.main import RedisRDFGraph


def cmd_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tool', required=True)

    tools = {
        'RDF': RDF
        , 'MemoryAliases': MemoryAliases
        , 'ScaleFree': ScaleFree
        , 'FullGraph': FullGraph
        , 'WorstCase': WorstCase
        , 'SparseGraph': SparseGraph
        , 'LUBM': LUBMGraph
        , 'graph2txt': Graph2TxtGraph
        , 'grammar2cnf': Grammar2Cnf
        , 'gen_RPQ': GenRPQGraph
        , 'redis_rdf': RedisRDFGraph
    }

    for name, tool in tools.items():
        subparser = subparsers.add_parser(name)
        tool.init_cmd_parser(subparser)

    args = parser.parse_args()
    tools[args.tool].eval_cmd_parser(args)


if __name__ == '__main__':
    cmd_parser()