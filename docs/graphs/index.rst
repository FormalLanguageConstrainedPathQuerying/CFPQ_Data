.. _graphs:

******
Graphs
******

.. only:: html

   :Release: |release|
   :Date: |today|

.. _contributing_data:

Contributing data
-----------------

New data — graphs, queries, grammars — enters the dataset through a single
`"CONTRIBUTE NEW DATA" issue <https://github.com/FormalLanguageConstrainedPathQuerying/FLPQ_Data/blob/dev/.github/ISSUE_TEMPLATE/new-data-template.md>`_:
you prepare one or more archives (one graph each), validate them, publish
them (e.g. to Google Drive), and open the issue with the links, the
validation output, the SHA256 of every archive, and the motivation. The
maintainers upload the archives and merge them into the dataset — no pull
request is needed.

Contribution cases
^^^^^^^^^^^^^^^^^^

The issue template's "Contribution type" section lists the four contribution
cases — new graph(s) for an existing or a new category, with an existing or
a new grammar, and new queries for existing graph(s) — and what each
requires; its remaining sections carry every required field (statistics,
grammar definitions, category description). A set of graphs for a category
goes into one issue as several archives (one graph per archive).

Validation
^^^^^^^^^^

Every archive must pass the structure checker before it is shared::

   flpq-check-archive <name>.tar.gz            # full archive
   flpq-check-archive <name>.tar.gz --partial  # partial archive

The issue carries the pasted output of this command per archive, the
archive's SHA256, and the FLPQ_Data version used; the template has the
recipe — ``pip install flpq-data`` installs the checker.

Consistency invariants
^^^^^^^^^^^^^^^^^^^^^^

- No graph without at least one query.
- No query without reference results (``results.mtx``).
- No item without description and motivation: every graph is described in
  its archive ``README.md``, every query in ``queries/README.md``, and the
  issue states why each new graph, grammar, or category is useful to other
  users.

Not accepted via this flow
^^^^^^^^^^^^^^^^^^^^^^^^^^

The issue template's "Not accepted via this flow" section lists the declined
cases: a grammar or query provided outside an archive (without reference
results), updates to an existing graph, a new representation of an existing
query, and more than one graph inside a single archive.

.. _graph_format_conversion:

Format conversion
-----------------

Graphs can be converted between the formats below without building an
in-memory NetworkX graph: the conversion runs over an **edge stream** — a
lazy iterator of ``(u, label, v)`` tuples in the TXT ``FROM LABEL TO`` order
— with one streaming reader and one streaming writer per format, composed by
:obj:`convert_graph <flpq_data.graphs.converters.convert_graph>`. This keeps
peak memory at O(1) for the common case (an MTX directory to TXT or ``.g``
text), where routing through a ``networkx.MultiDiGraph`` costs several
gigabytes on the largest graphs (#138: ~4 GiB of RAM for ~100 MB of input).

Formats
^^^^^^^

.. list-table::
   :header-rows: 1

   * - Format
     - On disk
     - Node ids
     - Direction
   * - ``mtx``
     - a directory with one Boolean MatrixMarket file per label (the :doc:`/file_structure` layout)
     - non-negative integers
     - both
   * - ``txt``
     - one edge per line, ``FROM LABEL TO``, optional quoting
     - strings
     - both
   * - ``rdf``
     - Turtle (the encoding below)
     - strings
     - both
   * - ``g``
     - FastMatrixCFPQ ``.g`` text: ``u v label`` lines plus auto-generated reverse edges; an indexed family ``X_0, X_1, ...`` collapses to ``X_i`` with the index as a fourth column
     - non-negative integers
     - write-only
   * - ``graph``
     - not on disk — an in-memory ``networkx.MultiDiGraph``
     - whatever the graph holds
     - read-only

Memory characteristics
^^^^^^^^^^^^^^^^^^^^^^

- Every reader and writer streams: one edge is held in memory at a time, so
  ``mtx`` → ``txt`` / ``g`` / ``rdf`` runs in O(1) RAM (the #138 case).
- Writing ``mtx`` is a single pass over the source with one temporary file
  per label (O(1) RAM, O(E) disk); it requires integer node ids (digit
  strings are accepted, anything else is an error).
- An ``rdf`` **source** is materialized: rdflib has no streaming parser, so
  reading RDF costs O(E) RAM. It is the only unavoidable materialization.

RDF encoding
^^^^^^^^^^^^

The RDF writer emits valid RDF 1.1 Turtle, one triple per line::

   <urn:flpq:node:0> <urn:flpq:label:load_5> <urn:flpq:node:1> .

Nodes are IRIs ``urn:flpq:node:<id>``, predicates IRIs
``urn:flpq:label:<label>``, with the variable components percent-encoded; the
writer streams line by line without an in-memory RDF store. The reader accepts
this encoding and, for backwards compatibility, the legacy form that older
versions of ``graph_to_rdf`` emitted — blank-node endpoints with a
``Literal`` predicate, which is not valid RDF 1.1 (predicates must be IRIs)
and only round-tripped inside rdflib.

RDF is a set of triples: parallel edges with identical ``(u, label, v)``
collapse on write — a format-inherent limitation the legacy form shared. The
other formats preserve parallel edges.

The NetworkX boundary
^^^^^^^^^^^^^^^^^^^^^

NetworkX stays where it earns its place: the random graph generators, the
adjacency-based utilities (:obj:`add_reverse_edges <flpq_data.graphs.utils.add_reverse_edges>`,
:obj:`filter_edges <flpq_data.graphs.utils.filter_edges>`, ...), query
materialization, and the existing ``graph_from_*`` / ``graph_to_*`` API, which
builds or consumes a ``networkx.MultiDiGraph``. The conversion path above
never materializes one.

CSV removal
^^^^^^^^^^^

The former CSV format (one edge per line, ``from to label``) is removed in
6.0.0: it was the same line-per-edge format as TXT with only the column order
different — a footgun, not a feature — and no dataset archive uses it
(archives are MTX-only). Use ``txt`` instead; ``graph_from_csv`` /
``graph_to_csv`` are gone, and the ``pandas`` dependency that only they used
is dropped.

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
