"""Download graph data from dataset."""
import logging
import os
import pathlib
import shutil
import tempfile

import requests

from typing import Union

from cfpq_data.config import DATA, GRAPHS_DIR, GRAMMARS_DIR, BENCHMARKS_DIR, VERSION

__all__ = [
    "DATASET_KEY_PREFIX",
    "DATASET_URL",
    "LEGACY_VERSION_PREFIX",
    "LEGACY_DATASET_URL",
    "GRAMMARS_URL",
    "BENCHMARK_URL",
    "MIGRATED_DATASET",
    "LEGACY_DATASET",
    "DATASET",
    "GRAMMAR_TEMPLATES",
    "BENCHMARKS",
    "download",
    "download_grammars",
    "download_benchmark",
]

DATASET_KEY_PREFIX = f"{VERSION[0]}.0.0/graph"
DATASET_URL = f"https://cfpq-data.storage.yandexcloud.net/{DATASET_KEY_PREFIX}/"

#: The key prefix of the data that has not been migrated to the current
#: dataset version: the old-format graph archives, the pre-existing
#: new-format graphs, all per-graph grammars, and the benchmarks still live
#: under ``4.0.0``.
LEGACY_VERSION_PREFIX = "4.0.0"
LEGACY_DATASET_URL = (
    f"https://cfpq-data.storage.yandexcloud.net/{LEGACY_VERSION_PREFIX}/graph/"
)
GRAMMARS_URL = (
    f"https://cfpq-data.storage.yandexcloud.net/{LEGACY_VERSION_PREFIX}/grammar/"
)
BENCHMARK_URL = (
    f"https://cfpq-data.storage.yandexcloud.net/{LEGACY_VERSION_PREFIX}/benchmark/"
)

#: The graphs converted from the old format and served from ``DATASET_URL``
#: (the current version prefix).
MIGRATED_DATASET = [
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
]

#: The pre-existing new-format graphs that stay under the legacy version
#: prefix (``LEGACY_DATASET_URL``); their data is not migrated.
LEGACY_DATASET = [
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

#: All downloadable graphs: the migrated ones and the legacy ones.
DATASET = MIGRATED_DATASET + LEGACY_DATASET


GRAMMAR_TEMPLATES = [
    "c_alias",
    "dyck",
    "java_points_to",
    "nested_parentheses",
]


BENCHMARKS = [
    "MS_Reachability",
]


def _dataset_url(name: str) -> str:
    """The base URL serving the archive of ``name``.

    The migrated graphs live under ``DATASET_URL`` (the current version
    prefix); the legacy ones stay under ``LEGACY_DATASET_URL``.
    """
    if name in LEGACY_DATASET:
        return LEGACY_DATASET_URL
    return DATASET_URL


def download(name: str) -> pathlib.Path:
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
    >>> from cfpq_data import *
    >>> path = download("generations")
    >>> sorted(p.name for p in path.iterdir())
    ['README.md', 'grammar', 'graph']

    Returns
    -------
    path : Path
        Path to the directory with the graph data.
    """
    if name in DATASET:
        logging.info(f"Found graph with {name=}")

        GRAPHS_DIR.mkdir(exist_ok=True, parents=True)

        graph_archive = GRAPHS_DIR / f"{name}.tar.gz"

        with requests.get(
            url=_dataset_url(name) + f"{name}.tar.gz",
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


def download_grammars(
    template: str, *, graph_name: Union[str, None] = None
) -> Union[pathlib.Path, None]:
    """Download grammars of the given template.

    Parameters
    ----------
    template : str
        The name of the grammar template from the dataset.

    graph_name : Union[str, None]
        The name of the specified graph from the dataset or None for downloading example grammars.

    Examples
    --------
    >>> from cfpq_data import *
    >>> path = download_grammars("java_points_to", graph_name="avrora")

    Returns
    -------
    path : Union[Path, None]
        Path to the directory with grammars data or None if there is no such grammars in dataset.
    """
    if template not in GRAMMAR_TEMPLATES:
        raise FileNotFoundError(f"No grammar {template=} found")

    if graph_name is None:
        logging.info(f"Found grammar {template=}")
        grammars_name = f"{template}"
        url = GRAMMARS_URL + f"example/{grammars_name}.tar.gz"
    elif graph_name in DATASET:
        logging.info(f"Found graph with {graph_name=} and grammar {template=}")
        grammars_name = f"{template}_{graph_name}"
        url = GRAMMARS_URL + f"{grammars_name}.tar.gz"
    else:
        raise FileNotFoundError(f"No graph with {graph_name=} found")

    GRAMMARS_DIR.mkdir(exist_ok=True, parents=True)

    grammar_archive = GRAMMARS_DIR / f"{grammars_name}.tar.gz"
    grammars = GRAMMARS_DIR / grammars_name

    with requests.get(
        url=url,
        stream=True,
    ) as r:
        if r.status_code == 404:
            logging.info(
                f"No grammars with {template=} for graph with {graph_name=} found"
            )
            return None
        else:
            with open(grammar_archive, "wb") as f:
                shutil.copyfileobj(r.raw, f)

    logging.info(f"Load archive {grammar_archive=}")

    shutil.unpack_archive(grammar_archive, GRAMMARS_DIR)

    logging.info(
        f"Unzip grammars with {template=} for graph with {graph_name=} to directory {grammars=}"
    )

    os.remove(grammar_archive)

    logging.info(f"Remove archive {grammar_archive=}")

    return grammars


def download_benchmark(name: str) -> pathlib.Path:
    """Download benchmark data.

    Parameters
    ----------
    name : str
        The name of the benchmark.

    Examples
    --------
    >>> from cfpq_data import *
    >>> path = download_benchmark("MS_Reachability")

    Returns
    -------
    path : Path
        Path to the directory with benchmark data.
    """
    if name in BENCHMARKS:
        logging.info(f"Found benchmark with {name=}")

        BENCHMARKS_DIR.mkdir(exist_ok=True, parents=True)

        benchmark_archive = BENCHMARKS_DIR / f"{name}.tar.gz"
        benchmark = BENCHMARKS_DIR / name

        with requests.get(
            url=BENCHMARK_URL + f"{name}.tar.gz",
            stream=True,
        ) as r:
            with open(benchmark_archive, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        logging.info(f"Load archive {benchmark_archive=}")

        shutil.unpack_archive(benchmark_archive, BENCHMARKS_DIR)

        logging.info(f"Unzip benchmark {name=} to directory {benchmark=}")

        os.remove(benchmark_archive)

        logging.info(f"Remove archive {benchmark_archive=}")

        return benchmark
    else:
        raise FileNotFoundError(f"No benchmark with {name=} found")
