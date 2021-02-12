import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

import rdflib
from tqdm import tqdm

from cfpq_data.src.graphs.RDF import RDF
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import add_graph_dir, add_rdf_edge, write_to_rdf

FULL_GRAPH_TO_GEN = [
    10
    , 50
    , 100
    , 200
    , 500
    , 1000
    , 2000
    , 5000
    , 10000
    , 25000
    , 50000
    , 80000
]


class FullGraph(RDF, CmdParser):
    """
    FullGraph — cycle graph, all edges are labeled with the same token.
    """

    graphs = {}

    @classmethod
    def build(cls, *args: int):
        """
        Build FullGraph instance by number of vertices in the graph
        :param args: only one argument - args[0] - number of vertices in the graph
        :type args: int
        :return: FullGraph instance
        :rtype: FullGraph
        """

        vertices_number = args[0]
        path_to_graph = gen_cycle_graph(add_graph_dir('FullGraph'), vertices_number)
        return FullGraph.load_from_rdf(path_to_graph)

    @staticmethod
    def init_cmd_parser(parser: ArgumentParser):
        """
        Initialize command line parser
        :param parser: FullGraph subparser of command line parser
        :type parser: ArgumentParser
        :return: None
        :rtype: None
        """

        parser.add_argument(
            '-p'
            , '--preset'
            , action='store_true'
            , help='Load preset FullGraph graphs from dataset'
        )
        parser.add_argument(
            '-n'
            , '--vertices_number'
            , required=False
            , type=int
            , help='Number of vertices of FullGraph graph'
        )

    @staticmethod
    def eval_cmd_parser(args: Namespace):
        """
        Evaluate command line parser
        :param args: Command line arguments
        :type args: Namespace
        :return: None
        :rtype: None
        """

        if args.preset is False and args.vertices_number is None:
            print("One of -p/--preset, -n/--vertices_number required")
            sys.exit()

        if args.preset is True:
            for n in tqdm(FULL_GRAPH_TO_GEN, desc='Full graphs generation'):
                FullGraph.build(n).save_metadata()

        if args.vertices_number is not None:
            graph = FullGraph.build(args.vertices_number)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_cycle_graph(target_dir: Path, vertices_number: int) -> Path:
    """
    Generates one cycle graph with specified number of vertices
    :param target_dir: Directory to save the graph
    :type target_dir: Path
    :param vertices_number: Number of vertices in the graph
    :type vertices_number: int
    :return: Path to generated graph
    :rtype: Path
    """

    output_graph = rdflib.Graph()

    edges = list()

    for i in range(0, vertices_number - 1):
        edges.append((i, 'A', i + 1))

    edges.append((vertices_number - 1, 'A', 0))

    for subj, pred, obj in tqdm(edges, desc=f'fullgraph_{vertices_number} generation'):
        add_rdf_edge(subj, pred, obj, output_graph)

    target = target_dir / f'fullgraph_{vertices_number}.xml'

    write_to_rdf(target, output_graph)

    return target
