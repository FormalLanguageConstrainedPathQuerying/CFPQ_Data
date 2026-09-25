.. _graphs_field_sensitive_alias:

Field-Sensitive Alias
*********************

.. only:: html

   :Release: |release|
   :Date: |today|

Field-sensitive alias graphs for C programs: memory locations are
distinguished by the struct field they occupy, so aliasing is tracked per
field (the ``f_i`` family), as in `"Taming Transitive Redundancy for Context-Free Language Reachability" <https://dl.acm.org/doi/10.1145/3563343>`_.

.. toctree::
   :hidden:

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

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - vf
     - Size (MB)
     - Download
   * - :ref:`xz_field_sensitive_alias`
     - 2808
     - 6604
     - 205164
     - 0.028
     - `xz_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/xz_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`nab_field_sensitive_alias`
     - 3444
     - 7982
     - 262566
     - 0.035
     - `nab_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/nab_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`leela_field_sensitive_alias`
     - 8090
     - 19888
     - 3968276
     - 0.086
     - `leela_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/leela_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`povray_field_sensitive_alias`
     - 15137
     - 38886
     - not available
     - 0.161
     - `povray_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/povray_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`x264_field_sensitive_alias`
     - 18051
     - 44780
     - 5246565
     - 0.201
     - `x264_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/x264_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`cactus_field_sensitive_alias`
     - 22350
     - 56636
     - not available
     - 0.225
     - `cactus_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/cactus_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`parest_field_sensitive_alias`
     - 29788
     - 64528
     - not available
     - 0.290
     - `parest_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/parest_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`perlbench_field_sensitive_alias`
     - 38091
     - 110874
     - not available
     - 0.447
     - `perlbench_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/perlbench_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`imagick_field_sensitive_alias`
     - 41652
     - 111550
     - not available
     - 0.446
     - `imagick_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/imagick_field_sensitive_alias.tar.gz>`_ 📥
   * - :ref:`omnetpp_field_sensitive_alias`
     - 49962
     - 119064
     - not available
     - 0.524
     - `omnetpp_field_sensitive_alias.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/omnetpp_field_sensitive_alias.tar.gz>`_ 📥

Canonical grammars
------------------

Productions with index :math:`i` are duplicated for each field number from the analyzed program classes.
The start nonterminal is :math:`V`.
Reversed edges (``a_r``, ``d_r``, ``f_r_i``) are auto-generated from forward edges.

.. math::

   M \, \rightarrow \, d_r \, V \, d \, \\
   V \, \rightarrow \, A \, V \, A \mid f_r_i \, V \, f_i \mid M \mid a_r \, V \, a \mid \varepsilon \, \\
   A \, \rightarrow \, a \, M? \mid \varepsilon \, \\

RSM (stored as ``vf.rsm`` in each archive):

.. code-block:: text

   start: V
   [box M]
   start: 0
   final: 3
   0 --d_r--> 1
   1 --V--> 2
   2 --d--> 3
   [box V]
   start: 0
   final: 0, 1, 2, 3, 4
   0 --V--> 1
   0 --M--> 4
   0 --a_r--> 5
   4 --a_r--> 5
   5 --V--> 1
   1 --a--> 2
   2 --M--> 3
   0 --f_r_i--> p_i
   p_i --V--> q_i
   q_i --f_i--> 3
