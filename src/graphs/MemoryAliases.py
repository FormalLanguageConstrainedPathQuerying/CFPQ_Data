import rdflib
import glob

from tqdm import tqdm

from src.tools.base import Tool
from src.utils import *
from src.tools.redis_rdf.src.redis_loader.triplet_loader import uri_to_name


def num_of_(graph_name):
    graph = rdflib.Graph()
    graph.load(graph_name)
    d = set()
    vert = set()
    a, b = 0, 0
    for s, p, o in graph:
        d.add((s, p, o))
        vert.add(s)
        vert.add(o)
        if uri_to_name(p, graph) == 'A':
            a += 1
        else:
            b += 1
    return len(vert), len(d), a, b



class MemoryAliases(Tool):
    def init_parser(self, parser):
        parser.add_argument(
            '-a'
            , '--all'
            , action='store_true'
            , help='Load all MemoryAliases graphs from dataset'
        )
        parser.add_argument(
            '-g'
            , '--graph'
            , choices=list(get_info()['MemoryAliases'].keys())
            , required=False
            , type=str
            , help='Load specific MemoryAliases graph from dataset'
        )

    def eval(self, args):
        if args.all is False and args.graph is None:
            print('One of -a/--all, -g/--graph required')
            exit()

        graphs = get_info()['MemoryAliases']
        meta_data_dict = {}

        if args.all is True:
            clean_dir('MemoryAliases')
            for graph_name in tqdm(graphs, desc='Downloading MemoryAliases'):
                download_data('MemoryAliases', graph_name, graphs[graph_name])
                unpack_graph('MemoryAliases', graph_name)
                graph_file = glob.glob("./data/MemoryAliases/Graphs/" + graph_name + ".*")
                with open("./data/MemoryAliases/" + graph_name + '_meta.json', 'w') as meta_data_file:
                    meta_data_dict["name"] = graph_name
                    meta_data_dict["path"] = "./data/MemoryAliases/Graphs/"
                    meta_data_dict["version"] = "0.0.0"
                    n = num_of_(graph_file[0])
                    meta_data_dict["vertices"] = n[0]
                    meta_data_dict["edges"] = {"All": n[1],
                                               "A": n[2],
                                               "D": n[3]}
                    meta_data_dict["size of file"] = os.path.getsize(graph_file[0])
                    json.dump(meta_data_dict, meta_data_file)

        if args.graph is not None:
            path = download_data('MemoryAliases', args.graph, graphs[args.graph])
            unpack_graph('MemoryAliases', args.graph)
            print(f'Loaded {args.graph} to {path}')
            graph_file = glob.glob("./data/MemoryAliases/Graphs/" + args.graph + ".*")[0]
            with open("./data/MemoryAliases/" + args.graph + '_meta.json', 'w') as meta_data_file:
                meta_data_dict["name"] = args.graph
                meta_data_dict["path"] = "./data/MemoryAliases/Graphs/"
                meta_data_dict["version"] = "0.0.0"
                n = num_of_(graph_file)
                meta_data_dict["vertices"] = n[0]
                meta_data_dict["edges"] = {"All":n[1],
                                               "A": n[2],
                                               "D": n[3]}
                meta_data_dict["size of file"] = os.path.getsize(graph_file)
                json.dump(meta_data_dict, meta_data_file)
