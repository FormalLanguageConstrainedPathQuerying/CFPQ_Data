import hashlib

from redis import Redis
from redisgraph import Node as RedisNode, Edge as RedisEdge
from tqdm import tqdm

from .graph import Graph as RedisGraph
from .triplet_loader import load_rdf_graph

BLOCK_SIZE = 100

def make_node(value: str, alias=None):
    return RedisNode(
        label='Node', alias=alias, properties={
            'value': value,
            'sha256': hashlib.sha256(str(value).encode('utf-8')).hexdigest()
        })

def load_in_redis(rdf_graph, redis_graph: RedisGraph):
    all_nodes = dict()

    # Add all nodes from file to hash map
    for subj, _, obj in rdf_graph:
        all_nodes.setdefault(str(subj), make_node(str(subj)))
        all_nodes.setdefault(str(obj), make_node(str(obj)))

    print(f'{redis_graph.name}: Add all nodes to redis graph')
    for k, v in tqdm(all_nodes.items()):
        redis_graph.add_node(v)
        if len(redis_graph.nodes) > BLOCK_SIZE:
            redis_graph.flush()
    redis_graph.flush()

    # Create index over Nodes
    redis_graph.query("CREATE INDEX ON :Node(sha256)")

    print(f'{redis_graph.name}: Add edges to existing nodes')
    for subj, pred, obj in tqdm(rdf_graph):
        edge = RedisEdge(all_nodes[str(subj)], pred, all_nodes[str(obj)])
        edge_r = RedisEdge(all_nodes[str(obj)], f'{pred}_r', all_nodes[str(subj)])
        redis_graph.add_node(all_nodes[str(subj)])
        redis_graph.add_node(all_nodes[str(obj)])
        redis_graph.add_edge(edge)
        redis_graph.add_edge(edge_r)
        if len(redis_graph.edges) > BLOCK_SIZE:
            redis_graph.flush_edges()
    redis_graph.flush_edges()


def load(rdf_file: str, redis_graph_name: str, redis_host: str, redis_port: int):
    rdf_graph = load_rdf_graph(rdf_file)

    redis_connector = Redis(host=redis_host, port=redis_port)
    redis_graph = RedisGraph(redis_graph_name, redis_connector)

    load_in_redis(rdf_graph, redis_graph)
