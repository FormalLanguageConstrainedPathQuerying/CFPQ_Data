from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple, Union, Optional

import rdflib
from tqdm import tqdm

from cfpq_data.src.graphs.rdf_graph import RDF
from cfpq_data.src.utils.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils.utils import add_graph_dir

FULL_GRAPH_TO_GEN = [
    10, 50, 100, 200, 500,
    1000, 2000, 5000, 10000, 25000, 50000, 80000
]


class FullGraph(RDF):
    """
    FullGraph — cycle graph, all edges are labeled with the same token

    - graphs: already built graphs
    """

    graphs: Dict[Tuple[str, str], Path] = dict()

    @classmethod
    def build(cls,
              *args: Union[Path, str, int],
              source_file_format: str = 'rdf',
              config: Optional[Dict[str, str]] = None) -> FullGraph:
        """
        Builds FullGraph instance by number of vertices in the graph

        :param args: args[0] - number of vertices in the graph
        :type args: int
        :param source_file_format: graph format ('txt'/'rdf')
        :type source_file_format: str
        :param config: edge configuration
        :type config: Optional[Dict[str, str]]
        :return: FullGraph instance
        :rtype: FullGraph
        """

        if isinstance(args[0], int):
            vertices_number = int(args[0])
            path_to_graph = gen_cycle_graph(add_graph_dir('FullGraph'), vertices_number)
            graph = FullGraph.load_from_rdf(path_to_graph)
        else:
            source = args[0]
            if source_file_format == 'txt':
                graph = cls.load_from_txt(source, config)
            else:
                graph = cls.load_from_rdf(source)

        graph.save_metadata()

        cls.graphs[(graph.basename, graph.file_extension)] = graph.path

        return graph


def gen_cycle_graph(destination_folder: Path, vertices_number: int) -> Path:
    """
    Generates one cycle graph with specified number of vertices

    :param destination_folder: directory to save the graph
    :type destination_folder: Path
    :param vertices_number: number of vertices in the graph
    :type vertices_number: int
    :return: path to generated graph
    :rtype: Path
    """

    output_graph = rdflib.Graph()

    edges = list()

    for i in range(0, vertices_number - 1):
        edges.append((i, 'A', i + 1))

    edges.append((vertices_number - 1, 'A', 0))

    for subj, pred, obj in tqdm(edges, desc=f'fullgraph_{vertices_number} generation'):
        add_rdf_edge(subj, pred, obj, output_graph)

    target = destination_folder / f'fullgraph_{vertices_number}.xml'
    write_to_rdf(target, output_graph)

    return target
