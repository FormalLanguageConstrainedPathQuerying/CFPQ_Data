.. _java_points-to:

Java Points-to
==============

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - Java Points-to Analysis Grammar
   * - Class
     - Context-Free
   * - Kind
     - Static Analysis
   * - Version
     - 4.0.0
   * - Example download (.txt + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/grammar/example/java_points-to.tar.gz>`_
   * - Origin
     - `link <https://dl.acm.org/doi/10.1145/2858965.2814307>`_


Grammar Parameters
------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - :math:`\textit{fields}`
     - List of fields :math:`f` used in Java program for load/store operations


Grammar Template
----------------

.. math::
   \textit{PointsTo} \, &\rightarrow \, (\textit{assign} \, \mid  \, \textit{load}_f \, \textit{Alias} \, \textit{store}_f)^{*} \, \textit{alloc} \, \\
   \textit{Alias} \, &\rightarrow \, \textit{PointsTo} \, \textit{FlowsTo} \, \\
   \textit{FlowsTo} \, &\rightarrow \, \overline{\textit{alloc}} \, (\overline{\textit{assign}} \, \mid \, \overline{\textit{store}}_f \, \textit{Alias} \, \overline{\textit{load}}_f)^* \, \\
   &\forall \, f \, \in \, \textit{fields} \, \\


Description
-----------
Java points-to analysis grammar generates language for the field-sensitive analysis
of Java programs, which tracks the dataflow between heap objects that are stored in
and loaded from fields :math:`f \in \textit{fields}`. Introduced in
`"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
The dataflow of the program is constructed from object creations, variable assignments,
and load/store operations on fields.


Example Grammars
----------------

The Java points-to analysis grammar with :math:`\textit{fields} = [0, 1]`.

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> PTh alloc
   PTh -> epsilon
   PTh -> assign PTh
   PTh -> load_0 Al store_0 PTh
   PTh -> load_1 Al store_1 PTh
   FT -> alloc_r FTh
   FTh -> epsilon
   FTh -> assign_r FTh
   FTh -> store_0_r Al load_0_r FTh
   FTh -> store_1_r Al load_1_r FTh
   Al -> S FT
----
