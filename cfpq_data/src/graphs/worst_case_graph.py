from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict, Tuple

import rdflib
from tqdm import tqdm

from cfpq_data.config import RELEASE_INFO
from cfpq_data.src.graphs.rdf_graph import RDF
from cfpq_data.src.utils.cmd_parser_interface import ICmdParser
from cfpq_data.src.utils.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils.utils import add_graph_dir

NUMBER_OF_WORST_CASES = 12


class WorstCase(RDF, ICmdParser):
    """
    WorstCase — graphs with two cycles

    - graphs: already built graphs
    """

    graphs: Dict[Tuple[str, str], Path] = dict()
    config: Dict[str, str] = RELEASE_INFO['Generators_Config']

    @classmethod
    def build(cls, vertices_number: int) -> WorstCase:
        """
        Builds WorstCase graph instance by number of vertices in the graph

        :param vertices_number: number of vertices in the graph
        :type vertices_number: int
        :return: WorstCase graph instance
        :rtype:WorstCase
        """

        path_to_graph = gen_worst_case_graph(add_graph_dir('WorstCase'), vertices_number)

        graph = WorstCase.load_from_rdf(path_to_graph)

        graph.save_metadata()

        return graph

    @staticmethod
    def init_cmd_parser(parser: ArgumentParser) -> None:
        """
        Initialize command line parser

        :param parser: WorstCase subparser of command line parser
        :type parser: ArgumentParser
        :return: None
        :rtype: None
        """

        parser.add_argument(
            '-p',
            '--preset',
            action='store_true',
            help='Load preset WorstCase graphs from dataset'
        )
        parser.add_argument(
            '-n',
            '--vertices_number',
            required=False,
            type=int,
            help='Number of vertices of WorstCase graph'
        )

    @staticmethod
    def eval_cmd_parser(args: Namespace) -> None:
        """
        Evaluate command line parser

        :param args: command line arguments
        :type args: Namespace
        :return: None
        :rtype: None
        """

        if args.preset is False and args.vertices_number is None:
            print("One of -p/--preset, -n/--vertices_number required")
            sys.exit()

        if args.preset is True:
            for n in tqdm(range(2, NUMBER_OF_WORST_CASES), desc='WorstCase graphs generation'):
                WorstCase.build(2 ** n).save_metadata()

        if args.vertices_number is not None:
            graph = WorstCase.build(args.vertices_number)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_worst_case_graph(destination_folder: Path, vertices_number: int) -> Path:
    """
    Generates graphs with two cycles by number of vertices in the graph

    :param destination_folder: directory to save the graph
    :type destination_folder: Path
    :param vertices_number: number of vertices in the graph
    :type vertices_number: int
    :return: path to generated graph
    :rtype: Path
    """

    output_graph = rdflib.Graph()

    first_cycle = int(vertices_number / 2) + 1

    edges = list()

    for i in range(0, first_cycle - 1):
        edges.append((i, 'A', i + 1))

    edges.append((first_cycle - 1, 'A', 0))
    edges.append((first_cycle - 1, 'B', first_cycle))

    for i in range(first_cycle, vertices_number - 1):
        edges.append((i, 'B', i + 1))

    edges.append((vertices_number - 1, 'B', first_cycle - 1))

    for subj, pred, obj in tqdm(edges, desc=f'worstcase_{vertices_number} generation'):
        add_rdf_edge(subj, pred, obj, output_graph)

    target = destination_folder / f'worstcase_{vertices_number}.xml'

    write_to_rdf(target, output_graph)

    return target
