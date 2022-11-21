import pytest

import cfpq_data


def test_download_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download("")


def test_download_grammars_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download_grammars("")


def test_download_grammars_none():
    assert cfpq_data.download_grammars("java_points_to", graph_name="skos") is None


def test_download_benchmark_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download_benchmark("")
