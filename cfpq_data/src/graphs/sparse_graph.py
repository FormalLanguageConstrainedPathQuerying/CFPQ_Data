from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple, Union, Optional

import networkx as nx
import rdflib
from tqdm import tqdm

from cfpq_data.src.graphs.rdf_graph import RDF
from cfpq_data.src.utils.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils.utils import add_graph_dir

SPARSE_GRAPH_TO_GEN = [
    [5000, 0.001],
    [10000, 0.001],
    [10000, 0.01],
    [10000, 0.1],
    [20000, 0.001],
    [40000, 0.001],
    [80000, 0.001]
]


class SparseGraph(RDF):
    """
    SparseGraph — graphs generated with NetworkX to emulate sparse data

    - graphs: already built graphs
    """

    graphs: Dict[Tuple[str, str], Path] = dict()

    @classmethod
    def build(cls,
              *args: Union[Path, str, int],
              source_file_format: str = 'rdf',
              config: Optional[Dict[str, str]] = None) -> SparseGraph:
        """
        Build SparseGraph instance by number of vertices in probability of edge existence

        - args[0] - number of vertices in the graph
        - args[1] - probability of edge existence in the graph

        :param args: arguments
        :type args: int
        :param source_file_format: graph format ('txt'/'rdf')
        :type source_file_format: str
        :param config: edge configuration
        :type config: Optional[Dict[str, str]]
        :return: SparseGraph instance
        :rtype: SparseGraph
        """

        if len(args) > 1:
            vertices_number = args[0]
            edge_probability = args[1]

            path_to_graph = gen_sparse_graph(add_graph_dir('SparseGraph'),
                                             vertices_number,
                                             edge_probability
                                             )

            graph = SparseGraph.load_from_rdf(path_to_graph)
        else:
            source = args[0]
            if source_file_format == 'txt':
                graph = cls.load_from_txt(source, config)
            else:
                graph = cls.load_from_rdf(source)

        graph.save_metadata()

        cls.graphs[(graph.basename, graph.file_extension)] = graph.path

        return graph


def gen_sparse_graph(destination_folder: Path,
                     vertices_number: int,
                     edge_probability: float) -> Path:
    """
    Generates sparse graph

    :param destination_folder: directory to save the graph
    :type destination_folder: Path
    :param vertices_number: number of vertices in the graph
    :type vertices_number: int
    :param edge_probability: probability of edge existence in the graph
    :type edge_probability: float
    :return: path to generated graph
    :rtype: Path
    """

    tmp_graph = nx.generators.fast_gnp_random_graph(vertices_number, edge_probability)

    output_graph = rdflib.Graph()

    edges = list()

    for v, to in tmp_graph.edges():
        edges.append((v, 'A', to))
        edges.append((v, 'AR', to))

    for subj, pred, obj in tqdm(
            edges,
            desc=f'G{vertices_number}-{edge_probability} generation'
    ):
        add_rdf_edge(subj, pred, obj, output_graph)

    target = destination_folder / f'G{vertices_number}-{edge_probability}.xml'

    write_to_rdf(target, output_graph)

    return target
