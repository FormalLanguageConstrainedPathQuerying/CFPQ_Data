from setuptools import *

from cfpq_data.config import *

setup(
    name=PACKAGE_NAME
    , version=PACKAGE_VERSION
    , description='Graphs and grammars for experimental analysis of context-free path querying algorithms'
    , long_description=Path(__file__).parent / 'README.md'
    , long_description_content_type='text/markdown'
    , packages=find_packages()
    , package_dir=MAIN_FOLDER
    , url='https://github.com/JetBrains-Research/CFPQ_Data'
    , license='Apache License 2.0'
    , author='Grigorev Semyon'
    , author_email='rsdpisuy@gmail.com'
    , package_data={'': ['*.json'], 'cfpq_data': ['data/*/Grammars/*.txt']}
    , include_package_data=True
    , entry_points={
        'console_scripts': [
            'cfpq_data = cfpq_data.cmd_parser:cmd_parser'
        ]
    }
)
