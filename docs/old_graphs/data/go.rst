.. _go:

go
==

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - go
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/go.tar.gz>`_
   * - Origin
     - `.owl <http://purl.obolibrary.org/obo/go.owl>`_


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
   * - 582929
     - 1437437


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 226481
   * - hasDbXref
     - 199191
   * - annotatedTarget
     - 132678
   * - annotatedSource
     - 132678
   * - annotatedProperty
     - 132678
   * - subClassOf
     - 94514
   * - hasExactSynonym
     - 90485
   * - label
     - 53100
   * - hasOBONamespace
     - 47427
   * - id
     - 47427
   * - IAO_0000115
     - 47417
   * - someValuesFrom
     - 31568
   * - onProperty
     - 31568
   * - rest
     - 24186
   * - first
     - 24186
   * - hasNarrowSynonym
     - 18849
   * - creation_date
     - 17873
   * - created_by
     - 17834
   * - hasRelatedSynonym
     - 14912
   * - equivalentClass
     - 12051
   * - intersectionOf
     - 12051
   * - comment
     - 5874
   * - deprecated
     - 5419
   * - hasBroadSynonym
     - 3865
   * - IAO_0100001
     - 3220
   * - hasAlternativeId
     - 2702
   * - IAO_0000231
     - 2702
   * - inSubset
     - 2452
   * - consider
     - 1862
   * - hasSynonymType
     - 111
   * - disjointWith
     - 30
   * - subPropertyOf
     - 21
   * - shorthand
     - 10
   * - propertyChainAxiom
     - 2
   * - inverseOf
     - 1
   * - hasScope
     - 1
   * - SynonymTypeProperty
     - 1
   * - IAO_0000589
     - 1
   * - hasOBOFormatVersion
     - 1
   * - default-namespace
     - 1
   * - license
     - 1
   * - versionIRI
     - 1
   * - creator
     - 1
   * - date
     - 1
   * - IAO_0000425
     - 1
   * - is_metadata_tag
     - 1
   * - is_class_level
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
