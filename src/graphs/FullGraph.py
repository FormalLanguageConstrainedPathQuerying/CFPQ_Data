from rdflib import Graph
from tqdm import tqdm

from src.tools.base import Tool
from src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from src.utils import *

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


class FullGraph(Tool):
    def init_parser(self, parser):
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

    def eval(self, args):
        if args.preset is False and args.vertices_number is None:
            print("One of -p/--preset, -n/--vertices_number required")
            exit()

        graphs_dir = add_graph_dir('FullGraph')

        if args.preset is True:
            for n in tqdm(FULL_GRAPH_TO_GEN, desc='Full graphs generation'):
                gen_cycle_graph(graphs_dir, n)

        if args.vertices_number is not None:
            graph = gen_cycle_graph(graphs_dir, args.vertices_number)
            print(f'Generated {graph}')


def gen_cycle_graph(target_dir, vertices):
    output_graph = Graph()

    for i in range(0, vertices - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(vertices - 1, 'A', 0, output_graph)

    target = os.path.join(target_dir, f'fullgraph_{vertices}')

    write_to_rdf(target, output_graph)

    return target
