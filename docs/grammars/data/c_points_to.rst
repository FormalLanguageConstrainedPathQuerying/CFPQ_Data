.. _c_alias:

C Alias
=======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - C Alias Analysis Grammar
   * - Class
     - Context-Free
   * - Version
     - 4.0.0
   * - Example download (.txt)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/grammar/example/c_alias.tar.gz>`_
   * - Origin
     - `link <https://dl.acm.org/doi/10.1145/1328897.1328464>`_


Grammar Template
----------------

.. math::

   S \, &\rightarrow \, \overline{d} \, V \, d \, \\
   V \, &\rightarrow \, ((S \, \mid \, \varepsilon) \, \overline{a})^{*} \, (S \, \mid \, \varepsilon) \, (a \, (S \, \mid \, \varepsilon))^{*} \, \\


Description
-----------
C alias analysis grammar generates language for the flow-insensitive alias analysis of C programs.
Introduced in `"Demand-driven alias analysis for C" <https://dl.acm.org/doi/10.1145/1328897.1328464>`_.
The alias problem here is formulated as a context-free language (CFL) reachability problem over a graph representation
of the assignments :math:`a` and pointer dereference relations :math:`d` in a program.


Example Grammars
----------------

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
   V \, \rightarrow \, ((S \, \mid \, \varepsilon) \, \overline{a})^{*} \, (S \, \mid \, \varepsilon) \, (a \, (S \, \mid \, \varepsilon))^{*} \, \\

`Pyformlang RSA <https://github.com/Aunsiels/pyformlang/tree/master/pyformlang/rsa>`_:

.. code-block:: python

   S -> d_r V d
   V -> ((S | epsilon) a_r)* (S | epsilon) (a (S | epsilon))*
