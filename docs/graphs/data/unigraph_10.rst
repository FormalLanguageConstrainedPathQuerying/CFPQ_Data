.. _unigraph_10:

unigraph_10
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_10
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1vdmXHv8se2PNRJ_Moxbgt3jBXfAy8gP9>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 2055882
     - 17223588


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 428075
   * - Is_homologous_to_r
     - 428075
   * - belongs_to
     - 516479
   * - belongs_to_r
     - 516479
   * - codes_for
     - 267020
   * - codes_for_r
     - 267020
   * - has
     - 2569647
   * - has_r
     - 2569647
   * - interacts_with
     - 673162
   * - participate_in
     - 3349393
   * - participate_in_r
     - 3349393
   * - refers_to
     - 1144599
   * - refers_to_r
     - 1144599

Grammar
------------------

The grammar file is attached to the archive.

.. math::

   S &\to Seq\,  IsAssociated\,  IsSimilar \\
   Seq &\to IsSimilar\, (codes\_for\,  IsSimilar)? \\
   & IsSimilar \to \varepsilon \\
   &\mid has\, IsSimilar\, has\_r \\
   &\mid is\_homologous\_to\, IsSimilar\, is\_homologous\_to\_r\, IsSimilar \\
   &\mid belongs\_to\, IsSimilar\, belongs\_to\_r \\
   &\mid participate\_in\, IsSimilar\, participate\_in\_r \\
   & IsAssociated \to refers\_to\, refers\_to
