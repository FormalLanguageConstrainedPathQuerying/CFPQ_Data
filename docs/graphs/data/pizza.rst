.. _pizza:

pizza
=====

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - pizza
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/pizza.tar.gz>`_
   * - Origin
     - `.owl <https://protege.stanford.edu/ontologies/pizza/pizza.owl>`_


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
   * - 671
     - 3960


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - disjointWith
     - 398
   * - disjointWith_r
     - 398
   * - type
     - 365
   * - type_r
     - 365
   * - subClassOf
     - 259
   * - subClassOf_r
     - 259
   * - onProperty
     - 188
   * - onProperty_r
     - 188
   * - first
     - 187
   * - first_r
     - 187
   * - rest
     - 187
   * - rest_r
     - 187
   * - someValuesFrom
     - 155
   * - someValuesFrom_r
     - 155
   * - label
     - 96
   * - label_r
     - 96
   * - allValuesFrom
     - 26
   * - allValuesFrom_r
     - 26
   * - comment
     - 25
   * - comment_r
     - 25
   * - unionOf
     - 25
   * - unionOf_r
     - 25
   * - equivalentClass
     - 15
   * - equivalentClass_r
     - 15
   * - intersectionOf
     - 15
   * - intersectionOf_r
     - 15
   * - range
     - 7
   * - range_r
     - 7
   * - domain
     - 6
   * - domain_r
     - 6
   * - hasValue
     - 6
   * - hasValue_r
     - 6
   * - distinctMembers
     - 5
   * - distinctMembers_r
     - 5
   * - subPropertyOf
     - 4
   * - subPropertyOf_r
     - 4
   * - complementOf
     - 3
   * - complementOf_r
     - 3
   * - inverseOf
     - 3
   * - inverseOf_r
     - 3
   * - versionInfo
     - 3
   * - versionInfo_r
     - 3
   * - minCardinality
     - 1
   * - minCardinality_r
     - 1
   * - oneOf
     - 1
   * - oneOf_r
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
