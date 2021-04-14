"""Returns a path to the TXT file
where the graph will be saved.
"""
from pathlib import Path
from typing import Union, Iterable

from networkx import MultiDiGraph

__all__ = ["graph_to_txt"]


def graph_to_txt(
    graph: MultiDiGraph, path: Union[Path, str], labels: Iterable[str] = None
) -> Path:
    """Returns a path to the TXT file
    where the graph will be saved.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to serialize.

    path: Union[Path, str]
        The path to the file where the graph will be serialized.

    labels : Optional[Iterable[str]]
        Graph edge labels to be preserved.
        `None` for all edge labels.

    Examples
    --------
    >>> import cfpq_data
    >>> g = cfpq_data.labeled_cycle_graph(42)
    >>> path = cfpq_data.graph_to_txt(g, "test.txt")

    Returns
    -------
    path : Path
        Path to a TXT file where the graph will be saved.
    """
    path = Path(path).resolve()
    with open(path, "w") as fout:
        for u, v, edge_labels in graph.edges(data=True):
            for label in edge_labels.values():
                if labels is None or str(label) in labels:
                    fout.write(f"'{u}' {label} '{v}'\n")
    return path
