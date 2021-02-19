from __future__ import annotations

import os
import shutil
import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict, Tuple, Union

import rdflib
import wget
from tqdm import tqdm

from cfpq_data.config import RELEASE_INFO, MAIN_FOLDER
from cfpq_data.src.graphs.rdf_graph import RDF
from cfpq_data.src.utils.cmd_parser_interface import ICmdParser
from cfpq_data.src.utils.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils.utils import add_graph_dir

LUBM_URL = 'http://swat.cse.lehigh.edu/projects/lubm/uba1.7.zip'
MAX_FILES_PER_UNI = 30


class LUBM(RDF, ICmdParser):
    """
    LUBM - Lehigh University Benchmark graph

    - graphs: already built graphs
    """

    graphs: Dict[Tuple[str, str], Path] = dict()
    config = RELEASE_INFO['LUBM_Config']

    @classmethod
    def build(cls, *args: Union[int, Tuple[int, int]]) -> LUBM:
        """
        Builds LUBM instance by number of generated graphs to create one LUBM graph

        :param args: args[0] - number of generated graphs, args[1] (optional) - edges configuration
        :type args: Union[int, Tuple[int, int]]
        :return: LUBM instance
        :rtype: LUBM
        """

        count = int(args[0])

        replace = RELEASE_INFO['LUBM_Config']
        if len(args) > 1:
            config = args[1]
            for edge_config in open(config, 'r').readlines():
                pair = edge_config.split(' ')
                old = rdflib.URIRef(pair[0].strip(' '))
                new = pair[1].strip('\n').strip(' ')
                replace[old] = new

        path_to_graph = gen_lubm_graph(add_graph_dir('LUBM'), count, replace)

        graph = LUBM.load_from_rdf(path_to_graph)

        graph.save_metadata()

        return graph

    @staticmethod
    def init_cmd_parser(parser: ArgumentParser) -> None:
        """
        Initializes command line parser

        :param parser: LUBM subparser of command line parser
        :type parser: ArgumentParser
        :return: None
        :rtype: None
        """

        parser.add_argument(
            '-n',
            '--number',
            required=True,
            type=int,
            help='Number of generated graphs to create LUBM graph'
        )

        parser.add_argument(
            '-c',
            '--config',
            required=False,
            type=str,
            help='Path to configuration file'
        )

    @staticmethod
    def eval_cmd_parser(args: Namespace) -> None:
        """
        Evaluates command line parser

        :param args: command line arguments
        :type args: Namespace
        :return: None
        :rtype: None
        """

        if args.config is not None:
            graph = LUBM.build(args.count, args.config)
        else:
            graph = LUBM.build(args.count)
        graph.save_metadata()
        print(f'Generated {graph.basename} to {graph.dirname}')


def gen_lubm_graph(destination_folder: Path,
                   count: int,
                   config: Dict[str, str]) -> Path:
    """
    Generates LUBM graph by specified number of generated graphs to create one LUBM graph

    :param destination_folder: directory to save the graph
    :type destination_folder: Path
    :param count: number of generated graphs
    :type count: int
    :param config: edges configuration
    :type config: Dict[str, str]
    :return: path to generated graph
    :rtype: Path
    """

    arch = MAIN_FOLDER / 'data' / 'LUBM' / 'uba.zip'
    univ_dir = MAIN_FOLDER / 'data' / 'LUBM' / 'univ'
    if not os.path.exists(univ_dir):
        wget.download(url=LUBM_URL, out=str(arch))
        shutil.unpack_archive(filename=str(arch), extract_dir=str(univ_dir))
        os.remove(arch)
    subprocess.run(
        'java ' +
        '-cp ' +
        'classes ' +
        'edu.lehigh.swat.bench.uba.Generator ' +
        '-univ ' +
        f'{count} ' +
        '-onto ' +
        'http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl',
        cwd=str(univ_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        shell=True
    )

    output_graph = rdflib.Graph()

    triples = list()

    vertices = dict()
    next_id = 0

    generated_graphs = \
        os.listdir(MAIN_FOLDER / 'data' / 'LUBM') + \
        os.listdir(univ_dir)  # for Windows

    for tmp_graph_path in generated_graphs:
        if 'University' not in tmp_graph_path:
            continue

        tmp_graph_path = f"{MAIN_FOLDER / 'data' / 'LUBM'}/{tmp_graph_path}"
        tmp_graph = rdflib.Graph()
        tmp_graph.parse(tmp_graph_path)

        for subj, pred, obj in tmp_graph:
            for tmp in [subj, obj]:
                if tmp not in vertices:
                    vertices[tmp] = next_id
                    next_id += 1
            if pred in config:
                triples.append((vertices[subj], pred, vertices[obj]))
            else:
                triples.append((vertices[subj], 'default', vertices[obj]))

        os.remove(tmp_graph_path)

    for subj, pred, obj in tqdm(triples, desc=f'lubm_{count} generation'):
        add_rdf_edge(subj, pred, obj, output_graph, config=config, reverse=True)

    target = destination_folder / f'lubm_{count}.xml'

    write_to_rdf(target, output_graph)

    return target
