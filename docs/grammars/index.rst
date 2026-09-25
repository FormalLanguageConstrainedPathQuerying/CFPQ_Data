.. _grammar_templates:

********
Grammars
********

.. only:: html

   :Release: |release|
   :Date: |today|

How to add a new grammar?
-------------------------

Just create a PR (Pull Request) corresponding to the `"Template for adding a new grammar" <https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/blob/master/.github/PULL_REQUEST_TEMPLATE/new_grammar.md>`_.

----

.. toctree::
   :hidden:
   :glob:

   data/*

Grammar templates
-----------------

.. list-table::
   :header-rows: 1

   * - Grammar
     - Class
     - Kind
   * - :ref:`nested_parentheses`
     - Context-Free
     - Hierarchical
   * - :ref:`dyck`
     - Context-Free
     - Hierarchical
   * - :ref:`c_alias`
     - Context-Free
     - Static Analysis
   * - :ref:`java_points-to`
     - Context-Free
     - Static Analysis
   * - :ref:`reachability`
     - Regular
     - General
   * - :ref:`label_star`
     - Regular
     - General
