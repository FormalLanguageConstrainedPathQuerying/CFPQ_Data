import json
import rdflib
import os
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
    for s, p, o in graph:
        d.add((s, p, o))
        vert.add(s)
        vert.add(o)
    return len(vert), len(d)

class RDF(Tool):
    def init_parser(self, parser):
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

    def eval(self, args):
        if args.all is False and args.graph is None:
            print('One of -a/--all, -g/--graph required')
            exit()

        graphs = get_info()['RDF']
        meta_data_dict = {}

        if args.all is True:
            clean_dir('RDF')
            for graph_name in tqdm(graphs, desc='Downloading RDF'):
                download_data('RDF', graph_name, graphs[graph_name])
                unpack_graph('RDF', graph_name)
                graph_file = glob.glob("./data/RDF/Graphs/" + graph_name + ".*")
                with open("./data/RDF/" + graph_name + '_meta.json', 'w') as meta_data_file:
                    meta_data_dict["name"] = graph_name
                    meta_data_dict["path"] = "./data/RDF/Graphs/"
                    meta_data_dict["version"] = "0.0.0"
                    n = num_of_(graph_file[0])
                    meta_data_dict["vertices"] = n[0]
                    meta_data_dict["edges"] = n[1]
                    meta_data_dict["size of file"] = os.path.getsize(graph_file[0])
                    json.dump(meta_data_dict, meta_data_file)

        if args.graph is not None:
            path = download_data('RDF', args.graph, graphs[args.graph])
            unpack_graph('RDF', args.graph)
            print(f'Loaded {args.graph} to {path}')
            graph_file = glob.glob("./data/RDF/Graphs/" + args.graph + ".*")[0]
            with open("./data/RDF/" + args.graph + '_meta.json', 'w') as meta_data_file:
                meta_data_dict["name"] = args.graph
                meta_data_dict["path"] = "./data/RDF/Graphs/"
                meta_data_dict["version"] = "0.0.0"
                n = num_of_(graph_file)
                meta_data_dict["vertices"] = n[0]
                meta_data_dict["edges"] = n[1]
                meta_data_dict["size of file"] = os.path.getsize(graph_file)
                json.dump(meta_data_dict, meta_data_file)
