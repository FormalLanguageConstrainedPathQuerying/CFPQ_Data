"""Download graph data from dataset."""
import logging
import os
import pathlib
import shutil

import requests

from cfpq_data.config import DATA, VERSION

__all__ = [
    "DATASET_URL",
    "BENCHMARK_URL",
    "DATASET",
    "BENCHMARK",
    "download",
    "download_benchmark",
]

DATASET_URL = f"https://cfpq-data.storage.yandexcloud.net/{VERSION[0]}.0.0/graph/"
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


BENCHMARK = [
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

        DATA.mkdir(exist_ok=True, parents=True)

        graph_archive = DATA / f"{name}.tar.gz"
        graph = DATA / name / f"{name}.csv"

        with requests.get(
            url=DATASET_URL + f"{name}.tar.gz",
            stream=True,
        ) as r:
            with open(graph_archive, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        logging.info(f"Load archive {graph_archive=}")

        shutil.unpack_archive(graph_archive, DATA)

        logging.info(f"Unzip graph {name=} to file {graph=}")

        os.remove(graph_archive)

        logging.info(f"Remove archive {graph_archive=}")

        return graph
    else:
        raise FileNotFoundError(f"No graph with {name=} found")


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
    if name in BENCHMARK:
        logging.info(f"Found benchmark with {name=}")

        DATA.mkdir(exist_ok=True, parents=True)

        benchmark_archive = DATA / f"{name}.tar.gz"
        benchmark = DATA / name

        with requests.get(
            url=BENCHMARK_URL + f"{name}.tar.gz",
            stream=True,
        ) as r:
            with open(benchmark_archive, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        logging.info(f"Load archive {benchmark_archive=}")

        shutil.unpack_archive(benchmark_archive, DATA)

        logging.info(f"Unzip benchmark {name=} to directory {benchmark=}")

        os.remove(benchmark_archive)

        logging.info(f"Remove archive {benchmark_archive=}")

        return benchmark
    else:
        raise FileNotFoundError(f"No benchmark with {name=} found")
