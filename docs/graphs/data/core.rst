.. _core:

core
====

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - core
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/core.tar.gz>`_
   * - Origin
     - `.owl <https://ftp.uniprot.org/pub/databases/uniprot/current_release/rdf/core.owl>`_


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
   * - 1323
     - 2752


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 706
   * - isDefinedBy
     - 387
   * - label
     - 269
   * - comment
     - 238
   * - first
     - 183
   * - rest
     - 183
   * - subClassOf
     - 178
   * - domain
     - 139
   * - range
     - 130
   * - seeAlso
     - 116
   * - onProperty
     - 49
   * - unionOf
     - 35
   * - subPropertyOf
     - 25
   * - distinctMembers
     - 14
   * - onClass
     - 13
   * - allValuesFrom
     - 12
   * - maxQualifiedCardinality
     - 10
   * - disjointWith
     - 8
   * - intersectionOf
     - 8
   * - equivalentClass
     - 8
   * - cardinality
     - 8
   * - qualifiedCardinality
     - 7
   * - someValuesFrom
     - 6
   * - onDataRange
     - 4
   * - inverseOf
     - 4
   * - oneOf
     - 3
   * - hasValue
     - 3
   * - maxCardinality
     - 2
   * - deprecated
     - 2
   * - versionInfo
     - 1
   * - minCardinality
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
