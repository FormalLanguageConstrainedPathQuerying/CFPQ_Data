from cfpq_data.src.graphs.GraphInterface import GraphInterface
from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import *


class RDF(GraphInterface, CmdParser):
    graphs = dict()
    graph_keys = RELEASE_INFO['RDF']
    config = RELEASE_INFO['RDF_Config']

    def __init__(self):
        self.type = None

        self.store = None

        self.path = None
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
            return cls.load(args[0])
        except BaseException as ex:
            raise BaseException(f'{cls.__name__}.build: {ex}')

    @classmethod
    def load(cls, path_to_graph=None, file_extension='rdf'):
        if file_extension == 'txt':
            rdf_graph = cls.load_from_txt(path_to_graph)
        else:
            rdf_graph = cls.load_from_rdf(path_to_graph)

        cls.graphs[(rdf_graph.basename, rdf_graph.file_extension)] = path_to_graph

        return rdf_graph

    def save(self, path_to_graph=None, file_extension='rdf', config=config):
        if path_to_graph is None:
            path_to_graph = DATA_FOLDER / self.type / 'Graphs' / self.basename
        if file_extension == 'txt':
            self.save_to_txt(path_to_graph, config)
        else:
            self.save_to_rdf(path_to_graph)
        return path_to_graph

    def get_metadata(self):
        return {
            'name': self.basename
            , 'path': self.path
            , 'version': RELEASE_INFO['version']
            , 'vertices': self.number_of_vertices
            , 'edges': self.number_of_edges
            , 'size of file': self.file_size
        }

    def save_metadata(self):
        with open(self.dirname / self.file_name + '_meta.json', 'w') as metadata_file:
            json.dump(self.get_metadata(), metadata_file, indent=4)

    def get_triples(self):
        triples = list()
        for subj, pred, obj in self.store:
            triples.append((subj, pred, obj))
        return triples

    @classmethod
    def load_from_rdf(cls, path_to_graph):
        if hasattr(cls, 'graph_keys') and path_to_graph in cls.graph_keys:
            graph_name = path_to_graph[:]
            download_data(cls.__name__, graph_name, cls.graph_keys[graph_name])
            path_to_graph = unpack_graph(cls.__name__, graph_name)

        rdf_graph = cls()

        rdf_graph.type = cls.__name__

        rdf_graph.store = rdflib.Graph()
        rdf_graph.store.parse(location=str(path_to_graph), format='xml')

        rdf_graph.path = path_to_graph
        rdf_graph.dirname = os.path.dirname(path_to_graph)
        rdf_graph.basename = os.path.basename(path_to_graph)

        rdf_graph.number_of_vertices = len(rdf_graph.store.all_nodes())
        rdf_graph.number_of_edges = len(rdf_graph.store)

        rdf_graph.file_size = os.path.getsize(path_to_graph)
        rdf_graph.file_name, rdf_graph.file_extension = os.path.splitext(rdf_graph.basename)

        return rdf_graph

    @classmethod
    def load_from_txt(cls, path_to_graph):
        tmp_rdf_graph = rdflib.Graph()

        with open(path_to_graph, 'r') as input_file:
            for edge in input_file:
                s, p, o = edge.split()
                add_rdf_edge(s, p, o, tmp_rdf_graph)
        write_to_rdf('tmp.xml', tmp_rdf_graph)

        rdf_graph = cls.load_from_rdf('tmp.xml')

        os.remove('tmp.xml')

        return rdf_graph

    def save_to_rdf(self, path_to_graph):
        write_to_rdf(path_to_graph, self.store)
        return path_to_graph

    def save_to_txt(self, path_to_graph, config=config):
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

        with open(path_to_graph, 'w') as output_file:
            for s, p, o in triples:
                output_file.write(f'{s} {p} {o}\n')

        return path_to_graph

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
            , choices=list(RELEASE_INFO['RDF'].keys())
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
                RDF.load_from_rdf(graph_name).save_metadata()

        if args.graph is not None:
            graph = RDF.load_from_rdf(args.graph)
            graph.save_metadata()
            print(f'Loaded {graph.basename} to {graph.dirname}')
