"""Read (and write) a graph from (and to) CSV file."""
import logging
import pathlib
from typing import Union

import networkx as nx
import pandas as pd

__all__ = [
    "graph_from_csv",
    "graph_to_csv",
]


def graph_from_csv(path: Union[pathlib.Path, str]) -> nx.MultiDiGraph:
    """Loads a graph from CSV file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the CSV file with which
        the graph will be created.

    Examples
    --------
    >>> from cfpq_data import *
    >>> p = cfpq_data.download("generations")
    >>> g = cfpq_data.graph_from_csv(p)
    >>> g.number_of_nodes()
    129
    >>> g.number_of_edges()
    273

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    data = pd.read_csv(
        filepath_or_buffer=path,
        sep=" ",
        header=None,
        names=["from", "to", "label"],
        engine="c",
    )

    graph = nx.from_pandas_edgelist(
        df=data,
        source="from",
        target="to",
        edge_attr="label",
        create_using=nx.MultiDiGraph,
    )

    logging.info(f"Load {graph=} from {path=}")

    return graph


def graph_to_csv(
    graph: nx.MultiDiGraph, path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Saves the `graph` to the CSV file by `path`.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path : Union[Path, str]
        The path to the CSV file where the graph will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> p = download("generations")
    >>> g = graph_from_csv(p)
    >>> path = graph_to_csv(g, "test.csv")

    Returns
    -------
    path : Path
        Path to the CSV file where the graph will be saved.
    """
    with open(file=path, mode="w") as f:
        for u, v, edge_labels in graph.edges(data=True):
            for e in edge_labels.values():
                f.write(f"{u} {v} {e}\n")

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {graph=} to {dest=}")

    return dest
