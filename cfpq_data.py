import argparse

from src.graphs.FullGraph import FullGraph
from src.graphs.MemoryAliases import MemoryAliases
from src.graphs.RDF import RDF
from src.graphs.ScaleFree import ScaleFree
from src.graphs.SparseGraph import SparseGraph
from src.graphs.WorstCase import WorstCase
from src.tools.LUBM.converter import LUBMGraph
from src.tools.gen_RPQ.gen import GenRPQGraph
from src.tools.grammar2cnf.grammar2cnf import Grammar2Cnf
from src.tools.graph2txt.graph2txt import Graph2TxtGraph
from src.tools.redis_rdf.main import RedisRDFGraph

if __name__ == '__main__':
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
