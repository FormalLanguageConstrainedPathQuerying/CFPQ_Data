.. _unigraph_4:

unigraph_4
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_4
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=11bLP_1eyPXGYs9brpGrsxJfw6psiWY7N>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 215481
     - 1346130


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 16848
   * - Is_homologous_to_r
     - 16848
   * - belongs_to
     - 19034
   * - belongs_to_r
     - 19034
   * - codes_for
     - 19390
   * - codes_for_r
     - 19390
   * - has
     - 89628
   * - has_r
     - 89628
   * - interacts_with
     - 37682
   * - participate_in
     - 281306
   * - participate_in_r
     - 281306
   * - refers_to
     - 228018
   * - refers_to_r
     - 228018

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
