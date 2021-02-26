from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional, Tuple, Any, List, Dict, Union

import rdflib

from cfpq_data.config import RELEASE_INFO, MAIN_FOLDER
from cfpq_data.src.graphs.graph_interface import IGraph
from cfpq_data.src.utils.rdf_graphs_downloader import download_data
from cfpq_data.src.utils.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils.utils import unpack_graph


class RDF(IGraph):
    """
    RDF — fixed versions of real-world RDF files (links are provided for updating purposes only!)

    - graphs: already built graphs
    - graph_keys: reserved graph names
    - config: default edge configuration
    """

    graphs: Dict[Tuple[str, str], Path] = dict()
    graph_keys: Dict[str, str] = RELEASE_INFO['RDF']

    def __init__(self):
        """
        Generic constructor

        - type: type of graph instance
        - store: stored rdflib graph
        - path: absolute path to graph
        - dirname: absolute path to graph directory
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
        self.dirname: Optional[Path] = None
        self.basename: Optional[str] = None

        self.vertices_number: Optional[int] = None
        self.edges_number: Optional[int] = None

        self.file_size: Optional[int] = None
        self.file_name: Optional[str] = None
        self.file_extension: Optional[str] = None

    @classmethod
    def build(cls,
              *args: Union[Path, str],
              source_file_format: str = 'rdf',
              config: Optional[Dict[str, str]] = None) -> RDF:
        """
        An RDF graph builder

        :param args: args[0] - path to graph or reserved graph name, args[1] (optional) - graph file extension
        :type args: Union[Path, str]
        :param source_file_format: graph format ('txt'/'rdf')
        :type source_file_format: str
        :param config: edge configuration
        :type config: Optional[Dict[str, str]]
        :return: RDF graph instance
        :rtype: RDF
        """

        source = args[0]

        if source_file_format == 'txt':
            graph = cls.load_from_txt(source, config)
        else:
            graph = cls.load_from_rdf(source)

        graph.save_metadata()

        cls.graphs[(graph.basename, graph.file_extension)] = graph.path

        return graph

    @classmethod
    def load(cls,
             source: Union[Path, str],
             source_file_format: str = 'rdf',
             config: Optional[Dict[str, str]] = None) -> RDF:
        """
        Loads RDF graph from specified source with specified source_file_format

        :param source: graph source
        :type source: Optional[Union[Path, str]]
        :param source_file_format: graph format ('txt'/'rdf')
        :type source_file_format: str
        :param config: edge configuration
        :type config: Optional[Dict[str, str]]
        :return: loaded graph
        :rtype: RDF
        """

        if source_file_format == 'txt':
            rdf_graph = cls.load_from_txt(source, config)
        else:
            rdf_graph = cls.load_from_rdf(source)

        return rdf_graph

    def save(self,
             destination: Union[Path, str],
             destination_file_format: str = 'rdf',
             config: Optional[Dict[str, str]] = None) -> Path:
        """
        Saves RDF graph to destination with specified destination_file_format and edge configuration

        :param destination: path to save the graph
        :type destination: Optional[Union[Path, str]]
        :param destination_file_format: graph format
        :type destination_file_format: str
        :param config: edges configuration
        :type config: Optional[Dict[str, str]]
        :return: path to saved graph
        :rtype: Path
        """

        if destination is None:
            destination = MAIN_FOLDER / 'data' / self.type / 'Graphs' / self.basename

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
            'name': str(self.basename),
            'path': str(self.path),
            'version': RELEASE_INFO['version'],
            'vertices': self.vertices_number,
            'edges': self.edges_number,
            'size of file': self.file_size
        }

    def save_metadata(self) -> Path:
        """
        Saves metadata to specified file

        :return: path to file with graph metadata
        :rtype: Path
        """

        metadata_file_path = self.dirname / f'{self.file_name}_meta.json'

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
    def load_from_rdf(cls, source: Path = None) -> RDF:
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

        graph.path = Path(source)
        graph.dirname = Path(os.path.dirname(source))
        graph.basename = os.path.basename(source)

        graph.vertices_number = len(graph.store.all_nodes())
        graph.edges_number = len(graph.store)

        graph.file_size = os.path.getsize(source)
        graph.file_name, graph.file_extension = os.path.splitext(graph.basename)

        return graph

    @classmethod
    def load_from_txt(cls,
                      source: Path = None,
                      config: Optional[Dict[str, str]] = None) -> RDF:
        """
        Loads RDF graph from specified source with txt format

        :param source: graph source
        :type source: Path
        :param config: edge configuration
        :type config: Optional[Dict[str, str]]
        :return: loaded graph
        :rtype: RDF
        """

        tmp_graph = rdflib.Graph()

        if config is None:
            config = dict()

            with open(source, 'r') as input_file:
                for edge in input_file:
                    s, p, o = edge.strip('\n').split(' ')
                    p_text = p
                    if not p.startswith('http'):
                        p_text = f'http://yacc/rdf-schema#{p_text}'
                    config[p] = p_text

        with open(source, 'r') as input_file:
            for edge in input_file:
                s, p, o = edge.strip('\n').split(' ')
                add_rdf_edge(s, config[p], o, tmp_graph)

        write_to_rdf(Path('tmp.xml'), tmp_graph)

        graph = cls.load_from_rdf(Path('tmp.xml'))

        # os.remove('tmp.xml')

        return graph

    def save_to_rdf(self, destination: Path) -> Path:
        """
        Saves RDF graph to destination rdf file

        :param destination: path to save the graph
        :type destination: Path
        :return: path to saved graph
        :rtype: Path
        """

        write_to_rdf(destination, self.store)
        return destination

    def save_to_txt(self,
                    destination: Path,
                    config: Optional[Dict[str, str]] = None) -> Path:
        """
        Saves RDF graph to destination txt file with specified edge configuration

        :param destination: path to save the graph
        :type destination: Path
        :param config: edges configuration
        :type config: Optional[Dict[str, str]]
        :return: path to saved graph
        :rtype: Path
        """

        vertices = dict()
        edges = dict()
        next_id = 0
        triples = list()

        if config is None:
            config = dict()

            for subj, pred, obj in self.store:
                p_text = str(pred)
                config[p_text] = p_text

        for subj, pred, obj in self.store:
            for tmp in [subj, obj]:
                if tmp not in vertices:
                    vertices[tmp] = next_id
                    next_id += 1

            p_text = str(pred)
            if p_text in config:
                edges[p_text] = config[p_text]
            else:
                edges[p_text] = 'other'

            triples.append((vertices[subj], edges[str(pred)], vertices[obj]))

        with open(destination, 'w') as output_file:
            for s, p, o in triples:
                output_file.write(f'{s} {p} {o}\n')

        return destination
