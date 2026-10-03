.. _label_star:

Label Star
==========

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - Per-Label Transitive Closure Regular Expression Template
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
   * - :math:`L`
     - A stored edge label of the graph; one query file per stored label


Grammar Template
----------------

.. math::

   L^*


Grammar Description
-------------------
The label star template generates the language of all strings consisting of repetitions of a single stored label: a pair :math:`(u, v)` is reachable if some path from :math:`u` to :math:`v` is labeled entirely by :math:`L` — the transitive closure of the edges labeled :math:`L`.

This is a designed stub: no real-world RPQ data exists yet. When the data is provided, the query file lives inside the self-contained graph archive under ``queries/rpq/`` (see the "File structure" section of the :ref:`graphs` page).

Example Grammars
----------------
The template instantiated for the stored label :math:`a`:

.. math::

   a^*

`Pyformlang Regex <https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html>`_:

.. code-block:: python

   a*
