import pytest

import cfpq_data


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
