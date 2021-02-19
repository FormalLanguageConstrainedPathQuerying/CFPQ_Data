import argparse

from cfpq_data.src.graphs.full_graph import FullGraph
from cfpq_data.src.graphs.lubm_graph import LUBM
from cfpq_data.src.graphs.memory_aliases_graph import MemoryAliases
from cfpq_data.src.graphs.rdf_graph import RDF
from cfpq_data.src.graphs.scale_free_graph import ScaleFree
from cfpq_data.src.graphs.sparse_graph import SparseGraph
from cfpq_data.src.graphs.worst_case_graph import WorstCase


def cmd_parser() -> None:
    """
    Command line utility for loading graphs

    :return: None
    :rtype: None
    """

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tool', required=True)

    tools = {
        'RDF': RDF
        , 'MemoryAliases': MemoryAliases
        , 'ScaleFree': ScaleFree
        , 'FullGraph': FullGraph
        , 'WorstCase': WorstCase
        , 'SparseGraph': SparseGraph
        , 'LUBM': LUBM
    }

    for name, tool in tools.items():
        subparser = subparsers.add_parser(name)
        tool.init_cmd_parser(subparser)

    args = parser.parse_args()
    tools[args.tool].eval_cmd_parser(args)


if __name__ == '__main__':
    cmd_parser()
