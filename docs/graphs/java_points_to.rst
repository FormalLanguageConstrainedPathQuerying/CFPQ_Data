.. _graphs_java_points_to:

Java points-to graphs
*********************

.. only:: html

   :Release: |release|
   :Date: |today|

Exhaustive, field-sensitive points-to graphs for Java programs, produced by
the analysis of `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Edges are the points-to relations (allocations, assignments, loads, stores,
calls, returns) together with their reverses.

.. toctree::
   :hidden:

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

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - java_points_to
     - Size (MB)
     - Download
   * - :ref:`gson`
     - 14114
     - 34934
     - 56325
     - 0.189
     - `gson.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/gson.tar.gz>`_ 📥
   * - :ref:`sunflow`
     - 15464
     - 15957
     - 35209
     - 0.076
     - `sunflow.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/sunflow.tar.gz>`_ 📥
   * - :ref:`lusearch`
     - 15774
     - 14994
     - 43719
     - 0.079
     - `lusearch.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/lusearch.tar.gz>`_ 📥
   * - :ref:`luindex`
     - 18532
     - 17375
     - 176051
     - 0.095
     - `luindex.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/luindex.tar.gz>`_ 📥
   * - :ref:`avrora`
     - 24690
     - 25196
     - 192790
     - 0.138
     - `avrora.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/avrora.tar.gz>`_ 📥
   * - :ref:`mockito`
     - 25436
     - 62388
     - 16169
     - 0.349
     - `mockito.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/mockito.tar.gz>`_ 📥
   * - :ref:`commons_io`
     - 26188
     - 62428
     - 24020
     - 0.342
     - `commons_io.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/commons_io.tar.gz>`_ 📥
   * - :ref:`commons_lang3`
     - 40970
     - 96854
     - 27553
     - 0.521
     - `commons_lang3.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/commons_lang3.tar.gz>`_ 📥
   * - :ref:`eclipse`
     - 41383
     - 40200
     - 378989
     - 0.201
     - `eclipse.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/eclipse.tar.gz>`_ 📥
   * - :ref:`h2`
     - 44717
     - 56683
     - 2611022
     - 0.256
     - `h2.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/h2.tar.gz>`_ 📥
   * - :ref:`pmd`
     - 54444
     - 59329
     - 137120
     - 0.280
     - `pmd.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/pmd.tar.gz>`_ 📥
   * - :ref:`xalan`
     - 58476
     - 62758
     - 1138776
     - 0.309
     - `xalan.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/xalan.tar.gz>`_ 📥
   * - :ref:`junit5`
     - 59818
     - 149370
     - 129598
     - 0.850
     - `junit5.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/junit5.tar.gz>`_ 📥
   * - :ref:`batik`
     - 60175
     - 63089
     - 868368
     - 0.301
     - `batik.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/batik.tar.gz>`_ 📥
   * - :ref:`fop`
     - 86183
     - 83016
     - 1984072
     - 0.404
     - `fop.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/fop.tar.gz>`_ 📥
   * - :ref:`tomcat`
     - 111327
     - 110884
     - 3792543
     - 0.544
     - `tomcat.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/tomcat.tar.gz>`_ 📥
   * - :ref:`guava`
     - 129562
     - 336232
     - 26384496
     - 2.00
     - `guava.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/guava.tar.gz>`_ 📥
   * - :ref:`jackson`
     - 149404
     - 395356
     - 3108775
     - 2.33
     - `jackson.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jackson.tar.gz>`_ 📥
   * - :ref:`jython`
     - 191895
     - 260034
     - 561720
     - 1.04
     - `jython.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jython.tar.gz>`_ 📥
   * - :ref:`tradebeans`
     - 439693
     - 466969
     - 34370090
     - 2.26
     - `tradebeans.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/tradebeans.tar.gz>`_ 📥
   * - :ref:`tradesoap`
     - 440680
     - 468263
     - 34451130
     - 2.26
     - `tradesoap.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/tradesoap.tar.gz>`_ 📥

Canonical grammars
------------------

Grammars for the field-sensitive analysis of Java programs introduced in `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Template for these grammars is described on the :ref:`java_points-to` page.

.. math::
   \textit{PointsTo} \, \rightarrow \, (\textit{assign} \mid \textit{load}_f \, \textit{Alias} \, \textit{store}_f)^{*} \, \textit{alloc} \, \\
   \textit{Alias} \, \rightarrow \, \textit{PointsTo} \, \textit{FlowsTo} \, \\
   \textit{FlowsTo} \, \rightarrow \, \overline{\textit{alloc}} \, (\overline{\textit{assign}} \mid \overline{\textit{store}_f} \, \textit{Alias} \, \overline{\textit{load}_f})^* \, \\
   \forall \, f \, \in \, Fields

Optimized variant
^^^^^^^^^^^^^^^^^

An equivalent WCNF grammar introduced as optimization (5) in `"Optimization of the Context-Free Language Reachability Matrix-Based Algorithm" <https://arxiv.org/abs/2401.11029>`_ (Fig. 1(b)) is stored in each archive as ``java_points_to_muravev2024.cnf``. It generates the same language and returns identical reachable-pair counts (verified with FastMatrixCFPQ on small graphs).

The archives of this category use two label conventions for the field-indexed
labels: the indexed template (``load_i``, ...) and the bare family form
(``load``, ...). The stored optimized variant follows the convention of its
archive — the indexed form below, or the same productions with every ``_i``
suffix dropped (``LPFS``, ``LP``, ``FS``, ``SPFL``, ``SP``, ``FL``) for the
bare-form archives.

.. code-block:: text

   PT	alloc
   PT	assign	PT
   PT	LPFS_i	PT
   FT	alloc_r
   FT	FT	assign_r
   FT	FT	SPFL_i
   LPFS_i	LP_i	FS_i
   LP_i	load_i	PT
   FS_i	FT	store_i
   SPFL_i	SP_i	FL_i
   SP_i	store_r_i	PT
   FL_i	FT	load_r_i

   Count:
   PT
