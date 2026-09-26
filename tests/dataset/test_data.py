import pytest

import flpq_data
from flpq_data.dataset import DATASET, DATASET_KEY_PREFIX, DATASET_URL


def test_url_constants():
    # The whole dataset lives under the current version prefix.
    assert DATASET_KEY_PREFIX == "5.0.0/graph"
    assert DATASET_URL == "https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/"
    assert flpq_data.__version__ == "5.0.0"


def test_dataset():
    assert len(DATASET) == 113
    assert len(set(DATASET)) == len(DATASET)


def test_download_rise():
    with pytest.raises(FileNotFoundError):
        flpq_data.download("")
