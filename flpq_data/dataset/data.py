"""Download graph data from dataset."""

import logging
import os
import pathlib
import shutil
import tempfile
import warnings

import requests

from flpq_data.config import DATASET_VERSION, GRAPHS_DIR
from flpq_data.dataset.registry import graph_names

__all__ = [
    "DATASET_KEY_PREFIX",
    "DATASET_URL",
    "download_graph",
    "download",
]

DATASET_KEY_PREFIX = f"{DATASET_VERSION}/graph"
DATASET_URL = f"https://cfpq-data.storage.yandexcloud.net/{DATASET_KEY_PREFIX}/"


def download_graph(name: str) -> pathlib.Path:
    """Download graph data from dataset.

    The archive is extracted to a directory named after the graph (the
    internal directory of the archive is normalized to the graph name, so
    archives with a different internal layout, e.g.
    ``cactus_field_sensitive_alias``, extract cleanly).

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.

    Examples
    --------
    >>> from flpq_data import *
    >>> path = download_graph("generations")
    >>> path.name
    'generations'

    Returns
    -------
    path : Path
        Path to the directory with the graph data.
    """
    if name in graph_names():
        logging.info(f"Found graph with {name=}")

        GRAPHS_DIR.mkdir(exist_ok=True, parents=True)

        graph_archive = GRAPHS_DIR / f"{name}.tar.gz"

        with requests.get(
            url=DATASET_URL + f"{name}.tar.gz",
            stream=True,
        ) as r:
            with open(graph_archive, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        logging.info(f"Load archive {graph_archive=}")

        extract_dir = pathlib.Path(tempfile.mkdtemp(dir=GRAPHS_DIR))
        try:
            shutil.unpack_archive(graph_archive, extract_dir)

            entries = list(extract_dir.iterdir())
            if len(entries) != 1 or not entries[0].is_dir():
                raise ValueError(
                    f"Archive {graph_archive=} must contain a single "
                    f"top-level directory, found {entries=}"
                )

            graph = GRAPHS_DIR / name
            if graph.exists():
                shutil.rmtree(graph)
            shutil.move(str(entries[0]), graph)
        finally:
            shutil.rmtree(extract_dir, ignore_errors=True)
            os.remove(graph_archive)

        logging.info(f"Unzip graph {name=} to directory {graph=}")

        return graph
    else:
        raise FileNotFoundError(f"No graph with {name=} found")


def download(name: str) -> pathlib.Path:
    """Deprecated alias of :func:`download_graph`.

    .. deprecated:: 6.0.0
        Use :func:`download_graph` instead.
    """
    warnings.warn(
        "download() is deprecated, use download_graph() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return download_graph(name)
