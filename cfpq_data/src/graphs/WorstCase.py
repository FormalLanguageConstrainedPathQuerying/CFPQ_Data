from cfpq_data.src.graphs.RDF import RDF
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.tools.rdf_helper import write_to_rdf
from cfpq_data.src.utils import *

NUMBER_OF_WORST_CASES = 12


class WorstCase(RDF, CmdParser):
    graphs = {}

    @classmethod
    def build(cls, vertices_number):
        path_to_graph = gen_worst_case_graph(add_graph_dir('WorstCase'), vertices_number)
        return WorstCase.load_from_rdf(path_to_graph)

    @staticmethod
    def init_cmd_parser(parser):
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

    @staticmethod
    def eval_cmd_parser(args):
        if args.preset is False and args.vertices_number is None:
            print("One of -p/--preset, -n/--vertices_number required")
            exit()

        if args.preset is True:
            for n in tqdm(range(2, NUMBER_OF_WORST_CASES), desc='WorstCase graphs generation'):
                WorstCase.build(2 ** n).save_metadata()

        if args.vertices_number is not None:
            graph = WorstCase.build(args.vertices_number)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_worst_case_graph(target_dir, vertices_number):
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

    target = target_dir / f'worstcase_{vertices_number}.xml'

    write_to_rdf(target, output_graph)

    return target
