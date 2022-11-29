.. _wine:

wine
====

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - wine
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/wine.tar.gz>`_
   * - Origin
     - `.rdf <https://www.w3.org/TR/owl-guide/wine.rdf>`_


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
   * - 733
     - 1839


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 485
   * - rest
     - 252
   * - first
     - 252
   * - onProperty
     - 174
   * - subClassOf
     - 126
   * - hasValue
     - 115
   * - locatedIn
     - 65
   * - intersectionOf
     - 56
   * - hasMaker
     - 52
   * - hasFlavor
     - 43
   * - hasBody
     - 41
   * - hasSugar
     - 40
   * - oneOf
     - 31
   * - allValuesFrom
     - 28
   * - maxCardinality
     - 22
   * - range
     - 10
   * - domain
     - 7
   * - cardinality
     - 6
   * - subPropertyOf
     - 5
   * - distinctMembers
     - 5
   * - label
     - 3
   * - differentFrom
     - 3
   * - comment
     - 3
   * - minCardinality
     - 2
   * - madeFromGrape
     - 2
   * - inverseOf
     - 2
   * - someValuesFrom
     - 1
   * - disjointWith
     - 1
   * - imports
     - 1
   * - priorVersion
     - 1
   * - hasColor
     - 1
   * - yearValue
     - 1
   * - adjacentRegion
     - 1
   * - unionOf
     - 1
   * - hasVintageYear
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
