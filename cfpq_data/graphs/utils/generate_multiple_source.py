import random
import logging

import networkx as nx

__all__ = ["generate_multiple_source"]

def generate_multiple_source(
    graph: nx.MultiDiGraph,
    chunk_size: int
    ) -> list[int]:
    """Returns a fixed-size set of vertices for multiple-source evaluation for the given graph.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph for which the sample is generated.
	
    chunk_size : int
    	Number of nodes to sample into the generated chunk.
    Returns
    -------
    nodes: list[int]
        The list of sampled node indices for which to evaluate multiple-source CFPQ.
    """
    nodes = graph.number_of_nodes()
    nodes_list = random.sample(range(nodes), chunk_size)
    
    logging.info(f"Generate chunk of {chunk_size} nodes for {graph=} for multiple-source evaluation")
    
    return nodes_list