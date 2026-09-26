.. _indexed_grammars:

Indexed Grammars
================

.. only:: html

   :Release: |release|
   :Date: |today|

What are indexed grammars?
--------------------------

An **indexed grammar** (also called a *block-matrix grammar* or *grammar with
indexed nonterminals*) is a context-free grammar in which certain symbols carry
an integer index. The index ties together edges that must match on the same
"slot" — a field number in points-to analysis, a call-site in dataflow
analysis, etc.

Instead of explicitly instantiating one production per index (which explodes
the grammar size), the indexed form keeps a single *template* production with
an ``_i`` placeholder:

.. code-block:: text

   PTh    load_i    Al_st_PTh_i      # one template production
   Al_st_PTh_i  Al  st_PTh_i
   st_PTh_i store_i PTh

At index :math:`k = 0`, this means: ``PTh -> load_0 Al_st_PTh_0`` and
``Al_st_PTh_0 -> Al st_PTh_0`` and ``st_PTh_0 -> store_0 PTh``. The solver
builds a separate relation (block) per index and composes only blocks at
matching indices — giving O(n² · b) complexity instead of O(n² · b²) for the
explicit form.

Syntax rules
------------

+--------------------------------------+------------------------------------------+
| Syntax                               | Meaning                                  |
+======================================+==========================================+
| ``load_i``                           | Indexed terminal: "load from field *k*"  |
+--------------------------------------+------------------------------------------+
| ``load_r_i``                         | Reversed indexed terminal: reverse of    |
|                                      | ``load_i``; graph label is ``load_k_r``  |
+--------------------------------------+------------------------------------------+
| ``Al_st_PTh_i``                      | Indexed nonterminal (ends in ``_i``)     |
+--------------------------------------+------------------------------------------+
| ``PT``, ``alloc``, ``assign``        | Non-indexed symbols (no suffix)          |
+--------------------------------------+------------------------------------------+
| Bare nonterminal line (e.g. ``V``)   | ε-production (identity relation)         |
+--------------------------------------+------------------------------------------+

In a production, all indexed symbols on the same side share the **same index**.
For example, ``PTh -> load_i Al_st_PTh_i`` means: for each k, compose the
relation of ``load_k`` with the relation of ``Al_st_PTh_k``.

The start symbol must NOT be indexed.

File formats
------------

**.cnf template** (compact, stored in graph archives):

.. code-block:: text

   PT	PTh	alloc
   PTh	load_i	Al_st_PTh_i
   Al_st_PTh_i	Al	st_PTh_i
   st_PTh_i	store_i	PTh
   ...

   Count:
   PT

**.g edge list** (input to FastMatrixCFPQ, 4 columns for indexed edges):

.. code-block:: text

   5 6 load_i 0
   6 5 load_r_i 0
   7 8 store_i 0
   8 7 store_r_i 0
   1 2 alloc

The 4th column is the index. Non-indexed edges have only 3 columns.

Materializing for non-indexed CFPQ tools
----------------------------------------

Many CFPQ algorithms (classic inside/outside fixpoint, matrix-based without
block support) require an **explicit** grammar where every index is spelled
out. The :func:`cfpq_data.queries.cfpq.readwrite.cnf_template.materialize_grammar`
function performs this expansion:

.. code-block:: python

   from cfpq_data import *
   import networkx as nx, pathlib, tempfile

   g = nx.MultiDiGraph()
   g.add_edges_from(
       [(0, 1, {"label": "load_0"}), (1, 2, {"label": "store_0"}),
        (0, 3, {"label": "load_1"}), (3, 2, {"label": "store_1"}),
        (0, 4, {"label": "alloc"})]
   )
   p = pathlib.Path(tempfile.mkdtemp()) / "g.cnf"
   p.write_text(
       "PT\tPTh\talloc\nPTh\tassign\n"
       "PTh\tload_i\tAl_st_PTh_i\nAl_st_PTh_i\tAl\tst_PTh_i\n"
       "st_PTh_i\tstore_i\tPTh\nAl\tPT\n\nCount:\nPT"
   )
   cfg = materialize_grammar(p, g)
   sorted(s.value for s in cfg.terminals)
   # ['alloc', 'assign', 'load_0', 'load_1', 'store_0', 'store_1']

The resulting CFG has one production per (production template × index) pair.
Terminals become ``load_0``, ``load_1``, ... and indexed nonterminals become
``Al_st_PTh_0``, ``st_PTh_0``, ...

When to use which form
----------------------

.. list-table::
   :header-rows: 1

   * - Use the **indexed template** (``.cnf`` with ``_i``) when:
     - Use the **materialized explicit** grammar (from ``materialize_grammar``) when:
   * - The solver supports block matrices (FastMatrixCFPQ)
     - The solver does NOT support indexed grammars (most classic CFPQ tools)
   * - You want O(n²·b) performance
     - The graph is small enough that the explicit grammar fits in memory
   * - You are storing/serving the grammar in an archive
     - You need to inspect or debug individual per-index productions

Grammars with indexed symbols in this dataset
---------------------------------------------

.. list-table::
   :header-rows: 1

   * - Grammar file
     - Indexed terminals
     - Index meaning
     - Graphs
   * - ``java_points_to.cnf``
     - ``load_i``, ``store_i``, ``load_r_i``, ``store_r_i``
     - field number
     - 21 Java points-to graphs
   * - ``vf.cnf``
     - ``call_i``, ``ret_i``
     - call-site number
     - 10 value-flow graphs
   * - ``aa.cnf``
     - ``f_i``, ``fbar_i``
     - field number
     - 10 field-sensitive alias graphs
   * - ``name_resolution.cnf``
     - ``psh_i``, ``vpsh_i``, ``vpp_i``, ``pp_i``
     - scope depth
     - 4 name-resolution graphs
