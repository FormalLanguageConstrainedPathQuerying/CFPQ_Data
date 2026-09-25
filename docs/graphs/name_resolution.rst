.. _graphs_name_resolution:

Name Resolution
***************

.. only:: html

   :Release: |release|
   :Date: |today|

Stack graphs capturing the scoping structure of source code for name
resolution, as in `"Stack Graphs: Name Resolution at Scale" <https://drops.dagstuhl.de/entities/document/10.4230/OASIcs.EVCS.2023.8>`_. Edges are the
stack-graph transitions (push, pop, branch, epsilon) that carry names through
scopes.

.. toctree::
   :hidden:

   data/name_resolution_jiaozi
   data/name_resolution_jsonpath
   data/name_resolution_shattered_pixel_dungeon
   data/name_resolution_libgdx

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - name_resolution
     - Size (MB)
     - Download
   * - :ref:`name_resolution_jiaozi`
     - 54952
     - 46322
     - not available
     - 0.240
     - `jiaozi.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jiaozi.tar.gz>`_ 📥
   * - :ref:`name_resolution_jsonpath`
     - 185421
     - 161488
     - 59764
     - 0.810
     - `jsonpath.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/jsonpath.tar.gz>`_ 📥
   * - :ref:`name_resolution_shattered_pixel_dungeon`
     - 1179205
     - 1017798
     - not available
     - 4.99
     - `shattered_pixel_dungeon.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/shattered_pixel_dungeon.tar.gz>`_ 📥
   * - :ref:`name_resolution_libgdx`
     - 2571363
     - 2321366
     - not available
     - 11.27
     - `libgdx.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/libgdx.tar.gz>`_ 📥

Canonical grammars
------------------

The grammar file is attached to the archive.

.. math::

   S &\to \varepsilon \\
     &\mid eps \quad S \\
     &\mid Q \quad S \\
     &\mid V \quad S \\
   S\#psh_{i} &\to psh_{i} \quad S \\
   S\#vpsh_{i} &\to vpsh_{i} \quad S \\
   V &\to S\#vpsh_{i} \quad vpp_{i} \\
   Q &\to S\#psh_{i} \quad pp_{i}
