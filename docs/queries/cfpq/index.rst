.. _cfpq_queries:

****
CFPQ
****

.. only:: html

   :Release: |release|
   :Date: |today|

Context-free path queries (CFPQ) constrain the paths of a labeled graph by a
context-free language: a pair :math:`(u, v)` is reachable if some path from
:math:`u` to :math:`v` is labeled by a string of the language. A query is
specified by a grammar template instantiated per graph from its stored labels;
one query may carry several representations of the same language (a CFG or an
RSM). The graph catalog is shared across all query classes — the "Applicable
graphs" list below cross-links the per-graph pages without duplicating them.

.. toctree::
   :hidden:
   :glob:

   data/*
   indexed_grammars

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

The static-analysis grammars use a compact indexed form; see
:doc:`indexed_grammars`.

Applicable graphs
-----------------

Graphs from the shared :ref:`catalog <graphs>` that carry at least one CFPQ
query.

.. applicable-graphs:begin

.. applicable-graphs:end
