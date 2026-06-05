.. _tradebeans:

tradebeans
==========

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - tradebeans
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1xdo7bCrbcLRGKdbDTlTAUwbdkq_Y2-js>`_
   * - Origin
     - `link <https://dacapobench.sourceforge.net>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 439693
     - 933938


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - :math:`\textit{alloc}`
     - 69597
   * - :math:`\overline{\textit{alloc}}`
     - 69597
   * - :math:`\textit{assign}`
     - 335195
   * - :math:`\overline{\textit{assign}}`
     - 335195
   * - :math:`\textit{load}_i`
     - 49794
   * - :math:`\overline{\textit{load}_i}`
     - 49794
   * - :math:`\textit{store}_i`
     - 12383
   * - :math:`\overline{\textit{store}_i}`
     - 12383

Canonical grammars
------------------

Grammars for the field-sensitive analysis of Java programs introduced in `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Template for these grammars is described on the :ref:`java_points-to` page.

.. math::
   \textit{PointsTo} \, \rightarrow \, (\textit{assign} \mid \textit{load}_f \, \textit{Alias} \, \textit{store}_f)^{*} \, \textit{alloc} \, \\
   \textit{Alias} \, \rightarrow \, \textit{PointsTo} \, \textit{FlowsTo} \, \\
   \textit{FlowsTo} \, \rightarrow \, \overline{\textit{alloc}} \, (\overline{\textit{assign}} \mid \overline{\textit{store}_f} \, \textit{Alias} \, \overline{\textit{load}_f})^* \, \\
   \forall \, f \, \in \, Fields
