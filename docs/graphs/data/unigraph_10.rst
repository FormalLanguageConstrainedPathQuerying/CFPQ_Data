.. _unigraph_10:

unigraph_10
===========

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
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1SWTFV2olNB9zlmEJ9PjD-0UYo6XF2fxo>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 2055881
     - 17223588


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - is_homologous_to
     - 428075
   * - is_homologous_to_r
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

   S &\to Seq \quad IsAssociated \quad IsSimilar \\
   Seq &\to IsSimilar \quad (codes\_for \quad IsSimilar)? \\
   IsSimilar &\to \varepsilon \\
             &\mid has \quad IsSimilar \quad has_{r} \\
             &\mid is\_homologous\_to \quad IsSimilar \quad is\_homologous\_to_{r} \quad IsSimilar \\
             &\mid belongs\_to \quad IsSimilar \quad belongs\_to_{r} \\
             &\mid participate\_in \quad IsSimilar \quad participate\_in_{r} \\
   IsAssociated &\to refers\_to \quad refers\_to_{r}
