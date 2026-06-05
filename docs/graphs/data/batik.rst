.. _batik:

batik
=====

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - batik
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1-lu0T9T8mYa8Hnn8YNjW4NEIAZErUNsH>`_
   * - Origin
     - `link <https://dacapobench.sourceforge.net>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 60175
     - 126178


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - :math:`\textit{alloc}`
     - 10322
   * - :math:`\overline{\textit{alloc}}`
     - 10322
   * - :math:`\textit{assign}`
     - 43905
   * - :math:`\overline{\textit{assign}}`
     - 43905
   * - :math:`\textit{load}_i`
     - 7176
   * - :math:`\overline{\textit{load}_i}`
     - 7176
   * - :math:`\textit{store}_i`
     - 1686
   * - :math:`\overline{\textit{store}_i}`
     - 1686

Canonical grammars
------------------

Grammars for the field-sensitive analysis of Java programs introduced in `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Template for these grammars is described on the :ref:`java_points-to` page.

.. math::
   \textit{PointsTo} \, \rightarrow \, (\textit{assign} \mid \textit{load}_f \, \textit{Alias} \, \textit{store}_f)^{*} \, \textit{alloc} \, \\
   \textit{Alias} \, \rightarrow \, \textit{PointsTo} \, \textit{FlowsTo} \, \\
   \textit{FlowsTo} \, \rightarrow \, \overline{\textit{alloc}} \, (\overline{\textit{assign}} \mid \overline{\textit{store}_f} \, \textit{Alias} \, \overline{\textit{load}_f})^* \, \\
   \forall \, f \, \in \, Fields
