.. _tomcat:

tomcat
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - tomcat
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1bd6fjsLT4JAX5BFC4jryW7kOIx1OCs4I>`_
   * - Origin
     - `link <https://dacapobench.sourceforge.net>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 111327
     - 221768


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - :math:`\textit{alloc}`
     - 22962
   * - :math:`\overline{\textit{alloc}}`
     - 22962
   * - :math:`\textit{assign}`
     - 69473
   * - :math:`\overline{\textit{assign}}`
     - 69473
   * - :math:`\textit{load}_i`
     - 15198
   * - :math:`\overline{\textit{load}_i}`
     - 15198
   * - :math:`\textit{store}_i`
     - 3251
   * - :math:`\overline{\textit{store}_i}`
     - 3251

Canonical grammars
------------------

Grammars for the field-sensitive analysis of Java programs introduced in `"Giga-scale exhaustive points-to analysis for Java in under a minute" <https://dl.acm.org/doi/10.1145/2858965.2814307>`_.
Template for these grammars is described on the :ref:`java_points-to` page.

.. math::
   \textit{PointsTo} \, \rightarrow \, (\textit{assign} \mid \textit{load}_f \, \textit{Alias} \, \textit{store}_f)^{*} \, \textit{alloc} \, \\
   \textit{Alias} \, \rightarrow \, \textit{PointsTo} \, \textit{FlowsTo} \, \\
   \textit{FlowsTo} \, \rightarrow \, \overline{\textit{alloc}} \, (\overline{\textit{assign}} \mid \overline{\textit{store}_f} \, \textit{Alias} \, \overline{\textit{load}_f})^* \, \\
   \forall \, f \, \in \, Fields
