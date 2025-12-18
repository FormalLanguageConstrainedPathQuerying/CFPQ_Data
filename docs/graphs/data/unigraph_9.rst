.. _unigraph_9:

unigraph_9
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_9
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1v27oSwzkS_Z35QkzIlO5KD6XqrHjL_vU>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 475479
     - 3579034


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 51193
   * - Is_homologous_to_r
     - 51193
   * - belongs_to
     - 69672
   * - belongs_to_r
     - 69672
   * - codes_for
     - 63434
   * - codes_for_r
     - 63434
   * - has
     - 287954
   * - has_r
     - 287954
   * - interacts_with
     - 123610
   * - participate_in
     - 834013
   * - participate_in_r
     - 834013
   * - refers_to
     - 421446
   * - refers_to_r
     - 421446

Grammar
------------------

The grammar file is attached to the archive.

.. math::

   S &\to Seq \quad IsAssociated \quad IsSimilar \\
   Seq &\to IsSimilar \quad (codes\_for \quad IsSimilar)? \\
   IsSimilar &\to \varepsilon \\
             &\mid has \quad IsSimilar \quad has\_r \\
             &\mid is\_homologous\_to \quad IsSimilar \quad is\_homologous\_to\_r \quad IsSimilar \\
             &\mid belongs\_to \quad IsSimilar \quad belongs\_to\_r \\
             &\mid participate\_in \quad IsSimilar \quad participate\_in\_r \\
   IsAssociated &\to refers\_to \quad refers\_to
