from pathlib import Path

import pytest
import os

PATH_FOLDER = Path(__file__).parent.parent.parent / 'cfpq_data' / 'data'
grammar_list = os.listdir(PATH_FOLDER)


@pytest.fixture(scope='session', params=[name for name in grammar_list if name.endswith(".txt")])
def grammar_name(request):
    return request.param