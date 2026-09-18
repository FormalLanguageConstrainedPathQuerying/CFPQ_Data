.. _graphs_context_sensitive_data_flow:

Context-Sensitive Data-Flow
***************************

.. only:: html

   :Release: |release|
   :Date: |today|

Context-sensitive data-flow graphs for C programs, tracking how values flow
through the program under a calling context (the ``call_i`` / ``ret_i``
families), as in `"Taming Transitive Redundancy for Context-Free Language Reachability" <https://dl.acm.org/doi/10.1145/3563343>`_.

.. toctree::
   :hidden:

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

.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - vf
     - Size (MB)
     - Download
   * - :ref:`xz`
     - 30492
     - 37173
     - 358834
     - 0.144
     - `xz.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/xz.tar.gz>`_ 📥
   * - :ref:`nab`
     - 31215
     - 37484
     - 739646
     - 0.126
     - `nab.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/nab.tar.gz>`_ 📥
   * - :ref:`leela`
     - 47665
     - 63996
     - 662466
     - 0.242
     - `leela.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/leela.tar.gz>`_ 📥
   * - :ref:`x264`
     - 138702
     - 201034
     - 20259480
     - 0.714
     - `x264.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/x264.tar.gz>`_ 📥
   * - :ref:`parest`
     - 233900
     - 307850
     - 1342540
     - 1.17
     - `parest.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/parest.tar.gz>`_ 📥
   * - :ref:`imagick`
     - 331177
     - 445544
     - 12687034
     - 1.93
     - `imagick.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/imagick.tar.gz>`_ 📥
   * - :ref:`povray`
     - 346034
     - 581210
     - 34599413
     - 2.34
     - `povray.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/povray.tar.gz>`_ 📥
   * - :ref:`cactus`
     - 359200
     - 580297
     - 47806209
     - 2.55
     - `cactus.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/cactus.tar.gz>`_ 📥
   * - :ref:`omnetpp`
     - 463454
     - 958487
     - 8424500
     - 6.06
     - `omnetpp.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/omnetpp.tar.gz>`_ 📥
   * - :ref:`perlbench`
     - 605864
     - 1114892
     - 297504186
     - 4.41
     - `perlbench.tar.gz <https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/perlbench.tar.gz>`_ 📥

Canonical grammars
------------------

Productions with index :math:`i` are duplicated for each call site in the analyzed program.
The start nonterminal is :math:`A`.

.. math::

   A \, \rightarrow \, A \, A \mid a \mid \varepsilon \, \\
   A \, \rightarrow \, call_i \, A \, ret_i \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   A -> A A | a | epsilon
   A -> call_i A ret_i
