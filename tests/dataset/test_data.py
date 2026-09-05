import pytest

import cfpq_data
from cfpq_data.dataset import (
    BENCHMARK_URL,
    DATASET,
    DATASET_KEY_PREFIX,
    DATASET_URL,
    GRAMMARS_URL,
    LEGACY_DATASET,
    LEGACY_DATASET_URL,
    MIGRATED_DATASET,
)
from cfpq_data.dataset.data import _dataset_url


def test_url_constants():
    # The dataset lives under the current version prefix; grammars,
    # benchmarks, and the not-yet-migrated graphs stay under 4.0.0.
    assert DATASET_KEY_PREFIX == "5.0.0/graph"
    assert DATASET_URL == "https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/"
    assert (
        LEGACY_DATASET_URL == "https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/"
    )
    assert GRAMMARS_URL == "https://cfpq-data.storage.yandexcloud.net/4.0.0/grammar/"
    assert BENCHMARK_URL == "https://cfpq-data.storage.yandexcloud.net/4.0.0/benchmark/"
    assert cfpq_data.__version__ == "5.0.0"


def test_dataset_split():
    assert len(DATASET) == 113
    assert len(MIGRATED_DATASET) == 54
    assert len(LEGACY_DATASET) == 59
    assert not set(MIGRATED_DATASET) & set(LEGACY_DATASET)
    assert len(set(DATASET)) == len(DATASET)


@pytest.mark.parametrize(
    "name,expected_url",
    [
        ("generations", DATASET_URL),
        ("avrora", DATASET_URL),
        ("gson", LEGACY_DATASET_URL),
        ("cactus_field_sensitive_alias", LEGACY_DATASET_URL),
    ],
)
def test_dataset_url_selection(name, expected_url):
    assert _dataset_url(name) == expected_url


def test_download_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download("")


@pytest.mark.parametrize("template,graph_name", [("", None), ("dyck", "")])
def test_download_grammars_rise(template, graph_name):
    with pytest.raises(FileNotFoundError):
        cfpq_data.download_grammars(template, graph_name=graph_name)


def test_download_grammars_none():
    assert cfpq_data.download_grammars("java_points_to", graph_name="skos") is None


@pytest.mark.parametrize("template,graph_name", [("dyck", None)])
def test_download_grammars_success(template, graph_name):
    assert not cfpq_data.download_grammars(template, graph_name=graph_name) is None


def test_download_benchmark_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download_benchmark("")
