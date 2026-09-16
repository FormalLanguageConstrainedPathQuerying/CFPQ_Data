"""Read (and write) a graph from (and to) a directory of MatrixMarket files."""
import logging
import pathlib
from typing import Dict, List, Tuple, Union

import networkx as nx

__all__ = [
    "filename_to_label",
    "label_to_filename",
    "graph_from_mtx_dir",
    "graph_to_mtx_dir",
]

#: The header lines of the Boolean MatrixMarket files of the dataset.
_MTX_HEADER = (
    "%%MatrixMarket matrix coordinate pattern general",
    "%%GraphBLAS type bool",
)


def filename_to_label(filename: Union[pathlib.Path, str]) -> str:
    """Returns the edge label of a MatrixMarket file name.

    The file name is the label itself (``load_5.mtx`` holds the edges labeled
    ``load_5``).

    Parameters
    ----------
    filename : Union[Path, str]
        The name of a MatrixMarket file.

    Examples
    --------
    >>> filename_to_label("type.mtx")
    'type'
    >>> filename_to_label("alloc_r.mtx")
    'alloc_r'
    >>> filename_to_label("load_5.mtx")
    'load_5'

    Returns
    -------
    label : str
        The edge label of the file.
    """
    label = pathlib.Path(filename).stem

    logging.info(f"Map {filename=} to {label=}")

    return label


def label_to_filename(label: str) -> str:
    """Returns the canonical MatrixMarket file name of an edge label.

    The canonical style is ``<label>.mtx``; reading it back with
    :func:`filename_to_label` returns the same label.

    Parameters
    ----------
    label : str
        The edge label.

    Examples
    --------
    >>> label_to_filename("load_5")
    'load_5.mtx'
    >>> label_to_filename("alloc_r")
    'alloc_r.mtx'

    Returns
    -------
    filename : str
        The file name of the label.
    """
    return f"{label}.mtx"


def graph_from_mtx_dir(path: Union[pathlib.Path, str]) -> nx.MultiDiGraph:
    """Loads a graph from a directory of MatrixMarket files.

    Each ``*.mtx`` file in the directory is a Boolean pattern matrix with one
    entry per edge of a single label (0-based indices, no values); the label
    is derived from the file name by :func:`filename_to_label`.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the directory with the MatrixMarket files.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> d = pathlib.Path(tempfile.mkdtemp()) / "graph"
    >>> _ = d.mkdir(parents=True)
    >>> _ = (d / "a.mtx").write_text(
    ...     "%%MatrixMarket matrix coordinate pattern general\\n"
    ...     "%%GraphBLAS type bool\\n3 3 2\\n0 1\\n1 2\\n"
    ... )
    >>> _ = (d / "b_5.mtx").write_text(
    ...     "%%MatrixMarket matrix coordinate pattern general\\n"
    ...     "%%GraphBLAS type bool\\n3 3 1\\n2 0\\n"
    ... )
    >>> g = graph_from_mtx_dir(d)
    >>> sorted((u, v, e["label"]) for u, v, e in g.edges(data=True))
    [(0, 1, 'a'), (1, 2, 'a'), (2, 0, 'b_5')]

    Returns
    -------
    g : MultiDiGraph
        Loaded graph.
    """
    path = pathlib.Path(path)
    graph = nx.MultiDiGraph()

    for mtx_file in sorted(path.glob("*.mtx")):
        label = filename_to_label(mtx_file.name)

        with open(mtx_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if tuple(lines[:2]) != _MTX_HEADER:
            raise ValueError(f"Unexpected header in {mtx_file=}")

        rows, cols, nnz = map(int, lines[2].split())
        pairs = lines[3:]
        if len(pairs) != nnz:
            raise ValueError(f"{mtx_file=} declares {nnz} entries but has {len(pairs)}")

        for pair in pairs:
            i, j = map(int, pair.split())
            graph.add_edge(i, j, label=label)

    logging.info(f"Load {graph=} from {path=}")

    return graph


def graph_to_mtx_dir(
    graph: nx.MultiDiGraph, path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Saves the ``graph`` to a directory of MatrixMarket files by ``path``.

    One file per edge label (the canonical name from
    :func:`label_to_filename`); each file is a Boolean pattern matrix with
    0-based indices and no values. The node ids must be non-negative integers
    (the matrix dimensions are the largest node id plus one).

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save.

    path : Union[Path, str]
        The path to the directory where the MatrixMarket files will be saved.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> g = nx.MultiDiGraph()
    >>> _ = g.add_edges_from(
    ...     [(0, 1, {"label": "a"}), (1, 2, {"label": "a"}),
    ...      (2, 0, {"label": "b_5"})]
    ... )
    >>> d = pathlib.Path(tempfile.mkdtemp())
    >>> path = graph_to_mtx_dir(g, d / "graph")
    >>> g2 = graph_from_mtx_dir(path)
    >>> sorted((u, v, e["label"]) for u, v, e in g2.edges(data=True)) == \\
    ...     sorted((u, v, e["label"]) for u, v, e in g.edges(data=True))
    True

    Returns
    -------
    path : Path
        Path to the directory where the graph will be saved.
    """
    dest = pathlib.Path(path)
    dest.mkdir(parents=True, exist_ok=True)

    nodes = list(graph.nodes())
    if any(not isinstance(node, int) or node < 0 for node in nodes):
        raise TypeError(f"The node ids of {graph=} must be non-negative integers")
    dimension = max(nodes, default=-1) + 1

    by_label: Dict[str, List[Tuple[int, int]]] = {}
    for u, v, data in graph.edges(data=True):
        by_label.setdefault(data["label"], []).append((u, v))

    for label in sorted(by_label):
        pairs = by_label[label]
        lines = [*_MTX_HEADER, f"{dimension} {dimension} {len(pairs)}"]
        lines += [f"{i} {j}" for i, j in pairs]
        (dest / label_to_filename(label)).write_text("\n".join(lines) + "\n")

    dest = dest.resolve()

    logging.info(f"Save {graph=} to {dest=}")

    return dest
