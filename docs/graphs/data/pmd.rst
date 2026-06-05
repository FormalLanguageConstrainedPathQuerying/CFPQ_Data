.. _pmd:

pmd
=====

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - pmd
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1sgkRMV-PykU6pQ3sFxIuw4dVqNBhptg5>`_
   * - Origin
     - `link <https://dacapobench.sourceforge.net>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 54444
     - 118658


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - :math:`\textit{alloc}`
     - 7552
   * - :math:`\overline{\textit{alloc}}`
     - 7552
   * - :math:`\textit{assign}`
     - 38676
   * - :math:`\overline{\textit{assign}}`
     - 38676
   * - :math:`\textit{load}_i`
     - 11109
   * - :math:`\overline{\textit{load}_i}`
     - 11109
   * - :math:`\textit{store}_i`
     - 1992
   * - :math:`\overline{\textit{store}_i}`
     - 1992

Canonical grammars
------------------

Grammars for the field-sensitive analysis of Java programs introduced in `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Template for these grammars is described on the :ref:`java_points-to` page.

.. math::
   \textit{PointsTo} \, \rightarrow \, (\textit{assign} \mid \textit{load}_f \, \textit{Alias} \, \textit{store}_f)^{*} \, \textit{alloc} \, \\
   \textit{Alias} \, \rightarrow \, \textit{PointsTo} \, \textit{FlowsTo} \, \\
   \textit{FlowsTo} \, \rightarrow \, \overline{\textit{alloc}} \, (\overline{\textit{assign}} \mid \overline{\textit{store}_f} \, \textit{Alias} \, \overline{\textit{load}_f})^* \, \\
   \forall \, f \, \in \, Fields
