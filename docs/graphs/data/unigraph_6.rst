.. _unigraph_6:

unigraph_6
==========

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
   * - 286644
     - 1708910


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - is_homologous_to
     - 24920
   * - is_homologous_to_r
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

   S &\to Seq \quad IsAssociated \quad IsSimilar \\
   Seq &\to IsSimilar \quad (codes\_for \quad IsSimilar)? \\
   IsSimilar &\to \varepsilon \\
             &\mid has \quad IsSimilar \quad has_{r} \\
             &\mid is\_homologous\_to \quad IsSimilar \quad is\_homologous\_to_{r} \quad IsSimilar \\
             &\mid belongs\_to \quad IsSimilar \quad belongs\_to_{r} \\
             &\mid participate\_in \quad IsSimilar \quad participate\_in_{r} \\
   IsAssociated &\to refers\_to \quad refers\_to_{r}
