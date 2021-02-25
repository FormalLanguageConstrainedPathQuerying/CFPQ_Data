from pathlib import Path

from rdflib import Graph, BNode, URIRef


def write_to_rdf(target_path: Path, graph: Graph):
    """
    Saves the graph along the specified path

    :param target_path: path where to save the graph
    :type target_path: Path
    :param graph: graph to be saved
    :type graph: rdflib.Graph
    :return: None
    :rtype: None
    """

    graph.serialize(destination=str(target_path), format='xml')


def add_rdf_edge(subj: int, pred: str, obj: int,
                 rdf_graph: Graph,
                 reverse: bool = False) -> None:
    """
    Add edge to RDF graph

    :param subj: number of the starting vertex
    :type subj: int
    :param pred: the label of the edge to be added
    :type pred: str
    :param obj: number of the ending vertex
    :type obj: int
    :param rdf_graph: the graph to which the edge will be added
    :type rdf_graph: rdflib.Graph
    :param reverse: a label indicating whether to add a reverse edge to the graph
    :type reverse: bool
    :return: None
    :rtype: None
    """

    s = BNode(f'id-{subj}')

    p_text = str(pred)
    if not p_text.startswith('http'):
        p_text = f'http://yacc/rdf-schema#{p_text}'
    p = URIRef(p_text)

    o = BNode(f'id-{obj}')

    rdf_graph.add((s, p, o))

    if reverse is True:
        pr = URIRef(str(p) + 'R')
        rdf_graph.add((s, pr, o))
