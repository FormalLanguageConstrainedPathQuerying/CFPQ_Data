from pathlib import Path
import glob

import pytest
import os

PATH_FOLDER = Path(__file__).parent.parent.parent / 'cfpq_data' / 'data'
grammar_list = glob.glob(f'{PATH_FOLDER}/*/Grammars/*.txt')


@pytest.fixture(scope='session', params=[name for name in grammar_list])
def grammar_name(request):
    return request.param