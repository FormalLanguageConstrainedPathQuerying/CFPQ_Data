.. _travel:

travel
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - travel
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1oJXPK2AEFS3twkpxQ1rqRxnJVxYzmRsh>`_
   * - Origin
     - `.owl <https://protege.stanford.edu/ontologies/travel.owl>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 131
     - 554


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 90
   * - type_r
     - 90
   * - subClassOf
     - 30
   * - subClassOf_r
     - 30
   * - first
     - 24
   * - first_r
     - 24
   * - rest
     - 24
   * - rest_r
     - 24
   * - disjointWith
     - 20
   * - disjointWith_r
     - 20
   * - onProperty
     - 15
   * - onProperty_r
     - 15
   * - domain
     - 10
   * - domain_r
     - 10
   * - range
     - 10
   * - range_r
     - 10
   * - someValuesFrom
     - 10
   * - someValuesFrom_r
     - 10
   * - comment
     - 9
   * - comment_r
     - 9
   * - equivalentClass
     - 7
   * - equivalentClass_r
     - 7
   * - intersectionOf
     - 7
   * - intersectionOf_r
     - 7
   * - differentFrom
     - 6
   * - differentFrom_r
     - 6
   * - hasValue
     - 3
   * - hasValue_r
     - 3
   * - hasPart
     - 2
   * - hasPart_r
     - 2
   * - inverseOf
     - 2
   * - inverseOf_r
     - 2
   * - minCardinality
     - 2
   * - minCardinality_r
     - 2
   * - oneOf
     - 2
   * - oneOf_r
     - 2
   * - complementOf
     - 1
   * - complementOf_r
     - 1
   * - hasAccommodation
     - 1
   * - hasAccommodation_r
     - 1
   * - unionOf
     - 1
   * - unionOf_r
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
