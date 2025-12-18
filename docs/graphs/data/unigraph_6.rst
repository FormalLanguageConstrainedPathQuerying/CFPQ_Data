.. _unigraph_6:

unigraph_6
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_6
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1KJ0F5Qmou6gT3k1HunIRhF3xLFjrbqYS>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 286645
     - 1708910


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 24920
   * - Is_homologous_to_r
     - 24920
   * - belongs_to
     - 36214
   * - belongs_to_r
     - 36214
   * - codes_for
     - 29538
   * - codes_for_r
     - 29538
   * - has
     - 125074
   * - has_r
     - 125074
   * - interacts_with
     - 54220
   * - participate_in
     - 340295
   * - participate_in_r
     - 340295
   * - refers_to
     - 271304
   * - refers_to_r
     - 271304

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
