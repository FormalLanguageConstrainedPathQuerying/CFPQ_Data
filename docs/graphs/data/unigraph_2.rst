.. _unigraph_2:

unigraph_2
==========

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
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1-H-4ZBZ5JjD4YegYx241iltyWqPon6Fz>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 36467
     - 168344


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - is_homologous_to
     - 3925
   * - is_homologous_to_r
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
     - 35854
   * - participate_in_r
     - 35854
   * - refers_to
     - 13875
   * - refers_to_r
     - 13875

Grammar
------------------

The grammar file is attached to the archive.

.. math::

   S &\to Seq \quad IsAssociated \quad IsSimilar \\
   Seq &\to IsSimilar \quad (codes\_for \quad IsSimilar)? \\
   IsSimilar &\to \varepsilon \\
             &\mid has \quad IsSimilar \quad has_{r} \\
             &\mid is\_homologous\_to \quad IsSimilar \quad is\_homologous\_to_{r} \quad IsSimilar \\
             &\mid belongs\_to \quad IsSimilar \quad belongs\_to_{r} \\
             &\mid participate\_in \quad IsSimilar \quad participate\_in_{r} \\
   IsAssociated &\to refers\_to \quad refers\_to_{r}
