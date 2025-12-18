.. _unigraph_2:

unigraph_2
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_2
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1dli_1CfeVMZ81ZVUzX51RrkIu7vg58JO>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 36468
     - 168344


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 3925
   * - Is_homologous_to_r
     - 3925
   * - belongs_to
     - 4116
   * - belongs_to_r
     - 4116
   * - codes_for
     - 4394
   * - codes_for_r
     - 4394
   * - has
     - 17827
   * - has_r
     - 17827
   * - interacts_with
     - 8362
   * - participate_in
     - 35824
   * - participate_in_r
     - 35824
   * - refers_to
     - 13875
   * - refers_to_r
     - 13875

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
