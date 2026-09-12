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

A graph is distributed as an archive ``<name>.tar.gz`` that unpacks to a
directory named after the graph:

- ``README.md`` — the description of the graph and of its files;
- ``grammar/`` — the grammars for this graph in the cnf format (if any);
- ``graph/`` — one MatrixMarket file per edge label.

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
`graph_from_mtx_dir <cfpq_data.graphs.readwrite.mtx.graph_from_mtx_dir>`_.

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

For every edge label ``L`` there is a reversed label ``L_r`` (written
:math:`\overline{L}` in the per-graph pages): an edge ``(u, v)`` labeled
``L`` corresponds to an edge ``(v, u)`` labeled ``L_r``. Reversed edges are
not stored in the archives; they are derived by
`add_reverse_edges <cfpq_data.graphs.utils.add_reverse_edges>`_, and the
"Edges Statistics" tables of the per-graph pages list the stored labels
only.

----

.. toctree::
   :hidden:
   :caption: C alias analysis

   data/wc
   data/bzip
   data/pr
   data/ls
   data/gzip
   data/apache
   data/init
   data/mm
   data/ipc
   data/lib
   data/block
   data/arch
   data/crypto
   data/security
   data/sound
   data/net
   data/fs
   data/drivers
   data/postgre
   data/kernel

.. toctree::
   :hidden:
   :caption: RDF

   data/generations
   data/travel
   data/skos
   data/univ
   data/foaf
   data/atom
   data/people
   data/biomedical
   data/pizza
   data/wine
   data/funding
   data/core
   data/pathways
   data/go_hierarchy
   data/enzyme
   data/geospecies
   data/go
   data/eclass
   data/taxonomy_hierarchy
   data/taxonomy

.. toctree::
   :hidden:
   :caption: Java points-to graphs

   data/gson
   data/sunflow
   data/lusearch
   data/luindex
   data/avrora
   data/mockito
   data/commons_io
   data/commons_lang3
   data/eclipse
   data/h2
   data/pmd
   data/xalan
   data/junit5
   data/batik
   data/fop
   data/tomcat
   data/guava
   data/jackson
   data/jython
   data/tradebeans
   data/tradesoap

.. toctree::
   :hidden:
   :caption: Field-Sensitive Alias

   data/xz_field_sensitive_alias
   data/nab_field_sensitive_alias
   data/leela_field_sensitive_alias
   data/povray_field_sensitive_alias
   data/x264_field_sensitive_alias
   data/cactus_field_sensitive_alias
   data/parest_field_sensitive_alias
   data/perlbench_field_sensitive_alias
   data/imagick_field_sensitive_alias
   data/omnetpp_field_sensitive_alias

.. toctree::
   :hidden:
   :caption: Context-Sensitive Data-Flow

   data/xz
   data/nab
   data/leela
   data/x264
   data/parest
   data/imagick
   data/povray
   data/cactus
   data/omnetpp
   data/perlbench

.. toctree::
   :hidden:
   :caption: Data Provenance

   data/provenance_sampleproject
   data/provenance_wikipedia_provenance
   data/provenance_pluggy
   data/provenance_itsdangerous
   data/provenance_requests
   data/provenance_httpx
   data/provenance_click
   data/provenance_jinja
   data/provenance_flask
   data/provenance_fastapi
   data/provenance_celery
   data/provenance_scikit_learn
   data/provenance_sphinx
   data/provenance_pandas
   data/provenance_django
   data/provenance_zulip
   data/provenance_superset
   data/provenance_airflow

.. toctree::
   :hidden:
   :caption: Name Resolution

   data/name_resolution_jiaozi
   data/name_resolution_jsonpath
   data/name_resolution_shattered_pixel_dungeon
   data/name_resolution_libgdx

.. toctree::
   :hidden:
   :caption: Biological graphs from UniProt

   data/unigraph_1
   data/unigraph_2
   data/unigraph_3
   data/unigraph_4
   data/unigraph_5
   data/unigraph_6
   data/unigraph_7
   data/unigraph_8
   data/unigraph_9
   data/unigraph_10

Graphs
------

Contents
^^^^^^^^

The per-category tables below include one column per grammar language
applicable to that category. Each cell shows the number of vertex pairs
reachable with respect to the respective language (i.e. the number of
pairs ``(u, v)`` for which some string in the language labels a path from
:math:`u` to :math:`v`). The count depends on the language, not on a
particular grammar: several grammars may generate the same language and
yield the same count. A cell reading "not available" means the value has
not been computed yet; an empty cell means the grammar does not apply to
that graph.

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

.. _graphs_c_alias_analysis:

C alias analysis
^^^^^^^^^^^^^^^^

Points-to (alias) graphs for a suite of C programs, built by demand-driven
alias analysis as in `"Demand-driven alias analysis for C" <https://dl.acm.org/doi/10.1145/1328897.1328464>`_.
Nodes are program entities and edges are the aliasing and flow relations
discovered for each program.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - c_alias
     - Download
   * - :ref:`wc`
     - 332
     - 269
     - 156
     - `wc.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/wc.tar.gz>`_ 📥
   * - :ref:`bzip`
     - 632
     - 556
     - 315
     - `bzip.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/bzip.tar.gz>`_ 📥
   * - :ref:`pr`
     - 815
     - 692
     - 385
     - `pr.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/pr.tar.gz>`_ 📥
   * - :ref:`ls`
     - 1687
     - 1453
     - 854
     - `ls.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/ls.tar.gz>`_ 📥
   * - :ref:`gzip`
     - 2687
     - 2293
     - 1458
     - `gzip.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/gzip.tar.gz>`_ 📥
   * - :ref:`apache`
     - 1721418
     - 1510411
     - 92806768
     - `apache.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/apache.tar.gz>`_ 📥
   * - :ref:`init`
     - 2446224
     - 2112809
     - 3783769
     - `init.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/init.tar.gz>`_ 📥
   * - :ref:`mm`
     - 2538243
     - 2191079
     - 3990305
     - `mm.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/mm.tar.gz>`_ 📥
   * - :ref:`ipc`
     - 3401022
     - 2931498
     - 5249389
     - `ipc.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/ipc.tar.gz>`_ 📥
   * - :ref:`lib`
     - 3401355
     - 2931880
     - 5276303
     - `lib.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/lib.tar.gz>`_ 📥
   * - :ref:`block`
     - 3423234
     - 2951393
     - 5351409
     - `block.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/block.tar.gz>`_ 📥
   * - :ref:`arch`
     - 3448422
     - 2970242
     - 5339563
     - `arch.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/arch.tar.gz>`_ 📥
   * - :ref:`crypto`
     - 3464970
     - 2988387
     - 5428237
     - `crypto.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/crypto.tar.gz>`_ 📥
   * - :ref:`security`
     - 3479982
     - 3003326
     - 5593387
     - `security.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/security.tar.gz>`_ 📥
   * - :ref:`sound`
     - 3528861
     - 3049732
     - 6085269
     - `sound.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/sound.tar.gz>`_ 📥
   * - :ref:`net`
     - 4039470
     - 3500141
     - 8833403
     - `net.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/net.tar.gz>`_ 📥
   * - :ref:`fs`
     - 4177416
     - 3609373
     - 9646475
     - `fs.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/fs.tar.gz>`_ 📥
   * - :ref:`drivers`
     - 4273803
     - 3707769
     - 18825025
     - `drivers.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/drivers.tar.gz>`_ 📥
   * - :ref:`postgre`
     - 5203419
     - 4678543
     - 90661446
     - `postgre.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/postgre.tar.gz>`_ 📥
   * - :ref:`kernel`
     - 11254434
     - 9484213
     - 16747731
     - `kernel.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/kernel.tar.gz>`_ 📥
.. _graphs_rdf:

RDF
^^^

Labeled directed graphs built from RDF / OWL datasets, where nodes are
resources and edges are predicates; they support studying context-free path
queries over RDF as in `"Context-Free Path Queries on RDF Graphs" <https://arxiv.org/abs/1506.00743>`_.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - subClassOf
     - subClassOf_type
     - type
     - broaderTransitive
     - Download
   * - :ref:`generations`
     - 129
     - 273
     - 0
     - 12
     - 12
     -
     - `generations.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/generations.tar.gz>`_ 📥
   * - :ref:`travel`
     - 131
     - 277
     - 33
     - 52
     - 19
     -
     - `travel.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/travel.tar.gz>`_ 📥
   * - :ref:`skos`
     - 144
     - 252
     - 1
     - 30
     - 29
     -
     - `skos.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/skos.tar.gz>`_ 📥
   * - :ref:`univ`
     - 179
     - 293
     - 17
     - 25
     - 6
     -
     - `univ.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/univ.tar.gz>`_ 📥
   * - :ref:`foaf`
     - 256
     - 631
     - 7
     - 36
     - 29
     -
     - `foaf.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/foaf.tar.gz>`_ 📥
   * - :ref:`atom`
     - 291
     - 425
     - 2
     - 6
     - 4
     -
     - `atom.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/atom.tar.gz>`_ 📥
   * - :ref:`people`
     - 337
     - 640
     - 24
     - 51
     - 29
     -
     - `people.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/people.tar.gz>`_ 📥
   * - :ref:`biomedical`
     - 341
     - 459
     - 43
     - 47
     - 4
     -
     - `biomedical.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/biomedical.tar.gz>`_ 📥
   * - :ref:`pizza`
     - 671
     - 1980
     - 1334
     - 1356
     - 20
     -
     - `pizza.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/pizza.tar.gz>`_ 📥
   * - :ref:`wine`
     - 733
     - 1839
     - 499
     - 565
     - 65
     -
     - `wine.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/wine.tar.gz>`_ 📥
   * - :ref:`funding`
     - 778
     - 1086
     - 27
     - 58
     - 31
     -
     - `funding.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/funding.tar.gz>`_ 📥
   * - :ref:`core`
     - 1323
     - 2752
     - 143
     - 204
     - 61
     -
     - `core.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/core.tar.gz>`_ 📥
   * - :ref:`pathways`
     - 6238
     - 12363
     - 883
     - 884
     - 2
     -
     - `pathways.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/pathways.tar.gz>`_ 📥
   * - :ref:`go_hierarchy`
     - 45007
     - 490109
     - 588976
     - 588976
     - 0
     -
     - `go_hierarchy.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/go_hierarchy.tar.gz>`_ 📥
   * - :ref:`enzyme`
     - 48815
     - 86543
     - 394
     - 396
     - 3
     - 14267542
     - `enzyme.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/enzyme.tar.gz>`_ 📥
   * - :ref:`geospecies`
     - 450609
     - 2201532
     - 0
     - 85
     - 85
     - 226669749
     - `geospecies.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/geospecies.tar.gz>`_ 📥
   * - :ref:`go`
     - 582929
     - 1437437
     - 640305
     - 640316
     - 9
     -
     - `go.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/go.tar.gz>`_ 📥
   * - :ref:`eclass`
     - 239111
     - 360248
     - 90988
     - 90994
     - 6
     -
     - `eclass.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/eclass.tar.gz>`_ 📥
   * - :ref:`taxonomy_hierarchy`
     - 2112625
     - 32876289
     - 5351657
     - 5351657
     - 0
     -
     - `taxonomy_hierarchy.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/taxonomy_hierarchy.tar.gz>`_ 📥
   * - :ref:`taxonomy`
     - 5728398
     - 14922125
     - 151703
     - 151706
     - 4
     -
     - `taxonomy.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/taxonomy.tar.gz>`_ 📥
.. _graphs_java_points_to:

Java points-to graphs
^^^^^^^^^^^^^^^^^^^^^

Exhaustive, field-sensitive points-to graphs for Java programs, produced by
the analysis of `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Edges are the points-to relations (allocations, assignments, loads, stores,
calls, returns) together with their reverses.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - java_points_to
     - Download
   * - :ref:`gson`
     - 14114
     - 34934
     - 56325
     - `gson.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/gson.tar.gz>`_ 📥
   * - :ref:`sunflow`
     - 15464
     - 15957
     - 35209
     - `sunflow.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/sunflow.tar.gz>`_ 📥
   * - :ref:`lusearch`
     - 15774
     - 14994
     - 43719
     - `lusearch.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/lusearch.tar.gz>`_ 📥
   * - :ref:`luindex`
     - 18532
     - 17375
     - 176051
     - `luindex.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/luindex.tar.gz>`_ 📥
   * - :ref:`avrora`
     - 24690
     - 25196
     - 192790
     - `avrora.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/avrora.tar.gz>`_ 📥
   * - :ref:`mockito`
     - 25436
     - 62388
     - 16169
     - `mockito.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/mockito.tar.gz>`_ 📥
   * - :ref:`commons_io`
     - 26188
     - 62428
     - 24020
     - `commons_io.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/commons_io.tar.gz>`_ 📥
   * - :ref:`commons_lang3`
     - 40970
     - 96854
     - 27553
     - `commons_lang3.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/commons_lang3.tar.gz>`_ 📥
   * - :ref:`eclipse`
     - 41383
     - 40200
     - 378989
     - `eclipse.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/eclipse.tar.gz>`_ 📥
   * - :ref:`h2`
     - 44717
     - 56683
     - 2611022
     - `h2.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/h2.tar.gz>`_ 📥
   * - :ref:`pmd`
     - 54444
     - 59329
     - 137120
     - `pmd.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/pmd.tar.gz>`_ 📥
   * - :ref:`xalan`
     - 58476
     - 62758
     - 1138776
     - `xalan.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/xalan.tar.gz>`_ 📥
   * - :ref:`junit5`
     - 59818
     - 149370
     - 129598
     - `junit5.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/junit5.tar.gz>`_ 📥
   * - :ref:`batik`
     - 60175
     - 63089
     - 868368
     - `batik.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/batik.tar.gz>`_ 📥
   * - :ref:`fop`
     - 86183
     - 83016
     - 1984072
     - `fop.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/fop.tar.gz>`_ 📥
   * - :ref:`tomcat`
     - 111327
     - 110884
     - 3792543
     - `tomcat.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/tomcat.tar.gz>`_ 📥
   * - :ref:`guava`
     - 129562
     - 336232
     - 26384496
     - `guava.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/guava.tar.gz>`_ 📥
   * - :ref:`jackson`
     - 149404
     - 395356
     - 3108775
     - `jackson.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jackson.tar.gz>`_ 📥
   * - :ref:`jython`
     - 191895
     - 260034
     - 561720
     - `jython.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jython.tar.gz>`_ 📥
   * - :ref:`tradebeans`
     - 439693
     - 466969
     - 34370090
     - `tradebeans.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/tradebeans.tar.gz>`_ 📥
   * - :ref:`tradesoap`
     - 440680
     - 468263
     - 34451130
     - `tradesoap.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/tradesoap.tar.gz>`_ 📥
.. _graphs_field_sensitive_alias:

Field-Sensitive Alias
^^^^^^^^^^^^^^^^^^^^^

Field-sensitive alias graphs for C programs: memory locations are
distinguished by the struct field they occupy, so aliasing is tracked per
field (the ``f_i`` family), as in `"Taming Transitive Redundancy for Context-Free Language Reachability" <https://dl.acm.org/doi/10.1145/3563343>`_.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - aa
     - Download
   * - :ref:`xz_field_sensitive_alias`
     - 2808
     - 6604
     - 205164
     - `xz_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/xz_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`nab_field_sensitive_alias`
     - 3444
     - 7982
     - 262566
     - `nab_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/nab_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`leela_field_sensitive_alias`
     - 8090
     - 19888
     - 3968276
     - `leela_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/leela_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`povray_field_sensitive_alias`
     - 15137
     - 38886
     - 27219043
     - `povray_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/povray_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`x264_field_sensitive_alias`
     - 18051
     - 44780
     - 5246565
     - `x264_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/x264_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`cactus_field_sensitive_alias`
     - 22350
     - 56636
     - 37625324
     - `cactus_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/cactus_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`parest_field_sensitive_alias`
     - 29788
     - 64528
     - 49415038
     - `parest_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/parest_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`perlbench_field_sensitive_alias`
     - 38091
     - 110874
     - 851737865
     - `perlbench_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/perlbench_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`imagick_field_sensitive_alias`
     - 41652
     - 111550
     - 369956094
     - `imagick_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/imagick_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`omnetpp_field_sensitive_alias`
     - 49962
     - 119064
     - 158255766
     - `omnetpp_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/omnetpp_field_sensitive_alias.tar.gz>`_ 📥
.. _graphs_context_sensitive_data_flow:

Context-Sensitive Data-Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Context-sensitive data-flow graphs for C programs, tracking how values flow
through the program under a calling context (the ``call_i`` / ``ret_i``
families), as in `"Taming Transitive Redundancy for Context-Free Language Reachability" <https://dl.acm.org/doi/10.1145/3563343>`_.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - vf
     - Download
   * - :ref:`xz`
     - 30492
     - 37173
     - 358834
     - `xz.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/xz.tar.gz>`_ 📥
   * - :ref:`nab`
     - 31215
     - 37484
     - 739646
     - `nab.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/nab.tar.gz>`_ 📥
   * - :ref:`leela`
     - 47665
     - 63996
     - 662466
     - `leela.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/leela.tar.gz>`_ 📥
   * - :ref:`x264`
     - 138702
     - 201034
     - 20259480
     - `x264.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/x264.tar.gz>`_ 📥
   * - :ref:`parest`
     - 233900
     - 307850
     - 1342540
     - `parest.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/parest.tar.gz>`_ 📥
   * - :ref:`imagick`
     - 331177
     - 445544
     - 12687034
     - `imagick.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/imagick.tar.gz>`_ 📥
   * - :ref:`povray`
     - 346034
     - 581210
     - 34599413
     - `povray.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/povray.tar.gz>`_ 📥
   * - :ref:`cactus`
     - 359200
     - 580297
     - 47806209
     - `cactus.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/cactus.tar.gz>`_ 📥
   * - :ref:`omnetpp`
     - 463454
     - 958487
     - 8424500
     - `omnetpp.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/omnetpp.tar.gz>`_ 📥
   * - :ref:`perlbench`
     - 605864
     - 1114892
     - 297504186
     - `perlbench.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/perlbench.tar.gz>`_ 📥
.. _graphs_data_provenance:

Data Provenance
^^^^^^^^^^^^^^^

Data-provenance graphs recording the lineage of data artifacts in a set of
Python projects, following the W3C PROV model (``Entity``, ``Activity``,
``wasDerivedFrom``) as studied in `"Understanding Data Science Lifecycle Provenance via Graph Segmentation and Summarization" <https://ieeexplore.ieee.org/document/8731467>`_.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - prov_derivation
     - Download
   * - :ref:`provenance_sampleproject`
     - 148
     - 763
     - 342
     - `sampleproject.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/sampleproject.tar.gz>`_ 📥
   * - :ref:`provenance_wikipedia_provenance`
     - 316
     - 1284
     - 1732
     - `wikipedia-provenance.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/wikipedia-provenance.tar.gz>`_ 📥
   * - :ref:`provenance_pluggy`
     - 353
     - 1818
     - 880
     - `pluggy.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/pluggy.tar.gz>`_ 📥
   * - :ref:`provenance_itsdangerous`
     - 425
     - 2210
     - 2912
     - `itsdangerous.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/itsdangerous.tar.gz>`_ 📥
   * - :ref:`provenance_requests`
     - 682
     - 3369
     - 2524
     - `requests.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/requests.tar.gz>`_ 📥
   * - :ref:`provenance_httpx`
     - 826
     - 4247
     - 4408
     - `httpx.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/httpx.tar.gz>`_ 📥
   * - :ref:`provenance_click`
     - 944
     - 4654
     - 2710
     - `click.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/click.tar.gz>`_ 📥
   * - :ref:`provenance_jinja`
     - 1202
     - 6277
     - 7436
     - `jinja.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jinja.tar.gz>`_ 📥
   * - :ref:`provenance_flask`
     - 1517
     - 7728
     - 8062
     - `flask.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/flask.tar.gz>`_ 📥
   * - :ref:`provenance_fastapi`
     - 6455
     - 26528
     - 8814
     - `fastapi.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/fastapi.tar.gz>`_ 📥
   * - :ref:`provenance_celery`
     - 6880
     - 35874
     - 25306
     - `celery.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/celery.tar.gz>`_ 📥
   * - :ref:`provenance_scikit_learn`
     - 11706
     - 60181
     - 217728
     - `scikit-learn.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/scikit-learn.tar.gz>`_ 📥
   * - :ref:`provenance_sphinx`
     - 13431
     - 72692
     - 304084
     - `sphinx.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/sphinx.tar.gz>`_ 📥
   * - :ref:`provenance_pandas`
     - 13696
     - 70959
     - 154646
     - `pandas.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/pandas.tar.gz>`_ 📥
   * - :ref:`provenance_django`
     - 23749
     - 113137
     - 615946
     - `django.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/django.tar.gz>`_ 📥
   * - :ref:`provenance_zulip`
     - 59854
     - 310032
     - 209908
     - `zulip.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/zulip.tar.gz>`_ 📥
   * - :ref:`provenance_superset`
     - 76348
     - 394708
     - 97460
     - `superset.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/superset.tar.gz>`_ 📥
   * - :ref:`provenance_airflow`
     - 90673
     - 454738
     - 91350
     - `airflow.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/airflow.tar.gz>`_ 📥

.. _graphs_name_resolution:

Name Resolution
^^^^^^^^^^^^^^^

Stack graphs capturing the scoping structure of source code for name
resolution, as in `"Stack Graphs: Name Resolution at Scale" <https://drops.dagstuhl.de/entities/document/10.4230/OASIcs.EVCS.2023.8>`_. Edges are the
stack-graph transitions (push, pop, branch, epsilon) that carry names through
scopes.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - name_resolution
     - Download
   * - :ref:`name_resolution_jiaozi`
     - 54952
     - 46322
     - 14435
     - `jiaozi.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jiaozi.tar.gz>`_ 📥
   * - :ref:`name_resolution_jsonpath`
     - 185421
     - 161488
     - 59764
     - `jsonpath.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jsonpath.tar.gz>`_ 📥
   * - :ref:`name_resolution_shattered_pixel_dungeon`
     - 1179205
     - 1017798
     - 971998
     - `shattered_pixel_dungeon.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/shattered_pixel_dungeon.tar.gz>`_ 📥
   * - :ref:`name_resolution_libgdx`
     - 2571363
     - 2321366
     - not available
     - `libgdx.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/libgdx.tar.gz>`_ 📥

.. _graphs_biological_uniprot:

Biological graphs from UniProt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Biological interaction graphs derived from the UniProt knowledgebase, where
nodes are biological entities and edges are the relations between them (e.g.
``belongs_to``, ``is_homologous_to``); they support subgraph and path queries
as in `"Subgraph queries by context-free grammars" <https://researchportal.helsinki.fi/en/publications/subgraph-queries-by-context-free-grammars/>`_.

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - grammar
     - Download
   * - :ref:`unigraph_1`
     - 3081
     - 11966
     - 376578
     - `unigraph_1.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_1.tar.gz>`_ 📥
   * - :ref:`unigraph_2`
     - 36467
     - 168344
     - 39888347
     - `unigraph_2.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_2.tar.gz>`_ 📥
   * - :ref:`unigraph_3`
     - 41332
     - 193866
     - 52471840
     - `unigraph_3.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_3.tar.gz>`_ 📥
   * - :ref:`unigraph_4`
     - 215480
     - 1346130
     - 808091802
     - `unigraph_4.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_4.tar.gz>`_ 📥
   * - :ref:`unigraph_5`
     - 243838
     - 1818404
     - 2303590109
     - `unigraph_5.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_5.tar.gz>`_ 📥
   * - :ref:`unigraph_6`
     - 286644
     - 1708910
     - 1722963921
     - `unigraph_6.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_6.tar.gz>`_ 📥
   * - :ref:`unigraph_7`
     - 285576
     - 2073268
     - 2320964134
     - `unigraph_7.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_7.tar.gz>`_ 📥
   * - :ref:`unigraph_8`
     - 449236
     - 3385168
     - not available
     - `unigraph_8.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_8.tar.gz>`_ 📥
   * - :ref:`unigraph_9`
     - 475478
     - 3579034
     - not available
     - `unigraph_9.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_9.tar.gz>`_ 📥
   * - :ref:`unigraph_10`
     - 2055881
     - 17223588
     - not available
     - `unigraph_10.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/unigraph_10.tar.gz>`_ 📥
