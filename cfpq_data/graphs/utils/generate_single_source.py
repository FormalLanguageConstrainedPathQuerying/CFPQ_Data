import random
import logging
from typing import List

import networkx as nx

__all__ = ["generate_single_source"]

def generate_single_source(
    graph: nx.MultiDiGraph
    ) -> List[int]:
    """Returns a set of vertices for single-source evaluation for the given graph.

    The size of generated set is dependant on the number of nodes in the graph.
    For 

    Parameters
    ----------
    graph : MultiDiGraph
        Graph for which the sample is generated.

    Returns
    -------
    nodes: List[int]
        The list of sampled node indices for which to evaluate single-source CFPQ.
    """
    nodes = graph.number_of_nodes()
    sources = []
    noderange = int(0)
    if nodes < 10000:
        noderange = nodes
    elif nodes < 100000:
        noderange = nodes // 10
    else:
        noderange = nodes // 100

    for i in range(noderange):
        sources.append(random.randrange(0, nodes))

    logging.info(f"Generate nodes for {graph=} for single-source evaluation")    
	
    return sources