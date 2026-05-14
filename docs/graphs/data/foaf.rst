.. _foaf:

foaf
====

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - foaf
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/foaf.tar.gz>`_
   * - Origin
     - `link <http://xmlns.com/foaf/0.1>`_


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
   * - 256
     - 1262


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 174
   * - type_r
     - 174
   * - label
     - 78
   * - label_r
     - 78
   * - comment
     - 75
   * - comment_r
     - 75
   * - term_status
     - 75
   * - term_status_r
     - 75
   * - isDefinedBy
     - 72
   * - isDefinedBy_r
     - 72
   * - domain
     - 55
   * - domain_r
     - 55
   * - range
     - 55
   * - range_r
     - 55
   * - subPropertyOf
     - 13
   * - subPropertyOf_r
     - 13
   * - subClassOf
     - 10
   * - subClassOf_r
     - 10
   * - disjointWith
     - 8
   * - disjointWith_r
     - 8
   * - inverseOf
     - 8
   * - inverseOf_r
     - 8
   * - equivalentClass
     - 5
   * - equivalentClass_r
     - 5
   * - description
     - 1
   * - description_r
     - 1
   * - equivalentProperty
     - 1
   * - equivalentProperty_r
     - 1
   * - title
     - 1
   * - title_r
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
