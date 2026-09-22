.. _reachability:

Reachability
============

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - Reachability Regular Expression Template
   * - Version
     - 5.0.0
   * - Class
     - Regular
   * - Kind
     - General
   * - Status
     - designed — no data yet (real-world RPQ data will be provided later)
   * - Origin
     - :ref:`FLPQ design <flpq>`


Grammar Parameters
------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - :math:`L_1, \dots, L_n`
     - The stored edge labels of the graph; there are no free parameters — the label set is derived from the graph


Grammar Template
----------------

.. math::

   (L_1 \,|\, \dots \,|\, L_n)^*


Grammar Description
-------------------
The reachability template generates the language of all strings over the stored labels of the graph: a pair :math:`(u, v)` is reachable if some path from :math:`u` to :math:`v` is labeled by an arbitrary string over the label set — unrestricted reachability.

This is a designed stub: no real-world RPQ data exists yet. When the data is provided, the query file lives inside the self-contained graph archive under ``queries/rpq/`` (see the "File structure" section of the :ref:`graphs` page).

Example Grammars
----------------
The template instantiated for a graph with stored labels :math:`\{a, b\}`:

.. math::

   (a \,|\, b)^*

`Pyformlang Regex <https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html>`_:

.. code-block:: python

   (a|b)*
