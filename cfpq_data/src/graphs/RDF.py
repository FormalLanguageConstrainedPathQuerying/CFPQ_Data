import json
import os
from pathlib import Path
from typing import Optional, Tuple, Any, List, Dict, Union

import rdflib
from tqdm import tqdm

from cfpq_data.config import RELEASE_INFO, DATA_FOLDER
from cfpq_data.src.graphs.GraphInterface import GraphInterface
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import download_data, unpack_graph, add_rdf_edge, write_to_rdf, clean_dir


class RDF(GraphInterface, CmdParser):
    """
    RDF — fixed versions of real-world RDF files (links are provided for updating purposes only!)

    - graphs: already builded graphs
    - graph_keys: reserved graph names
    - config: default edge configuration
    """

    graphs = dict()
    graph_keys = RELEASE_INFO['RDF']
    config = RELEASE_INFO['RDF_Config']

    def __init__(self):
        """
        Generic constructor

        - type: type of graph instance
        - store: stored rdflib graph
        - path: absolute path to graph
        - dirname: absoute path to graph directory
        - basename: graph file
        - vertices_number: number of vertices in the graph
        - edges_number: number of edges in the graph
        - file_size: size of graph file, in bytes
        - file_name: name of graph file
        - file_extension: extension of graph file
        """

        self.type: Optional[str] = None

        self.store: Optional[rdflib.Graph] = None

        self.path: Optional[Path] = None
        self.dirname = None
        self.basename = None

        self.vertices_number = None
        self.edges_number = None

        self.file_size = None
        self.file_name = None
        self.file_extension = None

    @classmethod
    def build(cls, *args: Union[Path, str]):
        """
        An RDF graph builder
        :param args: only one argument - args[0] - path to graph or reserves graph name
        :type args: Union[Path, str]
        :return: RDF graph instance
        :rtype: RDF
        """

        try:
            return cls.load(args[0])
        except BaseException as ex:
            raise BaseException(f'{cls.__name__}.build: {ex}')

    @classmethod
    def load(cls, source: Optional[Union[Path, str]] = None, source_file_format: str = 'rdf'):
        """
        Loads RDF graph from specified source with specified source_file_format
        :param source: graph source
        :type source: Optional[Union[Path, str]]
        :param source_file_format: graph format ('txt'/'rdf')
        :type source_file_format: str
        :return: loaded graph
        :rtype: RDF
        """

        if source_file_format == 'txt':
            rdf_graph = cls.load_from_txt(source)
        else:
            rdf_graph = cls.load_from_rdf(source)

        cls.graphs[(rdf_graph.basename, rdf_graph.file_extension)] = source

        return rdf_graph

    def save(self
             , destination: Optional[Union[Path, str]] = None
             , destination_file_format: str = 'rdf'
             , config: Dict[str, str] = None) -> Path:
        """
        Saves RDF graph to destination with specified destination_file_format and edge configuration
        :param destination: path to save the graph
        :type destination: Optional[Union[Path, str]]
        :param destination_file_format: graph format
        :type destination_file_format: str
        :param config: edges configuration
        :type config: Dict[str, str]
        :return: path to saved graph
        :rtype: Path
        """

        if destination is None:
            destination = DATA_FOLDER / self.type / 'Graphs' / self.basename
        if destination_file_format == 'txt':
            self.save_to_txt(destination, config)
        else:
            self.save_to_rdf(destination)
        return destination

    def get_metadata(self) -> Dict[str, str]:
        """
        Generates RDF graph metadata
        :return: metadata
        :rtype: Dict[str, str]
        """

        return {
            'name': self.basename
            , 'path': self.path
            , 'version': RELEASE_INFO['version']
            , 'vertices': self.vertices_number
            , 'edges': self.edges_number
            , 'size of file': self.file_size
        }

    def save_metadata(self) -> Path:
        """
        Saves metadata to specified file
        :return: path to file with graph metadata
        :rtype: Path
        """

        metadata_file_path = self.dirname / self.file_name + '_meta.json'

        with open(metadata_file_path, 'w') as metadata_file:
            json.dump(self.get_metadata(), metadata_file, indent=4)

        return metadata_file_path

    def get_triples(self) -> List[Tuple[Any, Any, Any]]:
        """
        Returns edges as list of triples (subject, predicate, object)
        :return: edges
        :rtype: List[Tuple[Any, Any, Any]]
        """

        triples = list()

        for subj, pred, obj in self.store:
            triples.append((subj, pred, obj))

        return triples

    @classmethod
    def load_from_rdf(cls, source: Path = None):
        """
        Loads RDF graph from specified source with rdf format
        :param source: graph source
        :type source: Path
        :return: loaded graph
        :rtype: RDF
        """

        if hasattr(cls, 'graph_keys') and source in cls.graph_keys:
            graph_name = source[:]
            download_data(cls.__name__, graph_name, cls.graph_keys[graph_name])
            source = unpack_graph(cls.__name__, graph_name)

        graph = cls()

        graph.type = cls.__name__

        graph.store = rdflib.Graph()
        graph.store.parse(location=str(source), format='xml')

        graph.path = source
        graph.dirname = os.path.dirname(source)
        graph.basename = os.path.basename(source)

        graph.vertices_number = len(graph.store.all_nodes())
        graph.edges_number = len(graph.store)

        graph.file_size = os.path.getsize(source)
        graph.file_name, graph.file_extension = os.path.splitext(graph.basename)

        return graph

    @classmethod
    def load_from_txt(cls, source: Path = None):
        """
        Loads RDF graph from specified source with txt format
        :param source: graph source
        :type source: Path
        :return: loaded graph
        :rtype: RDF
        """

        tmp_graph = rdflib.Graph()

        with open(source, 'r') as input_file:
            for edge in input_file:
                s, p, o = edge.split()
                add_rdf_edge(s, p, o, tmp_graph)

        write_to_rdf('tmp.xml', tmp_graph)

        graph = cls.load_from_rdf(Path('tmp.xml'))

        os.remove('tmp.xml')

        return graph

    def save_to_rdf(self, destination: Path):
        """
        Saves RDF graph to destination rdf file
        :param destination: path to save the graph
        :type destination: Path
        :return: path to saved graph
        :rtype: Path
        """

        write_to_rdf(Path, self.store)
        return destination

    def save_to_txt(self, destination: Path, config: Dict[str, str] = config):
        """
        Saves RDF graph to destination txt file with specified edge configuration
        :param destination: path to save the graph
        :type destination: Path
        :param config: edges configuration
        :type config: Dict[str, str]
        :return: path to saved graph
        :rtype: Path
        """

        vertices = dict()
        edges = dict()
        next_id = 0
        triples = list()

        for subj, pred, obj in self.store:
            if subj not in vertices:
                vertices[subj] = next_id
                next_id += 1
            if obj not in vertices:
                vertices[obj] = next_id
                next_id += 1

            edges[pred] = pred
            if config is not None:
                if pred in config:
                    edges[pred] = config[pred]
                elif 'default' in config:
                    edges[pred] = config['default']

            triples.append((
                vertices[subj]
                , edges[pred]
                , vertices[obj]
            ))

        with open(destination, 'w') as output_file:
            for s, p, o in triples:
                output_file.write(f'{s} {p} {o}\n')

        return destination

    @staticmethod
    def init_cmd_parser(parser):
        """
        Initialize command line parser
        :param parser: RDF subparser of command line parser
        :type parser: ArgumentParser
        :return: None
        :rtype: None
        """

        parser.add_argument(
            '-a'
            , '--all'
            , action='store_true'
            , help='Load all RDF graphs from dataset'
        )
        parser.add_argument(
            '-g'
            , '--graph'
            , choices=list(RELEASE_INFO['RDF'].keys())
            , required=False
            , type=str
            , help='Load specific RDF graph from dataset'
        )

    @staticmethod
    def eval_cmd_parser(args):
        """
        Evaluate command line parser
        :param args: command line arguments
        :type args: Namespace
        :return: None
        :rtype: None
        """

        if args.all is False and args.graph is None:
            print('One of -a/--all, -g/--graph required')
            exit()

        if args.all is True:
            clean_dir('RDF')
            for graph_name in tqdm(RDF.graph_keys, desc='Downloading RDF'):
                RDF.load_from_rdf(graph_name).save_metadata()

        if args.graph is not None:
            graph = RDF.load_from_rdf(args.graph)
            graph.save_metadata()
            print(f'Loaded {graph.basename} to {graph.dirname}')
