from tqdm import tqdm

from cfpq_data import RDF
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils import *

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
    graphs = {}

    @classmethod
    def build(cls, vertices_number):
        path_to_graph = gen_cycle_graph(add_graph_dir('FullGraph'), vertices_number)
        return FullGraph.from_rdf(path_to_graph)

    @staticmethod
    def init_cmd_parser(parser):
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
    def eval_cmd_parser(args):
        if args.preset is False and args.vertices_number is None:
            print("One of -p/--preset, -n/--vertices_number required")
            exit()

        if args.preset is True:
            for n in tqdm(FULL_GRAPH_TO_GEN, desc='Full graphs generation'):
                FullGraph.build(n).save_metadata()

        if args.vertices_number is not None:
            graph = FullGraph.build(args.vertices_number)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_cycle_graph(target_dir, vertices_number):
    output_graph = rdflib.Graph()

    for i in range(0, vertices_number - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(vertices_number - 1, 'A', 0, output_graph)

    target = os.path.join(target_dir, f'fullgraph_{vertices_number}')

    write_to_rdf(target, output_graph)

    return f'{target}.xml'
