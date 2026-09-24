.. _graphs:

******
Graphs
******

.. only:: html

   :Release: |release|
   :Date: |today|

How to add a new graph?
-----------------------

Just create a PR (Pull Request) corresponding to the `"Template for adding a new graph" <https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/blob/master/.github/PULL_REQUEST_TEMPLATE/new_graph.md>`_.

.. _graph_file_structure:

File structure
--------------

A graph is distributed as a self-contained archive ``<name>.tar.gz`` that
unpacks to a directory named after the graph. Every archive has the same
fixed structure::

   <name>/
   ├── README.md              description of the graph and of its files
   ├── graph/                 one MatrixMarket file per stored edge label
   │   └── <label>.mtx
   └── queries/               all queries for this graph, one directory each
       ├── README.md          describes every query
       ├── cfpq/              .cnf and/or .rsm representations
       ├── rpq/               .re and/or .rsm representations (regular only)
       └── mcfpq/             .mcfg representations (Datalog-like MCFG syntax)

- ``README.md`` answers the mandatory questions of the contribution
  templates — the templates are the source of truth for the fields, as with
  the statistics conventions.
- ``graph/`` is never empty; ``queries/`` always carries the three class
  directories (possibly empty) and its ``README.md``.
- A query is a directory ``queries/<class>/<query>/`` holding every
  representation of the language — at least one file with a class extension
  (``.cnf`` / ``.rsm`` for CFPQ, ``.re`` / ``.rsm`` for RPQ, ``.mcfg`` for
  MCFPQ) — plus exactly one ``results.mtx`` and nothing else. The same query
  may be represented in several ways (e.g. a CFG and an RSM); all
  representations must define the same language.
- ``results.mtx`` is a Boolean pattern matrix with the same dimensions as
  the graph matrices: entry ``(i, j)`` is present iff some path from node
  ``i`` to node ``j`` satisfies the query. It depends on the language, not
  on the representation.
- ``queries/README.md`` has one ``## <class>/<query>`` section per query
  directory (path relative to ``queries/``), each with a non-empty
  description.
- A query may only use labels of its own graph: every terminal it uses is a
  stored label or the reverse of one (see "Reversed edges" below). An RPQ
  representation in ``.rsm`` must be regular — no box transition may be
  labelled by a nonterminal.

A **partial archive** provides new queries for an existing graph: it unpacks
to a directory named after that graph and contains only ``queries/`` — the
new query directories (same layout) plus a ``README.md`` fragment with one
section per new query. It is validated with
``python utils/check_archive_structure.py <name>.tar.gz --partial`` and
merged into the existing archive with :ref:`merge_archive`.

The pre-migration graphs on the :ref:`old_graphs` page use the old CSV
format instead.

Each file ``graph/<label>.mtx`` is a Boolean pattern matrix that holds
exactly the edges with that label::

   %%MatrixMarket matrix coordinate pattern general
   %%GraphBLAS type bool
   <num_nodes> <num_nodes> <num_edges>
   <tail> <head>
   ...

Node ids are 0-based integers, and the matrix dimensions equal the number of
nodes. A whole directory is loaded by
:obj:`graph_from_mtx_dir <cfpq_data.graphs.readwrite.mtx.graph_from_mtx_dir>`.

Indexed labels
^^^^^^^^^^^^^^

Some graphs have families of labels that differ only in a numeric suffix,
e.g. ``load_0``, ``load_1``, ..., ``load_857``. In the per-graph pages and
in grammars such a family is written once with a placeholder subscript
(``load_f`` or ``load_i``) and a note that lists the index set. Each stored
label has its own file named after the label itself (``load_5.mtx`` holds
the edges labeled ``load_5``).

Reversed edges
^^^^^^^^^^^^^^

For every edge label ``L`` there is a reversed label ``L_r``: an edge ``(u, v)`` labeled
``L`` corresponds to an edge ``(v, u)`` labeled ``L_r``. Reversed edges are
not stored in the archives; they are derived by
:obj:`add_reverse_edges <cfpq_data.graphs.utils.add_reverse_edges>`, and the
"Edges Statistics" tables of the per-graph pages list the stored labels
only.

Contents
--------

The per-category tables include one column per grammar language
applicable to that category. Each cell shows the number of vertex pairs
reachable with respect to the respective language (i.e. the number of
pairs ``(u, v)`` for which some string in the language labels a path from
:math:`u` to :math:`v`). The count depends on the language, not on a
particular grammar: several grammars may generate the same language and
yield the same count. A cell reading "not available" means the value has
not been computed yet; an empty cell means the grammar does not apply to
that graph. Each table also has a ``Size (MB)`` column: the download size
of the graph's archive, in megabytes.

The canonical grammar behind each column is documented once on the
respective category page, in its "Canonical grammars" section — a grammar
is canonical for the whole category, so the per-graph pages do not repeat
it.

.. list-table::
   :header-rows: 1

   * - Source area
     - Number of graphs
   * - :ref:`graphs_c_alias_analysis`
     - 20
   * - :ref:`graphs_rdf`
     - 20
   * - :ref:`graphs_java_points_to`
     - 21
   * - :ref:`graphs_field_sensitive_alias`
     - 10
   * - :ref:`graphs_context_sensitive_data_flow`
     - 10
   * - :ref:`graphs_data_provenance`
     - 18
   * - :ref:`graphs_name_resolution`
     - 4
   * - :ref:`graphs_biological_uniprot`
     - 10

.. toctree::
   :maxdepth: 1

   c_alias_analysis
   rdf
   java_points_to
   field_sensitive_alias
   context_sensitive_data_flow
   data_provenance
   name_resolution
   biological_uniprot
