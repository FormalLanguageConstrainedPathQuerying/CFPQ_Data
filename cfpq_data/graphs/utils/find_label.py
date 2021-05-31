"""Returns the edge label
containing the specified string.
"""
from typing import Tuple, Any, Optional

from networkx import MultiDiGraph
from tqdm import tqdm

__all__ = ["find_label"]


def find_label(
    graph: MultiDiGraph, query: str, verbose: bool = True
) -> Optional[Tuple[Any, Any]]:
    """Returns the edge label
    containing the specified string.

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    query : str
        String to find.

    verbose : bool
        If true, a progress bar will be displayed.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.graph_from_dataset("foaf", verbose=False)
    >>> cfpq_data.find_label(g, "subClassOf", verbose=False)
    ('label', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'))

    Returns
    -------
    response : Optional[Tuple[Any, Any]]
        Pair (``edge label key``, ``edge label value``)
        where ``edge label value`` contains ``query``.
        Not if the required ``edge label value`` is not found.
    """
    res = None

    for _, _, edge_labels in tqdm(
        graph.edges(data=True), disable=not verbose, desc="Searching..."
    ):
        for k, v in edge_labels.items():
            if query in str(v):
                res = (k, v)
                break

    return res
