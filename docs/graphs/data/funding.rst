.. _funding:

funding
=======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - funding
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/funding.tar.gz>`_
   * - Origin
     - `link <http://purl.org/cerif/frapo/Funding>`_


CSV File Structure
------------------

.. list-table::
   :header-rows: 1

   * - Column Number
     - Column Type
     - Column Description
   * - 1
     - int
     - The tail of the edge
   * - 2
     - int
     - The head of the edge
   * - 3
     - str
     - The label of the edge


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 778
     - 1086


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 304
   * - label
     - 231
   * - comment
     - 229
   * - subClassOf
     - 90
   * - subPropertyOf
     - 76
   * - range
     - 40
   * - description
     - 39
   * - domain
     - 37
   * - inverseOf
     - 17
   * - rest
     - 6
   * - first
     - 6
   * - unionOf
     - 3
   * - rights
     - 1
   * - date
     - 1
   * - imports
     - 1
   * - title
     - 1
   * - creator
     - 1
   * - contributor
     - 1
   * - versionInfo
     - 1
   * - seeAlso
     - 1

Canonical grammars
------------------

Nested parentheses grammars introduced in `"Context-Free Path Queries on RDF Graphs" <https://arxiv.org/abs/1506.00743>`_.
Template for these grammars is described on the :ref:`nested_parentheses` page.

.. math::

   S \, \rightarrow \, \overline{subClassOf} \, S \, subClassOf \, \mid \, \overline{subClassOf} \, subClassOf \, \\
   S \, \rightarrow \, \overline{type} \, S \, type \, \mid \, \overline{type} \, type \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> subClassOf_r S subClassOf | subClassOf_r subClassOf
   S -> type_r S type | type_r type

----

.. math::

   S \, \rightarrow \, \overline{subClassOf} \, S \, subClassOf \, \mid \, \overline{subClassOf} \, subClassOf \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> subClassOf_r S subClassOf | subClassOf_r subClassOf

----

.. math::

   S \, \rightarrow \, \overline{type} \, S \, type \, \mid \, \overline{type} \, type \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> type_r S type | type_r type
