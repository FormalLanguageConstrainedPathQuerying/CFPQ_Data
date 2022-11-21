.. _fs:

fs
==

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - fs_after_inline
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/fs.tar.gz>`_
   * - Origin
     - `.txt <https://drive.google.com/uc?export=download&id=0B8bQanV_QfNkcFQxSzg2VzdrdXc>`_


CSV File Structure
------------------

.. list-table::
   :header-rows: 1

   * - Column Number
     - Column Type
     - Column Description
   * - 1
     - int
     - The tail of the edge
   * - 2
     - int
     - The head of the edge
   * - 3
     - str
     - The label of the edge


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 4177416
     - 3609373


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - D
     - 2784943
   * - A
     - 824430

Canonical grammars
------------------

.. note::

   You must apply function `cfpq_data.change_edges` with `mapping={"A": "a", "D": "d"}` to the graph in order to use these grammars.

Grammars for the alias analysis of C programs introduced in `"Demand-driven alias analysis for C" <https://dl.acm.org/doi/10.1145/1328897.1328464>`_.
Template for these grammars is described on the :ref:`c_alias` page.

.. math::

   S \, \rightarrow \, \overline{d} \, V \, d \, \\
   V \, \rightarrow \, V_1 \, V_2 \, V_3 \, \\
   V_1 \, \rightarrow \, \varepsilon \, \\
   V_1 \, \rightarrow \, V_2 \, \overline{a} \, V_1 \, \\
   V_2 \, \rightarrow \, \varepsilon \, \\
   V_2 \, \rightarrow \, S \, \\
   V_3 \, \rightarrow \, \varepsilon \, \\
   V_3 \, \rightarrow \, a \, V_2 \, V_3 \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> d_r V d
   V -> V1 V2 V3
   V1 -> epsilon
   V1 -> V2 a_r V1
   V2 -> epsilon
   V2 -> S
   V3 -> epsilon
   V3 -> a V2 V3

----

.. math::

   S \, \rightarrow \, \overline{d} \, V \, d \, \\
   V \, \rightarrow \, ((S \mid \varepsilon) \, \overline{a})^{*} \, (S \mid \varepsilon) \, (a \, (S \mid \varepsilon))^{*} \, \\

`Pyformlang RSA <https://github.com/Aunsiels/pyformlang/tree/master/pyformlang/rsa>`_:

.. code-block:: python

   S -> d_r V d
   V -> ((S|epsilon) a_r)* (S|epsilon) (a (S|epsilon))*
