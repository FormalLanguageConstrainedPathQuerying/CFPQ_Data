.. _unigraph_1:

unigraph_1
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_1
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1iNDQ04N1A9D94whhfWaDEdjioPUQLXR8>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 3082
     - 11966


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 1
   * - Is_homologous_to_r
     - 1
   * - belongs_to
     - 69
   * - belongs_to_r
     - 69
   * - codes_for
     - 33
   * - codes_for_r
     - 33
   * - has
     - 2201
   * - has_r
     - 2201
   * - interacts_with
     - 100
   * - participate_in
     - 2008
   * - participate_in_r
     - 2008
   * - refers_to
     - 1621
   * - refers_to_r
     - 1621

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
