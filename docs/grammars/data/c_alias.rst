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
   * - Kind
     - Static Analysis
   * - Version
     - 4.0.0
   * - Example download (.txt + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/grammar/example/c_alias.tar.gz>`_
   * - Origin
     - `link <https://dl.acm.org/doi/10.1145/1328897.1328464>`_


Grammar Parameters
------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - :math:`\textit{assigment_labels}`
     - Pair :math:`(a, \overline{a})` where label :math:`a` represents the assignment operation and :math:`a_r` is reverse to it
   * - :math:`\textit{dereference_labels}`
     - Pair :math:`(d, \overline{d})` where label :math:`d` represents pointer dereference relation and :math:`d_r` is reverse to it


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
C Alias grammar with :math:`\textit{assigment_labels} = \{(\textit{a}, \textit{a_r})\}` and :math:`\textit{dereference_labels} = \{(\textit{d}, \textit{d_r})\}`.

.. math::

   S \, \rightarrow \, \textit{d_r} \, V \, d \, \\
   V \, \rightarrow \, V_1 \, V_2 \, V_3 \, \\
   V_1 \, \rightarrow \, \varepsilon \, \\
   V_1 \, \rightarrow \, V_2 \, \textit{a_r} \, V_1 \, \\
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

   S \, \rightarrow \, \textit{d_r} \, V \, d \, \\
   V \, \rightarrow \, ((S \, \mid \, \varepsilon) \, \textit{a_r})^{*} \, (S \, \mid \, \varepsilon) \, (a \, (S \, \mid \, \varepsilon))^{*} \, \\

`Pyformlang RSA <https://github.com/Aunsiels/pyformlang/tree/master/pyformlang/rsa>`_:

.. code-block:: python

   S -> d_r V d
   V -> ((S | epsilon) a_r)* (S | epsilon) (a (S | epsilon))*
