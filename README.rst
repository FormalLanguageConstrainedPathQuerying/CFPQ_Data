CFPQ_Data
=========

.. image:: https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/actions/workflows/tests.yml/badge.svg?branch=master
   :target: https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/actions/workflows/tests.yml

.. image:: https://codecov.io/gh/FormalLanguageConstrainedPathQuerying/CFPQ_Data/branch/master/graph/badge.svg?token=6IAZM6KZT7
   :target: https://codecov.io/gh/FormalLanguageConstrainedPathQuerying/CFPQ_Data

.. image:: https://img.shields.io/pypi/v/cfpq-data.svg
   :target: https://pypi.org/project/cfpq-data/

.. image:: https://img.shields.io/pypi/pyversions/cfpq-data.svg
   :target: https://pypi.org/project/cfpq-data/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/blob/master/LICENSE.txt

CFPQ_Data is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex Graphs and Grammars used for
experimental analysis of Context-Free Path Querying algorithms.

- **Website:** https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data
- **Tutorial:** https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html
- **Documentation:** https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/index.html
- **Source Code:** https://github.com/formallanguageconstrainedpathquerying/CFPQ_Data
- **Bug Tracker:** https://github.com/formallanguageconstrainedpathquerying/CFPQ_Data/issues

Examples
********

Dataset content
---------------

.. code-block:: python

   >>> import cfpq_data
   >>> cfpq_data.DATASET[:3]
   ['skos', 'wc', 'generations']

The full list of graphs, with statistics and download links, is on the
`Graphs <https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html>`_ page.

Load graph from Dataset
-----------------------

.. code-block:: python

   >>> bzip_path = cfpq_data.download("bzip")
   >>> bzip = cfpq_data.graph_from_mtx_dir(bzip_path / "graph")

How to add a new graph?
***********************

Just create

- an ``Issue`` corresponding to the `"Issue template for adding a new graph" <https://github.com/formallanguageconstrainedpathquerying/CFPQ_Data/blob/master/.github/ISSUE_TEMPLATE/graph-add-template.md>`_.
- a ``Pull Request`` corresponding to the `"Pull request template for adding a new graph" <https://github.com/formallanguageconstrainedpathquerying/CFPQ_Data/blob/master/.github/PULL_REQUEST_TEMPLATE/new_graph.md>`_.
