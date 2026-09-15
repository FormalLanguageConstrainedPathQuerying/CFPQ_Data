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
- **Changelog:** https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/blob/master/CHANGELOG.md

Installation
************

Install from PyPI with ``pip``::

   pip install cfpq-data

Requires Python 3.11–3.13; see the `Install <https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/install.html>`_ page for details.

What's inside
**************

CFPQ_Data bundles **113 labeled directed graphs** across eight families — C alias analysis, RDF/OWL datasets, Java points-to, field-sensitive aliasing, context-sensitive data-flow, data provenance, name resolution (stack graphs), and biological graphs from UniProt — together with the context-free grammars used to query them. Each graph ships as a per-label MatrixMarket archive; see the `Graphs <https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html>`_ page for statistics and download links.

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

For developers
**************

To work on CFPQ_Data itself, set up the development environment (Poetry)::

   poetry install --with dev,test,docs
   poetry run pip install .

and run the main local checks that CI enforces — tests, style, and the docs
build::

   poetry run pytest --doctest-modules -vv -s cfpq_data tests
   pre-commit run --all-files
   poetry run make -C docs html

The full developer guide — development setup, pre-commit, the test pipeline,
docs build and deployment, the package release process, and contribution
guidelines — is on the `Developer <https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/developer.html>`_ page.

How to add a new graph?
***********************

Just create

- an ``Issue`` corresponding to the `"Issue template for adding a new graph" <https://github.com/formallanguageconstrainedpathquerying/CFPQ_Data/blob/master/.github/ISSUE_TEMPLATE/graph-add-template.md>`_.
- a ``Pull Request`` corresponding to the `"Pull request template for adding a new graph" <https://github.com/formallanguageconstrainedpathquerying/CFPQ_Data/blob/master/.github/PULL_REQUEST_TEMPLATE/new_graph.md>`_.

Citation
********

If you use CFPQ_Data in your work, please cite it — see the `Citation <https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/about.html#citation>`_ section on the About page for BibTeX entries.

Licensing
*********

The **code** (package source, documentation, and tooling) is licensed under
Apache-2.0 (`LICENSE.txt <https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/blob/master/LICENSE.txt>`_). The **dataset** (graphs, grammars, and benchmarks) is licensed under CC-BY 4.0 (`LICENSE-DATA.txt <https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/blob/master/LICENSE-DATA.txt>`_).
