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

C alias analysis
^^^^^^^^^^^^^^^^

* :ref:`apache`
* :ref:`arch`
* :ref:`block`
* :ref:`bzip`
* :ref:`crypto`
* :ref:`drivers`
* :ref:`fs`
* :ref:`gzip`
* :ref:`init`
* :ref:`ipc`
* :ref:`kernel`
* :ref:`lib`
* :ref:`ls`
* :ref:`mm`
* :ref:`net`
* :ref:`postgre`
* :ref:`pr`
* :ref:`security`
* :ref:`sound`
* :ref:`wc`

RDF
^^^

* :ref:`atom`
* :ref:`biomedical`
* :ref:`core`
* :ref:`eclass`
* :ref:`enzyme`
* :ref:`foaf`
* :ref:`funding`
* :ref:`generations`
* :ref:`geospecies`
* :ref:`go`
* :ref:`go_hierarchy`
* :ref:`pathways`
* :ref:`people`
* :ref:`pizza`
* :ref:`skos`
* :ref:`taxonomy`
* :ref:`taxonomy_hierarchy`
* :ref:`travel`
* :ref:`univ`
* :ref:`wine`

Java points-to graphs
^^^^^^^^^^^^^^^^^^^^^

* :ref:`avrora`
* :ref:`batik`
* :ref:`commons_io`
* :ref:`commons_lang3`
* :ref:`eclipse`
* :ref:`fop`
* :ref:`gson`
* :ref:`guava`
* :ref:`h2`
* :ref:`jackson`
* :ref:`junit5`
* :ref:`jython`
* :ref:`luindex`
* :ref:`lusearch`
* :ref:`mockito`
* :ref:`pmd`
* :ref:`sunflow`
* :ref:`tomcat`
* :ref:`tradebeans`
* :ref:`tradesoap`
* :ref:`xalan`

Field-Sensitive Alias
^^^^^^^^^^^^^^^^^^^^^

* :ref:`cactus_field_sensitive_alias`
* :ref:`imagick_field_sensitive_alias`
* :ref:`leela_field_sensitive_alias`
* :ref:`nab_field_sensitive_alias`
* :ref:`omnetpp_field_sensitive_alias`
* :ref:`parest_field_sensitive_alias`
* :ref:`perlbench_field_sensitive_alias`
* :ref:`povray_field_sensitive_alias`
* :ref:`x264_field_sensitive_alias`
* :ref:`xz_field_sensitive_alias`

Context-Sensitive Data-Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :ref:`cactus`
* :ref:`imagick`
* :ref:`leela`
* :ref:`nab`
* :ref:`omnetpp`
* :ref:`parest`
* :ref:`perlbench`
* :ref:`povray`
* :ref:`x264`
* :ref:`xz`

Data Provenance
^^^^^^^^^^^^^^^

* :ref:`provenance_airflow`
* :ref:`provenance_celery`
* :ref:`provenance_click`
* :ref:`provenance_django`
* :ref:`provenance_fastapi`
* :ref:`provenance_flask`
* :ref:`provenance_httpx`
* :ref:`provenance_itsdangerous`
* :ref:`provenance_jinja`
* :ref:`provenance_pandas`
* :ref:`provenance_pluggy`
* :ref:`provenance_requests`
* :ref:`provenance_sampleproject`
* :ref:`provenance_scikit_learn`
* :ref:`provenance_sphinx`
* :ref:`provenance_superset`
* :ref:`provenance_wikipedia_provenance`
* :ref:`provenance_zulip`

Name Resolution
^^^^^^^^^^^^^^^

* :ref:`name_resolution_jiaozi`
* :ref:`name_resolution_jsonpath`
* :ref:`name_resolution_libgdx`
* :ref:`name_resolution_shattered_pixel_dungeon`

Biological graphs from UniProt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :ref:`unigraph_1`
* :ref:`unigraph_10`
* :ref:`unigraph_2`
* :ref:`unigraph_3`
* :ref:`unigraph_4`
* :ref:`unigraph_5`
* :ref:`unigraph_6`
* :ref:`unigraph_7`
* :ref:`unigraph_8`
* :ref:`unigraph_9`

.. applicable-graphs:end
