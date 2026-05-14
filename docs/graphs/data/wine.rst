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
     - 3678


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 485
   * - type_r
     - 485
   * - first
     - 252
   * - first_r
     - 252
   * - rest
     - 252
   * - rest_r
     - 252
   * - onProperty
     - 174
   * - onProperty_r
     - 174
   * - subClassOf
     - 126
   * - subClassOf_r
     - 126
   * - hasValue
     - 115
   * - hasValue_r
     - 115
   * - locatedIn
     - 65
   * - locatedIn_r
     - 65
   * - intersectionOf
     - 56
   * - intersectionOf_r
     - 56
   * - hasMaker
     - 52
   * - hasMaker_r
     - 52
   * - hasFlavor
     - 43
   * - hasFlavor_r
     - 43
   * - hasBody
     - 41
   * - hasBody_r
     - 41
   * - hasSugar
     - 40
   * - hasSugar_r
     - 40
   * - oneOf
     - 31
   * - oneOf_r
     - 31
   * - allValuesFrom
     - 28
   * - allValuesFrom_r
     - 28
   * - maxCardinality
     - 22
   * - maxCardinality_r
     - 22
   * - range
     - 10
   * - range_r
     - 10
   * - domain
     - 7
   * - domain_r
     - 7
   * - cardinality
     - 6
   * - cardinality_r
     - 6
   * - distinctMembers
     - 5
   * - distinctMembers_r
     - 5
   * - subPropertyOf
     - 5
   * - subPropertyOf_r
     - 5
   * - comment
     - 3
   * - comment_r
     - 3
   * - differentFrom
     - 3
   * - differentFrom_r
     - 3
   * - label
     - 3
   * - label_r
     - 3
   * - inverseOf
     - 2
   * - inverseOf_r
     - 2
   * - madeFromGrape
     - 2
   * - madeFromGrape_r
     - 2
   * - minCardinality
     - 2
   * - minCardinality_r
     - 2
   * - adjacentRegion
     - 1
   * - adjacentRegion_r
     - 1
   * - disjointWith
     - 1
   * - disjointWith_r
     - 1
   * - hasColor
     - 1
   * - hasColor_r
     - 1
   * - hasVintageYear
     - 1
   * - hasVintageYear_r
     - 1
   * - imports
     - 1
   * - imports_r
     - 1
   * - priorVersion
     - 1
   * - priorVersion_r
     - 1
   * - someValuesFrom
     - 1
   * - someValuesFrom_r
     - 1
   * - unionOf
     - 1
   * - unionOf_r
     - 1
   * - yearValue
     - 1
   * - yearValue_r
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
