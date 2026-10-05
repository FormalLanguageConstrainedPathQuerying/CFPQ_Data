import pytest

import flpq_data
from flpq_data.dataset import DATASET_KEY_PREFIX, DATASET_URL


def test_url_constants():
    # The whole dataset lives under the current version prefix.
    assert DATASET_KEY_PREFIX == "6.0.0/graph"
    assert DATASET_URL == "https://cfpq-data.storage.yandexcloud.net/6.0.0/graph/"
    assert flpq_data.__version__ == "6.0.0"


def test_download_graph_rise():
    with pytest.raises(FileNotFoundError):
        flpq_data.download_graph("")


def test_download_deprecated():
    with pytest.warns(DeprecationWarning, match="download_graph"):
        with pytest.raises(FileNotFoundError):
            flpq_data.download("")
