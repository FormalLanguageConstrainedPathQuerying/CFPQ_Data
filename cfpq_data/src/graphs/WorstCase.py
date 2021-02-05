import rdflib
from tqdm import tqdm

from cfpq_data.src.graphs.Graph import Graph
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.tools.rdf_helper import write_to_rdf, add_rdf_edge
from cfpq_data.src.utils import *

NUMBER_OF_WORST_CASES = 12


class WorstCase(Graph, CmdParser):
    graphs = {}

    def __init__(self, vertices_number):
        self.dirname = add_graph_dir('WorstCase')
        self.basename = f'worstcase_{vertices_number}.xml'

        path_to_graph = gen_worst_case_graph(self.dirname, vertices_number)

        self.graph = rdflib.Graph()
        self.graph.load(path_to_graph)

        self.vertices_number = len(self.graph.all_nodes())
        self.number_of_edges = len(self.graph)

        self.file_size = os.path.getsize(path_to_graph)
        self.file_name, self.file_extension = os.path.splitext(self.basename)

        WorstCase.graphs[self.basename] = path_to_graph

    def get_metadata(self):
        return {
            'name': self.basename
            , 'path': self.dirname
            , 'version': get_info()['version']
            , 'vertices': self.vertices_number
            , 'edges': self.number_of_edges
            , 'size of file': self.file_size
        }

    def save_metadata(self):
        with open(f'{self.dirname}/{self.file_name}_meta.json', 'w') as metadata_file:
            json.dump(self.get_metadata(), metadata_file, indent=4)

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
                WorstCase(2 ** n).save_metadata()

        if args.vertices_number is not None:
            graph = WorstCase(args.vertices_number)
            graph.save_metadata()
            print(f'Generated {graph.basename} to {graph.dirname}')


def gen_worst_case_graph(target_dir, vertices_number):
    output_graph = rdflib.Graph()

    first_cycle = int(vertices_number / 2) + 1

    for i in range(0, first_cycle - 1):
        add_rdf_edge(i, 'A', i + 1, output_graph)

    add_rdf_edge(first_cycle - 1, 'A', 0, output_graph)
    add_rdf_edge(first_cycle - 1, 'B', first_cycle, output_graph)

    for i in range(first_cycle, vertices_number - 1):
        add_rdf_edge(i, 'B', i + 1, output_graph)

    add_rdf_edge(vertices_number - 1, 'B', first_cycle - 1, output_graph)

    target = os.path.join(target_dir, f'worstcase_{vertices_number}')

    write_to_rdf(target, output_graph)

    return f'{target}.xml'
