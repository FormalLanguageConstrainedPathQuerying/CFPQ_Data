.. _unigraph_5:

unigraph_5
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_5
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1h4Vv2SHogbeqwIGFfMfjE48zG7kT04sQ>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 243839
     - 1818404


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 25983
   * - Is_homologous_to_r
     - 25983
   * - belongs_to
     - 31908
   * - belongs_to_r
     - 31908
   * - codes_for
     - 32606
   * - codes_for_r
     - 32606
   * - has
     - 155449
   * - has_r
     - 155449
   * - interacts_with
     - 66122
   * - participate_in
     - 472609
   * - participate_in_r
     - 472609
   * - refers_to
     - 157586
   * - refers_to_r
     - 157586

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
