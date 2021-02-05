import logging
import random
import string
from unittest import TestCase

from redis import Redis
from redisgraph import Edge as RedisEdge

from cfpq_data.src.tools.redis_rdf.src.redis_loader.graph import Graph as RedisGraph
from cfpq_data.src.tools.redis_rdf.src.redis_loader.loader import load_in_redis, make_node
from cfpq_data.src.tools.redis_rdf.src.redis_loader.triplet_loader import load_rdf_graph


def print_edge_with_alias(edge: RedisEdge, alias: str):
    return f'{edge.src_node}-[{alias}: {edge.relation} {edge.toString()}]->{edge.dest_node}'


class TestLoad(TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.redis_connector = Redis(host='localhost', port=6380)

    def testLoadTxt(self):
        self.loadAndCheck(load_rdf_graph('examples/graph.txt'))

    def testLoadXml(self):
        self.loadAndCheck(load_rdf_graph('examples/graph.xml'))

    def loadAndCheck(self, rdf_graph):
        redis_graph = RedisGraph(self.randomGraphName(), self.redis_connector)

        # load
        load_in_redis(rdf_graph, redis_graph)

        # check every edge
        for subj, pred, obj in rdf_graph:
            self.assertTrue(self.checkEdgeExist(redis_graph, self.makeEdge(subj, pred, obj)))
            self.assertTrue(self.checkEdgeExist(redis_graph, self.makeEdge(obj, f'{pred}_r', subj)))

        # check total edges count
        self.assertEqual(len(rdf_graph) * 2, self.countEdges(redis_graph))

    @staticmethod
    def makeEdge(subj, pred, obj):
        return RedisEdge(make_node(str(subj), 'src'), pred, make_node(str(obj)), 'dst')

    @staticmethod
    def checkEdgeExist(redis_graph: RedisGraph, edge: RedisEdge):
        query = f'MATCH {print_edge_with_alias(edge, "edge")} RETURN COUNT(edge)'
        count = redis_graph.query(query).result_set[0][0]
        return count > 0

    @staticmethod
    def countEdges(redis_graph: RedisGraph):
        query = f'MATCH ()-[r]->() RETURN COUNT(r)'
        return redis_graph.query(query).result_set[0][0]

    @staticmethod
    def randomGraphName():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))
