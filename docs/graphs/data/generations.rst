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
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1g1hRX2J3WdoWXJDfzt1MlPIPezLZDVze>`_
   * - Origin
     - `link <http://www.owl-ontologies.com/generations.owl>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 129
     - 546


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 78
   * - type_r
     - 78
   * - first
     - 45
   * - first_r
     - 45
   * - rest
     - 45
   * - rest_r
     - 45
   * - onProperty
     - 27
   * - onProperty_r
     - 27
   * - intersectionOf
     - 18
   * - intersectionOf_r
     - 18
   * - equivalentClass
     - 17
   * - equivalentClass_r
     - 17
   * - someValuesFrom
     - 15
   * - someValuesFrom_r
     - 15
   * - hasValue
     - 12
   * - hasValue_r
     - 12
   * - hasSex
     - 4
   * - hasSex_r
     - 4
   * - hasChild
     - 2
   * - hasChild_r
     - 2
   * - hasParent
     - 2
   * - hasParent_r
     - 2
   * - inverseOf
     - 2
   * - inverseOf_r
     - 2
   * - sameAs
     - 2
   * - sameAs_r
     - 2
   * - hasSibling
     - 1
   * - hasSibling_r
     - 1
   * - oneOf
     - 1
   * - oneOf_r
     - 1
   * - range
     - 1
   * - range_r
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
