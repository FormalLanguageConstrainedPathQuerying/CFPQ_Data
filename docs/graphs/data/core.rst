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
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1iauv_uNwEqeZ0wLYt-q0DemaKlf0Eokl>`_
   * - Origin
     - `.owl <https://ftp.uniprot.org/pub/databases/uniprot/current_release/rdf/core.owl>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 1323
     - 5504


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 706
   * - type_r
     - 706
   * - isDefinedBy
     - 387
   * - isDefinedBy_r
     - 387
   * - label
     - 269
   * - label_r
     - 269
   * - comment
     - 238
   * - comment_r
     - 238
   * - first
     - 183
   * - first_r
     - 183
   * - rest
     - 183
   * - rest_r
     - 183
   * - subClassOf
     - 178
   * - subClassOf_r
     - 178
   * - domain
     - 139
   * - domain_r
     - 139
   * - range
     - 130
   * - range_r
     - 130
   * - seeAlso
     - 116
   * - seeAlso_r
     - 116
   * - onProperty
     - 49
   * - onProperty_r
     - 49
   * - unionOf
     - 35
   * - unionOf_r
     - 35
   * - subPropertyOf
     - 25
   * - subPropertyOf_r
     - 25
   * - distinctMembers
     - 14
   * - distinctMembers_r
     - 14
   * - onClass
     - 13
   * - onClass_r
     - 13
   * - allValuesFrom
     - 12
   * - allValuesFrom_r
     - 12
   * - maxQualifiedCardinality
     - 10
   * - maxQualifiedCardinality_r
     - 10
   * - cardinality
     - 8
   * - cardinality_r
     - 8
   * - disjointWith
     - 8
   * - disjointWith_r
     - 8
   * - equivalentClass
     - 8
   * - equivalentClass_r
     - 8
   * - intersectionOf
     - 8
   * - intersectionOf_r
     - 8
   * - qualifiedCardinality
     - 7
   * - qualifiedCardinality_r
     - 7
   * - someValuesFrom
     - 6
   * - someValuesFrom_r
     - 6
   * - inverseOf
     - 4
   * - inverseOf_r
     - 4
   * - onDataRange
     - 4
   * - onDataRange_r
     - 4
   * - hasValue
     - 3
   * - hasValue_r
     - 3
   * - oneOf
     - 3
   * - oneOf_r
     - 3
   * - deprecated
     - 2
   * - deprecated_r
     - 2
   * - maxCardinality
     - 2
   * - maxCardinality_r
     - 2
   * - minCardinality
     - 1
   * - minCardinality_r
     - 1
   * - versionInfo
     - 1
   * - versionInfo_r
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
