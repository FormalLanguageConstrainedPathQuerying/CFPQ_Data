import pytest

import cfpq_data


def test_download_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download("")


def test_download_benchmark_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download_benchmark("")
