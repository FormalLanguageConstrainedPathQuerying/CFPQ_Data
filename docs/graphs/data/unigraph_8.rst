.. _unigraph_8:

unigraph_8
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_8
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1AAbvfMmjGkialHkukg9dAZbcIMwFX0Sf>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 449237
     - 3385168


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 46962
   * - Is_homologous_to_r
     - 46962
   * - belongs_to
     - 65054
   * - belongs_to_r
     - 65054
   * - codes_for
     - 58471
   * - codes_for_r
     - 58471
   * - has
     - 266994
   * - has_r
     - 266994
   * - interacts_with
     - 114040
   * - participate_in
     - 791262
   * - participate_in_r
     - 791262
   * - refers_to
     - 406821
   * - refers_to_r
     - 406821

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
