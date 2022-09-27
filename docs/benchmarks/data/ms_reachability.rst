.. _msreachability:

MS_Reachability
===============

.. contents:: Table of Contents

Info
----
.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - Multiple-Source_Reachability_Benchmark
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://cfpq-data.s3.us-east-2.amazonaws.com/4.0.0/benchmark/MS_Reachability.tar.gz>`_

Description
-----------
This benchmark contains graphs, queries, sets of source vertices, and results for the multiple-source
formal-language-constrained reachability problem.
For each graph we provide the following benchmark information:

- **graph** -- contains a graph and its statistics (.csv + .md)
- **queries** -- contains different regular queries in the form of regular expressions
- **results** -- contains files with pairs of vertices <src, dest>  where 'src' is a source vertex and 'dest' is a vertex reachable from the 'src' vertex with respect to a particular query and a set of source vertices
- **src_vertices** -- contains different sets of source vertices

More information about multiple-source formal-language-constrained reachability problem can be found in
`"Multiple-Source Context-Free Path Querying in Terms of Linear Algebra" <https://openproceedings.org/2021/conf/edbt/p48.pdf>`_

Graphs Used
-----------
.. list-table::
   :header-rows: 1

   * - Graph
     - Num Nodes
     - Num Edges
     - Download
   * - :ref:`core`
     - 1323
     - 2752
     - `.tar.gz <https://cfpq-data.s3.us-east-2.amazonaws.com/2.0.0/core.tar.gz>`_ 📥
   * - :ref:`enzyme`
     - 48815
     - 86543
     - `.tar.gz <https://cfpq-data.s3.us-east-2.amazonaws.com/2.0.0/enzyme.tar.gz>`_ 📥
   * - :ref:`eclass`
     - 239111
     - 360248
     - `.tar.gz <https://cfpq-data.s3.us-east-2.amazonaws.com/2.0.0/eclass.tar.gz>`_ 📥
   * - :ref:`go`
     - 582929
     - 1437437
     - `.tar.gz <https://cfpq-data.s3.us-east-2.amazonaws.com/2.0.0/go.tar.gz>`_ 📥

Query Examples
--------------

.. math::

   \textit{type} \, \textit{isDefinedBy}^{*} \, \textit{type}\\

`Pyformlang Regex <https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html#pyformlang.regular_expression.Regex>`_:

.. code-block:: python

   type isDefinedBy* type

----

.. math::

   (\textit{rest} \, | \, \textit{label} \, | \, \textit{range} \, | \, \textit{type} \, | \, \textit{comment}) \, \textit{seeAlso}^{*}\\

`Pyformlang Regex <https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html#pyformlang.regular_expression.Regex>`_:

.. code-block:: python

   (rest | label | range | type | comment) seeAlso*

Useful utilities
----------------
For this benchmark we provide some useful functions from
:ref:`multiple_source_utils <cfpq_data.graphs.utils.multiple_source_utils>`.
