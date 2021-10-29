import pytest

import cfpq_data


def test_download_rise():
    with pytest.raises(FileNotFoundError):
        cfpq_data.download("")
