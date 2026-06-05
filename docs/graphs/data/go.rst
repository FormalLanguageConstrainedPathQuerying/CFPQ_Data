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
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1PmYTOqwLVHxduUmaq7VpWKtn0S6KeSBH>`_
   * - Origin
     - `.owl <http://purl.obolibrary.org/obo/go.owl>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 582929
     - 2874874


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 226481
   * - type_r
     - 226481
   * - hasDbXref
     - 199191
   * - hasDbXref_r
     - 199191
   * - annotatedProperty
     - 132678
   * - annotatedProperty_r
     - 132678
   * - annotatedSource
     - 132678
   * - annotatedSource_r
     - 132678
   * - annotatedTarget
     - 132678
   * - annotatedTarget_r
     - 132678
   * - subClassOf
     - 94514
   * - subClassOf_r
     - 94514
   * - hasExactSynonym
     - 90485
   * - hasExactSynonym_r
     - 90485
   * - label
     - 53100
   * - label_r
     - 53100
   * - hasOBONamespace
     - 47427
   * - hasOBONamespace_r
     - 47427
   * - id
     - 47427
   * - id_r
     - 47427
   * - IAO_i_0000115
     - 47417
   * - IAO_r_i_0000115
     - 47417
   * - onProperty
     - 31568
   * - onProperty_r
     - 31568
   * - someValuesFrom
     - 31568
   * - someValuesFrom_r
     - 31568
   * - first
     - 24186
   * - first_r
     - 24186
   * - rest
     - 24186
   * - rest_r
     - 24186
   * - hasNarrowSynonym
     - 18849
   * - hasNarrowSynonym_r
     - 18849
   * - creation_date
     - 17873
   * - creation_date_r
     - 17873
   * - created_by
     - 17834
   * - created_by_r
     - 17834
   * - hasRelatedSynonym
     - 14912
   * - hasRelatedSynonym_r
     - 14912
   * - equivalentClass
     - 12051
   * - equivalentClass_r
     - 12051
   * - intersectionOf
     - 12051
   * - intersectionOf_r
     - 12051
   * - comment
     - 5874
   * - comment_r
     - 5874
   * - deprecated
     - 5419
   * - deprecated_r
     - 5419
   * - hasBroadSynonym
     - 3865
   * - hasBroadSynonym_r
     - 3865
   * - IAO_i_0100001
     - 3220
   * - IAO_r_i_0100001
     - 3220
   * - IAO_i_0000231
     - 2702
   * - IAO_r_i_0000231
     - 2702
   * - hasAlternativeId
     - 2702
   * - hasAlternativeId_r
     - 2702
   * - inSubset
     - 2452
   * - inSubset_r
     - 2452
   * - consider
     - 1862
   * - consider_r
     - 1862
   * - hasSynonymType
     - 111
   * - hasSynonymType_r
     - 111
   * - disjointWith
     - 30
   * - disjointWith_r
     - 30
   * - subPropertyOf
     - 21
   * - subPropertyOf_r
     - 21
   * - shorthand
     - 10
   * - shorthand_r
     - 10
   * - propertyChainAxiom
     - 2
   * - propertyChainAxiom_r
     - 2
   * - IAO_i_0000425
     - 1
   * - IAO_i_0000589
     - 1
   * - IAO_r_i_0000425
     - 1
   * - IAO_r_i_0000589
     - 1
   * - SynonymTypeProperty
     - 1
   * - SynonymTypeProperty_r
     - 1
   * - creator
     - 1
   * - creator_r
     - 1
   * - date
     - 1
   * - date_r
     - 1
   * - default-namespace
     - 1
   * - default-namespace_r
     - 1
   * - hasOBOFormatVersion
     - 1
   * - hasOBOFormatVersion_r
     - 1
   * - hasScope
     - 1
   * - hasScope_r
     - 1
   * - inverseOf
     - 1
   * - inverseOf_r
     - 1
   * - is_class_level
     - 1
   * - is_class_level_r
     - 1
   * - is_metadata_tag
     - 1
   * - is_metadata_tag_r
     - 1
   * - license
     - 1
   * - license_r
     - 1
   * - versionIRI
     - 1
   * - versionIRI_r
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
