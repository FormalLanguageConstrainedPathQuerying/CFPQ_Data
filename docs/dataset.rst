.. _dataset_catalog:

*******
Dataset
*******

.. only:: html

   :Release: |release|
   :Date: |today|

The dataset catalog: graphs and queries for experimental analysis of
formal-language-constrained path querying. The graph catalog is shared by all
query classes; each class has its own section with its query templates and the
list of applicable graphs.

.. toctree::
   :maxdepth: 1

   graphs/index
   queries/cfpq/index
   queries/rpq/index
   queries/mcfpq/index
   reachable_pairs

How to add a new grammar?
-------------------------

Grammars are added together with the data they apply to — create an ``Issue`` corresponding to the `"CONTRIBUTE NEW DATA" issue template <https://github.com/FormalLanguageConstrainedPathQuerying/FLPQ_Data/blob/master/.github/ISSUE_TEMPLATE/new-data-template.md>`_ (the "Queries and grammars" section). A grammar is accepted only if it is instantiated as at least one query with reference results in a contributed archive.
