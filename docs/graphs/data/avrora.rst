.. _avrora:

avrora
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - avrora
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1Wrd7Cm34u4ybwoNiZ1WgRbLGMVvGPH-T>`_
   * - Origin
     - `link <https://dacapobench.sourceforge.net>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 24690
     - 50392


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - :math:`\textit{alloc}`
     - 4526
   * - :math:`\overline{\textit{alloc}}`
     - 4526
   * - :math:`\textit{assign}`
     - 16009
   * - :math:`\overline{\textit{assign}}`
     - 16009
   * - :math:`\textit{load}_i`
     - 3684
   * - :math:`\overline{\textit{load}_i}`
     - 3684
   * - :math:`\textit{store}_i`
     - 977
   * - :math:`\overline{\textit{store}_i}`
     - 977

Canonical grammars
------------------

Grammars for the field-sensitive analysis of Java programs introduced in `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Template for these grammars is described on the :ref:`java_points-to` page.

.. math::
   \textit{PointsTo} \, \rightarrow \, (\textit{assign} \mid \textit{load}_f \, \textit{Alias} \, \textit{store}_f)^{*} \, \textit{alloc} \, \\
   \textit{Alias} \, \rightarrow \, \textit{PointsTo} \, \textit{FlowsTo} \, \\
   \textit{FlowsTo} \, \rightarrow \, \overline{\textit{alloc}} \, (\overline{\textit{assign}} \mid \overline{\textit{store}_f} \, \textit{Alias} \, \overline{\textit{load}_f})^* \, \\
   \forall \, f \, \in \, Fields
