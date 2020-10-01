#!/usr/bin/python3
from src.tools.init.init import InitTool
from src.tools.grammar2cnf.grammar2cnf import Grammar2Cnf
from src.tools.graph2txt.graph2txt import Graph2TxtTool
from src.tools.LUBM.converter import LUBMTool
from src.tools.gen_RPQ.gen import GenRPQTool
from src.tools.redis_rdf.main import RedisRDFTool
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tool', required=True)

    tools = {
        'init': InitTool(),
        'graph2txt': Graph2TxtTool(),
        'grammar2cnf': Grammar2Cnf(),
        'LUBM': LUBMTool,
        'gen_RPQ': GenRPQTool,
        'redis_rdf': RedisRDFTool,
    }
    for name, tool in tools.items():
        subparser = subparsers.add_parser(name)
        tool.init_parser(subparser)

    args = parser.parse_args()
    tools[args.tool].eval(args)

