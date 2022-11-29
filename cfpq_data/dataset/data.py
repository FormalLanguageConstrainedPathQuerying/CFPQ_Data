"""Download graph data from dataset."""
import logging
import os
import pathlib
import shutil

import requests

from typing import Union

from cfpq_data.config import DATA, GRAPHS_DIR, GRAMMARS_DIR, BENCHMARKS_DIR, VERSION

__all__ = [
    "DATASET_URL",
    "GRAMMARS_URL",
    "BENCHMARK_URL",
    "DATASET",
    "GRAMMAR_TEMPLATES",
    "BENCHMARKS",
    "download",
    "download_grammars",
    "download_benchmark",
]

DATASET_URL = f"https://cfpq-data.storage.yandexcloud.net/{VERSION[0]}.0.0/graph/"
GRAMMARS_URL = f"https://cfpq-data.storage.yandexcloud.net/{VERSION[0]}.0.0/grammar/"
BENCHMARK_URL = f"https://cfpq-data.storage.yandexcloud.net/{VERSION[0]}.0.0/benchmark/"

DATASET = [
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


GRAMMAR_TEMPLATES = [
    "c_alias",
    "dyck",
    "java_points_to",
    "nested_parentheses",
]


BENCHMARKS = [
    "MS_Reachability",
]


def download(name: str) -> pathlib.Path:
    """Download graph data from dataset.

    Parameters
    ----------
    name : str
        The name of the graph from the dataset.

    Examples
    --------
    >>> from cfpq_data import *
    >>> path = download("generations")

    Returns
    -------
    path : Path
        Path to the file with graph data.
    """
    if name in DATASET:
        logging.info(f"Found graph with {name=}")

        GRAPHS_DIR.mkdir(exist_ok=True, parents=True)

        graph_archive = GRAPHS_DIR / f"{name}.tar.gz"
        graph = GRAPHS_DIR / name / f"{name}.csv"

        with requests.get(
            url=DATASET_URL + f"{name}.tar.gz",
            stream=True,
        ) as r:
            with open(graph_archive, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        logging.info(f"Load archive {graph_archive=}")

        shutil.unpack_archive(graph_archive, GRAPHS_DIR)

        logging.info(f"Unzip graph {name=} to file {graph=}")

        os.remove(graph_archive)

        logging.info(f"Remove archive {graph_archive=}")

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
