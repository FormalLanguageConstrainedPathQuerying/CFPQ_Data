CFPQ_Data
=========

.. image:: https://github.com/JetBrains-Research/CFPQ_Data/actions/workflows/tests.yml/badge.svg?branch=master
   :target: https://github.com/JetBrains-Research/CFPQ_Data/actions/workflows/tests.yml

.. image:: https://codecov.io/gh/JetBrains-Research/CFPQ_Data/branch/master/graph/badge.svg?token=6IAZM6KZT7
   :target: https://codecov.io/gh/JetBrains-Research/CFPQ_Data

.. image:: https://img.shields.io/pypi/v/cfpq-data.svg
   :target: https://pypi.org/project/cfpq-data/

.. image:: https://img.shields.io/pypi/pyversions/cfpq-data.svg
   :target: https://pypi.org/project/cfpq-data/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://github.com/JetBrains-Research/CFPQ_Data/blob/master/LICENSE.txt

CFPQ_Data is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex Graphs and Grammars used for
experimental analysis of Context-Free Path Querying algorithms.

- **Website:** https://jetbrains-research.github.io/CFPQ_Data
- **Tutorial:** https://jetbrains-research.github.io/CFPQ_Data/tutorial.html
- **Documentation:** https://jetbrains-research.github.io/CFPQ_Data/reference/index.html
- **Source Code:** https://github.com/JetBrains-Research/CFPQ_Data
- **Bug Tracker:** https://github.com/JetBrains-Research/CFPQ_Data/issues

Examples
********

Dataset content
---------------

.. code-block:: python

   >>> import cfpq_data
   >>> cfpq_data.DATASET
   ['skos', 'wc', 'generations', 'travel', 'univ', 'atom', 'biomedical', 'bzip', 'foaf', 'people', 'pr', 'funding', 'ls', 'wine', 'pizza', 'gzip', 'core', 'pathways', 'enzyme', 'eclass', 'go_hierarchy', 'go', 'apache', 'init', 'mm', 'geospecies', 'ipc', 'lib', 'block', 'arch', 'crypto', 'security', 'sound', 'net', 'fs', 'drivers', 'postgre', 'kernel', 'taxonomy', 'taxonomy_hierarchy']

Load graph from Dataset
-----------------------

.. code-block:: python

   >>> bzip_path = cfpq_data.download("bzip")
   >>> bzip = cfpq_data.graph_from_csv(bzip_path)
   
How to add a new graph?
***********************

Just create a PR (Pull Request) corresponding to the `"Template for adding a new graph" <https://github.com/JetBrains-Research/CFPQ_Data/blob/master/.github/PULL_REQUEST_TEMPLATE/new_graph.md>`_.
