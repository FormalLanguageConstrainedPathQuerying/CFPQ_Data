import pytest

import flpq_data
from flpq_data.dataset import (
    DATASET,
    DATASET_KEY_PREFIX,
    DATASET_URL,
    GRAPHS,
)


def test_url_constants():
    # The whole dataset lives under the current version prefix.
    assert DATASET_KEY_PREFIX == "5.0.0/graph"
    assert DATASET_URL == "https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/"
    assert flpq_data.__version__ == "5.0.0"


def test_graphs():
    assert len(GRAPHS) == 113
    assert len(set(GRAPHS)) == len(GRAPHS)


def test_dataset_alias():
    # DATASET is a deprecated alias of GRAPHS (renamed in 6.0.0).
    assert DATASET is GRAPHS


def test_download_graph_rise():
    with pytest.raises(FileNotFoundError):
        flpq_data.download_graph("")


def test_download_deprecated():
    with pytest.warns(DeprecationWarning, match="download_graph"):
        with pytest.raises(FileNotFoundError):
            flpq_data.download("")
