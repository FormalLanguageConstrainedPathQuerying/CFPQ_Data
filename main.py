#!/usr/bin/python3

from src.tools.init.init import InitTool
from src.tools.graph2txt.graph2txt import Graph2TxtTool
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tool', required=True)

    tools = {
        'init': InitTool(),
        'graph2txt': Graph2TxtTool(),
        # all tools will be here
    }
    for name, tool in tools.items():
        subparser = subparsers.add_parser(name)
        tool.init_parser(subparser)

    args = parser.parse_args()
    tools[args.tool].eval(args)

