from setuptools import setup, find_packages

setup(
    name='cfpq_data'
    , version='0.0.0'
    , packages=find_packages()
    , url='https://github.com/JetBrains-Research/CFPQ_Data'
    , license='Apache License 2.0'
    , author='Grigorev Semyon'
    , author_email='rsdpisuy@gmail.com'
    , description='Graphs and grammars for experimental analysis of context-free path querying algorithms'
    , package_data={'': ['*.json'], 'cfpq_data': ['data/*/Grammars/*.txt']}
    , include_package_data=True
)
