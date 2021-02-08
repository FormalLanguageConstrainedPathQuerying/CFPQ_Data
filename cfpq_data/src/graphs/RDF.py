from tqdm import tqdm

from cfpq_data.src.graphs.GraphInterface import GraphInterface
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import *


class RDF(GraphInterface, CmdParser):
    graphs = dict()
    graph_keys = get_info()['RDF']

    def __init__(self):
        self.store = None

        self.dirname = None
        self.basename = None

        self.number_of_vertices = None
        self.number_of_edges = None

        self.file_size = None
        self.file_name = None
        self.file_extension = None

    @classmethod
    def build(cls, *args):
        try:
            path_to_graph = args[0]
            _, file_extension = os.path.splitext(path_to_graph.basename)

            if file_extension == 'txt':
                return cls.from_txt(path_to_graph)
            if rdflib.util.guess_format(path_to_graph) == 'xml':
                return cls.from_rdf(path_to_graph)

        except BaseException as ex:
            raise BaseException(f'{cls.__name__}:build:{ex}')

    @classmethod
    def from_rdf(cls, path_to_graph):
        if hasattr(cls, 'graph_keys') and path_to_graph in cls.graph_keys:
            graph_name = path_to_graph
            download_data(cls.__name__, graph_name, cls.graph_keys[graph_name])
            path_to_graph = unpack_graph(cls.__name__, graph_name)

        rdf_graph = cls()

        rdf_graph.store = rdflib.Graph()
        rdf_graph.store.load(path_to_graph)

        rdf_graph.dirname = os.path.dirname(path_to_graph)
        rdf_graph.basename = os.path.basename(path_to_graph)

        rdf_graph.number_of_vertices = len(rdf_graph.store.all_nodes())
        rdf_graph.number_of_edges = len(rdf_graph.store)

        rdf_graph.file_size = os.path.getsize(path_to_graph)
        rdf_graph.file_name, rdf_graph.file_extension = os.path.splitext(rdf_graph.basename)

        cls.graphs[rdf_graph.basename] = path_to_graph

        return rdf_graph

    def to_rdf(self, path):
        write_to_rdf(path, self.store)
        return self

    @classmethod
    def from_txt(cls, path):
        tmp_rdf_graph = rdflib.Graph()

        with open(path, 'r') as input_file:
            for edge in input_file:
                s, p, o = edge.split()
                add_rdf_edge(s, p, o, tmp_rdf_graph)
        write_to_rdf('tmp.xml', tmp_rdf_graph)

        rdf_graph = cls.from_rdf('tmp.xml')

        os.remove('tmp.xml')

        return rdf_graph

    def to_txt(self, path):
        ids = dict()
        next_id = 0
        triples = list()

        for subj, pred, obj in self.store:
            if subj not in ids:
                ids[subj] = next_id
                next_id += 1
            if obj not in ids:
                ids[obj] = next_id
                next_id += 1
            triples.append((subj, pred.value, obj))

        with open(path, 'r') as output_file:
            for s, p, o in triples:
                output_file.write(f'{s} {p} {o}\n')

        return TXTGraph.from_txt(path)

    def get_metadata(self):
        return {
            'name': self.basename
            , 'path': self.dirname
            , 'version': get_info()['version']
            , 'vertices': self.number_of_vertices
            , 'edges': self.number_of_edges
            , 'size of file': self.file_size
        }

    def save_metadata(self):
        with open(f'{self.dirname}/{self.file_name}_meta.json', 'w') as metadata_file:
            json.dump(self.get_metadata(), metadata_file, indent=4)

    @staticmethod
    def init_cmd_parser(parser):
        parser.add_argument(
            '-a'
            , '--all'
            , action='store_true'
            , help='Load all RDF graphs from dataset'
        )
        parser.add_argument(
            '-g'
            , '--graph'
            , choices=list(get_info()['RDF'].keys())
            , required=False
            , type=str
            , help='Load specific RDF graph from dataset'
        )

    @staticmethod
    def eval_cmd_parser(args):
        if args.all is False and args.graph is None:
            print('One of -a/--all, -g/--graph required')
            exit()

        if args.all is True:
            clean_dir('RDF')
            for graph_name in tqdm(RDF.graph_keys, desc='Downloading RDF'):
                RDF.from_rdf(graph_name).save_metadata()

        if args.graph is not None:
            graph = RDF.from_rdf(args.graph)
            graph.save_metadata()
            print(f'Loaded {graph.basename} to {graph.dirname}')
