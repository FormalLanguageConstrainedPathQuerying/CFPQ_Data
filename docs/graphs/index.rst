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

----

Graphs
------

Contents
^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Source area
     - Number of graphs
   * - :ref:`graphs_cfpq_old_collection`
     - 36
   * - :ref:`graphs_rdf`
     - 18
   * - :ref:`graphs_java_points_to`
     - 7
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

.. _graphs_cfpq_old_collection:

CFPQ old collection
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`wc`
     - 332
     - 538
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/wc.tar.gz>`_ 📥
   * - :ref:`bzip`
     - 632
     - 1112
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/bzip.tar.gz>`_ 📥
   * - :ref:`pr`
     - 815
     - 1384
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/pr.tar.gz>`_ 📥
   * - :ref:`core`
     - 1323
     - 5504
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/core.tar.gz>`_ 📥
   * - :ref:`ls`
     - 1687
     - 2906
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/ls.tar.gz>`_ 📥
   * - :ref:`gzip`
     - 2687
     - 4586
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/gzip.tar.gz>`_ 📥
   * - :ref:`sunflow`
     - 15464
     - 31914
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/sunflow.tar.gz>`_ 📥
   * - :ref:`lusearch`
     - 15774
     - 29988
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/lusearch.tar.gz>`_ 📥
   * - :ref:`luindex`
     - 18532
     - 34750
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/luindex.tar.gz>`_ 📥
   * - :ref:`avrora`
     - 24690
     - 50392
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/avrora.tar.gz>`_ 📥
   * - :ref:`eclipse`
     - 41383
     - 80400
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/eclipse.tar.gz>`_ 📥
   * - :ref:`h2`
     - 44717
     - 113366
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/h2.tar.gz>`_ 📥
   * - :ref:`pmd`
     - 54444
     - 118658
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/pmd.tar.gz>`_ 📥
   * - :ref:`xalan`
     - 58476
     - 125516
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/xalan.tar.gz>`_ 📥
   * - :ref:`batik`
     - 60175
     - 126178
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/batik.tar.gz>`_ 📥
   * - :ref:`fop`
     - 86183
     - 166032
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/fop.tar.gz>`_ 📥
   * - :ref:`tomcat`
     - 111327
     - 221768
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/tomcat.tar.gz>`_ 📥
   * - :ref:`jython`
     - 191895
     - 520068
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/jython.tar.gz>`_ 📥
   * - :ref:`eclass`
     - 239111
     - 720496
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/eclass.tar.gz>`_ 📥
   * - :ref:`tradebeans`
     - 439693
     - 933938
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/tradebeans.tar.gz>`_ 📥
   * - :ref:`tradesoap`
     - 440680
     - 936526
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/tradesoap.tar.gz>`_ 📥
   * - :ref:`apache`
     - 1721418
     - 3020822
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/apache.tar.gz>`_ 📥
   * - :ref:`init`
     - 2446224
     - 4225618
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/init.tar.gz>`_ 📥
   * - :ref:`mm`
     - 2538243
     - 4382158
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/mm.tar.gz>`_ 📥
   * - :ref:`ipc`
     - 3401022
     - 5862996
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/ipc.tar.gz>`_ 📥
   * - :ref:`lib`
     - 3401355
     - 5863760
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/lib.tar.gz>`_ 📥
   * - :ref:`block`
     - 3423234
     - 5902786
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/block.tar.gz>`_ 📥
   * - :ref:`arch`
     - 3448422
     - 5940484
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/arch.tar.gz>`_ 📥
   * - :ref:`crypto`
     - 3464970
     - 5976774
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/crypto.tar.gz>`_ 📥
   * - :ref:`security`
     - 3479982
     - 6006652
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/security.tar.gz>`_ 📥
   * - :ref:`sound`
     - 3528861
     - 6099464
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/sound.tar.gz>`_ 📥
   * - :ref:`net`
     - 4039470
     - 7000282
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/net.tar.gz>`_ 📥
   * - :ref:`fs`
     - 4177416
     - 7218746
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/fs.tar.gz>`_ 📥
   * - :ref:`drivers`
     - 4273803
     - 7415538
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/drivers.tar.gz>`_ 📥
   * - :ref:`postgre`
     - 5203419
     - 9357086
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/postgre.tar.gz>`_ 📥
   * - :ref:`kernel`
     - 11254434
     - 18968426
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/kernel.tar.gz>`_ 📥

.. _graphs_rdf:

RDF
^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`generations`
     - 129
     - 546
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/generations.tar.gz>`_ 📥
   * - :ref:`travel`
     - 131
     - 554
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/travel.tar.gz>`_ 📥
   * - :ref:`skos`
     - 144
     - 504
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/skos.tar.gz>`_ 📥
   * - :ref:`univ`
     - 179
     - 586
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/univ.tar.gz>`_ 📥
   * - :ref:`foaf`
     - 256
     - 1262
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/foaf.tar.gz>`_ 📥
   * - :ref:`atom`
     - 291
     - 850
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/atom.tar.gz>`_ 📥
   * - :ref:`people`
     - 337
     - 1280
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/people.tar.gz>`_ 📥
   * - :ref:`biomedical`
     - 341
     - 918
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/biomedical.tar.gz>`_ 📥
   * - :ref:`pizza`
     - 671
     - 3960
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/pizza.tar.gz>`_ 📥
   * - :ref:`wine`
     - 733
     - 3678
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/wine.tar.gz>`_ 📥
   * - :ref:`funding`
     - 778
     - 2172
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/funding.tar.gz>`_ 📥
   * - :ref:`pathways`
     - 6238
     - 24726
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/pathways.tar.gz>`_ 📥
   * - :ref:`go_hierarchy`
     - 45007
     - 980218
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/go_hierarchy.tar.gz>`_ 📥
   * - :ref:`enzyme`
     - 48815
     - 173086
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/enzyme.tar.gz>`_ 📥
   * - :ref:`geospecies`
     - 450609
     - 4384690
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/geospecies.tar.gz>`_ 📥
   * - :ref:`go`
     - 582929
     - 2874874
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/go.tar.gz>`_ 📥
   * - :ref:`taxonomy_hierarchy`
     - 2112625
     - 65752578
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/taxonomy_hierarchy.tar.gz>`_ 📥
   * - :ref:`taxonomy`
     - 5728398
     - 29844250
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/taxonomy.tar.gz>`_ 📥

.. _graphs_java_points_to:

Java points-to graphs
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`gson`
     - 14114
     - 34934
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/gson.tar.gz>`_ 📥
   * - :ref:`mockito`
     - 25436
     - 62388
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/mockito.tar.gz>`_ 📥
   * - :ref:`commons_io`
     - 26188
     - 62428
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/commons_io.tar.gz>`_ 📥
   * - :ref:`commons_lang3`
     - 40970
     - 96854
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/commons_lang3.tar.gz>`_ 📥
   * - :ref:`junit5`
     - 59818
     - 149370
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/junit5.tar.gz>`_ 📥
   * - :ref:`guava`
     - 129562
     - 336232
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/guava.tar.gz>`_ 📥
   * - :ref:`jackson`
     - 149404
     - 395356
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/jackson.tar.gz>`_ 📥

.. _graphs_field_sensitive_alias:

Field-Sensitive Alias
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`xz_field_sensitive_alias`
     - 2808
     - 6604
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/xz_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`nab_field_sensitive_alias`
     - 3444
     - 7982
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/nab_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`leela_field_sensitive_alias`
     - 8090
     - 19888
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/leela_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`povray_field_sensitive_alias`
     - 15137
     - 38886
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/povray_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`x264_field_sensitive_alias`
     - 18051
     - 44780
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/x264_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`cactus_field_sensitive_alias`
     - 22350
     - 56636
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/cactus_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`parest_field_sensitive_alias`
     - 29788
     - 64528
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/parest_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`perlbench_field_sensitive_alias`
     - 38091
     - 110874
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/perlbench_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`imagick_field_sensitive_alias`
     - 41652
     - 111550
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/imagick_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`omnetpp_field_sensitive_alias`
     - 49962
     - 119064
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/omnetpp_field_sensitive_alias.tar.gz>`_ 📥

.. _graphs_context_sensitive_data_flow:

Context-Sensitive Data-Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`xz`
     - 30492
     - 37173
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/xz.tar.gz>`_ 📥
   * - :ref:`nab`
     - 31215
     - 37484
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/nab.tar.gz>`_ 📥
   * - :ref:`leela`
     - 47665
     - 63996
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/leela.tar.gz>`_ 📥
   * - :ref:`x264`
     - 138702
     - 201034
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/x264.tar.gz>`_ 📥
   * - :ref:`parest`
     - 233900
     - 307850
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/parest.tar.gz>`_ 📥
   * - :ref:`imagick`
     - 331177
     - 445544
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/imagick.tar.gz>`_ 📥
   * - :ref:`povray`
     - 346034
     - 581210
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/povray.tar.gz>`_ 📥
   * - :ref:`cactus`
     - 359200
     - 580297
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/cactus.tar.gz>`_ 📥
   * - :ref:`omnetpp`
     - 463454
     - 958487
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/omnetpp.tar.gz>`_ 📥
   * - :ref:`perlbench`
     - 605864
     - 1114892
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/perlbench.tar.gz>`_ 📥

.. _graphs_data_provenance:

Data Provenance
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`provenance_sampleproject`
     - 148
     - 763
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/sampleproject.tar.gz>`_ 📥
   * - :ref:`provenance_wikipedia_provenance`
     - 316
     - 1284
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/wikipedia-provenance.tar.gz>`_ 📥
   * - :ref:`provenance_pluggy`
     - 353
     - 1818
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/pluggy.tar.gz>`_ 📥
   * - :ref:`provenance_itsdangerous`
     - 425
     - 2210
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/itsdangerous.tar.gz>`_ 📥
   * - :ref:`provenance_requests`
     - 682
     - 3369
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/requests.tar.gz>`_ 📥
   * - :ref:`provenance_httpx`
     - 826
     - 4247
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/httpx.tar.gz>`_ 📥
   * - :ref:`provenance_click`
     - 944
     - 4654
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/click.tar.gz>`_ 📥
   * - :ref:`provenance_jinja`
     - 1202
     - 6277
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/jinja.tar.gz>`_ 📥
   * - :ref:`provenance_flask`
     - 1517
     - 7728
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/flask.tar.gz>`_ 📥
   * - :ref:`provenance_fastapi`
     - 6455
     - 26528
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/fastapi.tar.gz>`_ 📥
   * - :ref:`provenance_celery`
     - 6880
     - 35874
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/celery.tar.gz>`_ 📥
   * - :ref:`provenance_scikit_learn`
     - 11706
     - 60181
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/scikit-learn.tar.gz>`_ 📥
   * - :ref:`provenance_sphinx`
     - 13431
     - 72692
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/sphinx.tar.gz>`_ 📥
   * - :ref:`provenance_pandas`
     - 13696
     - 70959
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/pandas.tar.gz>`_ 📥
   * - :ref:`provenance_django`
     - 23749
     - 113137
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/django.tar.gz>`_ 📥
   * - :ref:`provenance_zulip`
     - 59854
     - 310032
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/zulip.tar.gz>`_ 📥
   * - :ref:`provenance_superset`
     - 76348
     - 394708
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/superset.tar.gz>`_ 📥
   * - :ref:`provenance_airflow`
     - 90673
     - 454738
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/airflow.tar.gz>`_ 📥

.. _graphs_name_resolution:

Name Resolution
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`name_resolution_jiaozi`
     - 54952
     - 46322
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/jiaozi.tar.gz>`_ 📥
   * - :ref:`name_resolution_jsonpath`
     - 185421
     - 161488
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/jsonpath.tar.gz>`_ 📥
   * - :ref:`name_resolution_shattered_pixel_dungeon`
     - 1179205
     - 1017798
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/shattered_pixel_dungeon.tar.gz>`_ 📥
   * - :ref:`name_resolution_libgdx`
     - 2571363
     - 2321366
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/libgdx.tar.gz>`_ 📥

.. _graphs_biological_uniprot:

Biological graphs from UniProt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`unigraph_1`
     - 3081
     - 11966
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_1.tar.gz>`_ 📥
   * - :ref:`unigraph_2`
     - 36467
     - 168344
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_2.tar.gz>`_ 📥
   * - :ref:`unigraph_3`
     - 41332
     - 193866
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_3.tar.gz>`_ 📥
   * - :ref:`unigraph_4`
     - 215480
     - 1346130
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_4.tar.gz>`_ 📥
   * - :ref:`unigraph_5`
     - 243838
     - 1818404
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_5.tar.gz>`_ 📥
   * - :ref:`unigraph_6`
     - 286644
     - 1708910
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_6.tar.gz>`_ 📥
   * - :ref:`unigraph_7`
     - 285576
     - 2073268
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_7.tar.gz>`_ 📥
   * - :ref:`unigraph_8`
     - 449236
     - 3385168
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_8.tar.gz>`_ 📥
   * - :ref:`unigraph_9`
     - 475478
     - 3579034
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_9.tar.gz>`_ 📥
   * - :ref:`unigraph_10`
     - 2055881
     - 17223588
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/unigraph_10.tar.gz>`_ 📥
