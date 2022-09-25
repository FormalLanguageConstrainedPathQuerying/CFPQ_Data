"""Utilities for the multiple-source query evaluation."""
import random
import logging
import pathlib
import shlex
from typing import List, Tuple, Union

import networkx as nx

__all__ = [
    "generate_multiple_source",
    "generate_multiple_source_percent",
    "multiple_source_from_txt",
    "multiple_source_to_txt",
    "multiple_source_result_from_txt",
    "multiple_source_result_to_txt",
]


def generate_multiple_source(
    graph: nx.MultiDiGraph,
    set_size: int,
    *,
    seed: Union[int, None] = None,
) -> List[int]:
    """Returns a fixed-size list of unique graph vertices for multiple-source evaluation.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph for which the sample is generated.

    set_size : int
        Number of nodes to sample into the generated set.

    seed : Union[int, None]
        Indicator of random number generation state.

    Examples
    --------
    >>> from cfpq_data import *
    >>> seed = 42
    >>> g = cfpq_data.labeled_two_cycles_graph(42, 29)
    >>> source_vertices = cfpq_data.generate_multiple_source(g, 10, seed=seed)
    >>> source_vertices
    [3, 4, 12, 14, 15, 18, 29, 32, 36, 54]

    Returns
    -------
    source_vertices: List[int]
        The sorted list of unique sampled vertices for the given graph.
    """
    num_nodes = graph.number_of_nodes()

    if set_size > num_nodes:
        raise ValueError(
            f"{set_size} exceeds the number of nodes in a graph ({num_nodes})"
        )
    elif set_size < 0:
        raise ValueError(f"{set_size} cannot be negative")

    random.seed(seed)
    source_vertices = list(random.sample(list(graph.nodes), set_size))
    source_vertices.sort()

    logging.info(
        f"Generate set of source vertices of {set_size} nodes for {graph=} for multiple-source evaluation"
    )

    return source_vertices


def generate_multiple_source_percent(
    graph: nx.MultiDiGraph,
    percent: float,
    *,
    seed: Union[int, None] = None,
) -> List[int]:
    """Returns a list of unique graph vertices with the given percent of vertices for multiple-source evaluation.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph for which the sample is generated.

    percent : float
        Percent of nodes to sample into the generated set.

    seed : Union[int, None]
        Indicator of random number generation state.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = cfpq_data.labeled_two_cycles_graph(42, 29)
    >>> g.number_of_nodes()
    72
    >>> seed = 42
    >>> source_vertices = cfpq_data.generate_multiple_source_percent(g, 10.0, seed=seed)
    >>> source_vertices
    [4, 14, 15, 18, 29, 32, 36]

    Returns
    -------
    source_vertices: List[int]
        The sorted list of unique sampled vertices for the given graph.
    """

    if percent < 0 or percent > 100:
        raise ValueError(f"{percent} is incorrect percent of vertices")

    return generate_multiple_source(
        graph, int(graph.number_of_nodes() * percent / 100.0), seed=seed
    )


def multiple_source_from_txt(path: Union[pathlib.Path, str]) -> List[int]:
    """Returns a list of source vertices loaded from a TXT file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with the set of source vertices.

    Examples
    --------
    >>> from cfpq_data import *
    >>> l = [1, 2, 5, 10]
    >>> path = multiple_source_to_txt(l, "test.txt")
    >>> source_vertices = multiple_source_from_txt(path)
    >>> source_vertices
    [1, 2, 5, 10]

    Returns
    -------
    source_vertices: List[int]
        The loaded list of source vertices.
    """

    source_vertices = []

    with open(path, "r") as f:
        for vertex in f:
            try:
                v = int(vertex.strip())
                source_vertices.append(v)
            except Exception as e:
                raise ValueError(
                    f"{vertex} does not match the input format (integer)"
                ) from e

        logging.info(f"Load {source_vertices=} from {path=}")

    return source_vertices


def multiple_source_to_txt(
    source_vertices: List[int], path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Returns a path to the TXT file where the graph will be saved.

    Parameters
    ----------
    source_vertices : List[int]
        The list of source vertices to save.

    path: Union[Path, str]
        The path to the file where the list of source vertices will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> l = [1, 2, 5, 10]
    >>> path = multiple_source_to_txt(l, "test.txt")

    Returns
    -------
    path : Path
        Path to a TXT file where the list of source vertices will be saved.
    """
    with open(path, "w") as f:
        for vertex in source_vertices:
            f.write(str(vertex) + "\n")

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {source_vertices=} to {dest=}")

    return dest


def multiple_source_result_from_txt(
    path: Union[pathlib.Path, str]
) -> List[Tuple[int, int]]:
    """Returns a list with the result of multiple-source query evaluation loaded from a TXT file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with the result of multiple-source query evaluation.

    Examples
    --------
    >>> from cfpq_data import *
    >>> ms_result = [(1, 1), (1, 3), (2, 2), (3, 1)]
    >>> path = multiple_source_result_to_txt(ms_result, "test.txt")
    >>> reachable_pairs = multiple_source_result_from_txt(path)
    >>> reachable_pairs
    [(1, 1), (1, 3), (2, 2), (3, 1)]

    Returns
    -------
    reachable_pairs: List[Tuple[int, int]]
        The loaded pairs of reachable vertices.
    """

    reachable_pairs = []

    with open(path, "r") as f:
        for vertex_pair in f:
            try:
                u, v = shlex.split(vertex_pair.strip())
                reachable_pairs.append((int(u), int(v)))
            except Exception as e:
                raise ValueError(
                    f"{vertex_pair} does not match the input format: FROM TO"
                ) from e

        logging.info(f"Load {reachable_pairs=} from {path=}")

    return reachable_pairs


def multiple_source_result_to_txt(
    reachable_pairs: List[Tuple[int, int]], path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Returns a path to the TXT file where the multiple-source query evaluation result will be saved.

    Parameters
    ----------
    reachable_pairs : List[Tuple[int, int]]
        The multiple-source query evaluation result to save.

    path: Union[Path, str]
        The path to the file where the multiple-source query evaluation result will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> ms_result = [(1, 1), (1, 3), (2, 2), (3, 1)]
    >>> path = multiple_source_result_to_txt(ms_result, "test.txt")

    Returns
    -------
    path : Path
        Path to a TXT file where the multiple-source query evaluation result will be saved.
    """
    with open(path, "w") as f:
        for u, v in reachable_pairs:
            f.write(f"{u} {v}\n")

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {reachable_pairs=} to {dest=}")

    return dest
