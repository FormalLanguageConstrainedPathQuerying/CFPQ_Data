.. _generations:

generations
===========

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - generations
   * - Version
     - 2.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.s3.us-east-2.amazonaws.com/2.0.0/generations.tar.gz>`_
   * - Origin
     - `link <http://www.owl-ontologies.com/generations.owl>`_


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
   * - 129
     - 273


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 78
   * - rest
     - 45
   * - first
     - 45
   * - onProperty
     - 27
   * - intersectionOf
     - 18
   * - equivalentClass
     - 17
   * - someValuesFrom
     - 15
   * - hasValue
     - 12
   * - hasSex
     - 4
   * - inverseOf
     - 2
   * - sameAs
     - 2
   * - hasParent
     - 2
   * - hasChild
     - 2
   * - range
     - 1
   * - hasSibling
     - 1
   * - versionInfo
     - 1
   * - oneOf
     - 1

Canonical grammars
------------------

Introduced in `"Context-Free Path Queries on RDF Graphs" <https://arxiv.org/abs/1506.00743>`_

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
