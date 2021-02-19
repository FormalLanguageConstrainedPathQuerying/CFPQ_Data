import json
from pathlib import Path

PACKAGE_NAME = 'cfpq_data'

MAIN_FOLDER = Path(__file__).parent

with open(MAIN_FOLDER / 'release_notes.json', 'r') as input_file:
    RELEASE_INFO = json.load(input_file)

PACKAGE_VERSION = RELEASE_INFO['version']
