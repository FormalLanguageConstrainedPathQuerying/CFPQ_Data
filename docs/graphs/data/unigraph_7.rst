.. _unigraph_7:

unigraph_7
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - unigraph_7
   * - Version
     - 4.0.3
   * - Direct download (.mtx files)
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1HHrkCyiCY84hjSa5W9mupfYd2619faqQ>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 285577
     - 2073268


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - Is_homologous_to
     - 26038
   * - Is_homologous_to_r
     - 26038
   * - belongs_to
     - 31775
   * - belongs_to_r
     - 31775
   * - codes_for
     - 32401
   * - codes_for_r
     - 32401
   * - has
     - 153793
   * - has_r
     - 153793
   * - interacts_with
     - 65078
   * - participate_in
     - 500983
   * - participate_in_r
     - 500983
   * - refers_to
     - 259105
   * - refers_to_r
     - 259105

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
