from rdflib import Graph
from tqdm import tqdm

from src.tools.base import Tool
from src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from src.utils import *

NUMBER_OF_WORST_CASES = 12


class WorstCase(Tool):
    def init_parser(self, parser):
        parser.add_argument(
            '-p'
            , '--preset'
            , action='store_true'
            , help='Load preset WorstCase graphs from dataset'
        )
        parser.add_argument(
            '-n'
            , '--vertices_number'
            , required=False
            , type=int
            , help='Number of vertices of WorstCase graph'
        )

    def eval(self, args):
        if args.preset is False and args.vertices_number is None:
            print("One of -p/--preset, -n/--vertices_number required")
            exit()

        graphs_dir = add_graph_dir('WorstCase')

        if args.preset is True:
            for n in tqdm(range(2, NUMBER_OF_WORST_CASES), desc='WorstCase graphs generation'):
                gen_worst_case_graph(graphs_dir, 2 ** n)

        if args.vertices_number is not None:
            graph = gen_worst_case_graph(graphs_dir, args.vertices_number)
            print(f'Generated {graph}')


def gen_worst_case_graph(target_dir, vertices):
    output_graph = Graph()

    first_cycle = int(vertices / 2) + 1

    for i in range(0, first_cycle - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(first_cycle - 1, 'A', 0, output_graph)
    add_rdf_edge(first_cycle - 1, 'B', first_cycle, output_graph)

    for i in range(first_cycle, vertices - 1):
        add_rdf_edge(i, 'B', i + 1, output_graph)

    add_rdf_edge(vertices - 1, 'B', first_cycle - 1, output_graph)

    target = os.path.join(target_dir, f'worstcase_{vertices}')

    write_to_rdf(target, output_graph)

    return target
