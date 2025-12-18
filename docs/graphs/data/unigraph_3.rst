.. _unigraph_3:

unigraph_3
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_3
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1LYU-INIDw562laqO79pbXoKGRjEJQzbf>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 41333
     - 193866


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 4231
   * - Is_homologous_to_r
     - 4231
   * - belongs_to
     - 4618
   * - belongs_to_r
     - 4618
   * - codes_for
     - 4963
   * - codes_for_r
     - 4963
   * - has
     - 20960
   * - has_r
     - 20960
   * - interacts_with
     - 9570
   * - participate_in
     - 42751
   * - participate_in_r
     - 42751
   * - refers_to
     - 14625
   * - refers_to_r
     - 14625

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
