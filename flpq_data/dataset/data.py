"""Download graph data from dataset."""

import logging
import os
import pathlib
import shutil
import tempfile
import warnings

import requests

from flpq_data.config import GRAPHS_DIR, VERSION

__all__ = [
    "DATASET_KEY_PREFIX",
    "DATASET_URL",
    "GRAPHS",
    "download_graph",
    "DATASET",
    "download",
]

DATASET_KEY_PREFIX = f"{VERSION[0]}.0.0/graph"
DATASET_URL = f"https://cfpq-data.storage.yandexcloud.net/{DATASET_KEY_PREFIX}/"

#: All downloadable graphs, served from ``DATASET_URL``.
GRAPHS = [
    "skos",
    "wc",
    "generations",
    "travel",
    "univ",
    "atom",
    "biomedical",
    "bzip",
    "foaf",
    "people",
    "pr",
    "funding",
    "ls",
    "wine",
    "pizza",
    "gzip",
    "core",
    "pathways",
    "enzyme",
    "eclass",
    "go_hierarchy",
    "go",
    "apache",
    "init",
    "mm",
    "geospecies",
    "ipc",
    "lib",
    "block",
    "arch",
    "crypto",
    "security",
    "sound",
    "net",
    "fs",
    "drivers",
    "postgre",
    "kernel",
    "taxonomy",
    "taxonomy_hierarchy",
    "avrora",
    "batik",
    "eclipse",
    "fop",
    "h2",
    "jython",
    "luindex",
    "lusearch",
    "pmd",
    "sunflow",
    "tomcat",
    "tradebeans",
    "tradesoap",
    "xalan",
    "airflow",
    "cactus",
    "cactus_field_sensitive_alias",
    "celery",
    "click",
    "commons_io",
    "commons_lang3",
    "django",
    "fastapi",
    "flask",
    "gson",
    "guava",
    "httpx",
    "imagick",
    "imagick_field_sensitive_alias",
    "itsdangerous",
    "jackson",
    "jiaozi",
    "jinja",
    "jsonpath",
    "junit5",
    "leela",
    "leela_field_sensitive_alias",
    "libgdx",
    "mockito",
    "nab",
    "nab_field_sensitive_alias",
    "omnetpp",
    "omnetpp_field_sensitive_alias",
    "pandas",
    "parest",
    "parest_field_sensitive_alias",
    "perlbench",
    "perlbench_field_sensitive_alias",
    "pluggy",
    "povray",
    "povray_field_sensitive_alias",
    "requests",
    "sampleproject",
    "scikit-learn",
    "shattered_pixel_dungeon",
    "sphinx",
    "superset",
    "unigraph_1",
    "unigraph_10",
    "unigraph_2",
    "unigraph_3",
    "unigraph_4",
    "unigraph_5",
    "unigraph_6",
    "unigraph_7",
    "unigraph_8",
    "unigraph_9",
    "wikipedia-provenance",
    "x264",
    "x264_field_sensitive_alias",
    "xz",
    "xz_field_sensitive_alias",
    "zulip",
]


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
    if name in GRAPHS:
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


#: Deprecated alias of :data:`GRAPHS` (renamed in 6.0.0). A plain constant —
#: a module ``__getattr__`` would fire during the package's own star import.
DATASET = GRAPHS


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
