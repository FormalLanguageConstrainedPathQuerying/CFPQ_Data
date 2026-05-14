.. _atom:

atom
====

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - atom_primitive
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/atom.tar.gz>`_
   * - Origin
     - `link <http://ontology.dumontierlab.com/atom-primitive>`_


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
   * - 291
     - 850


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 138
   * - type_r
     - 138
   * - label
     - 129
   * - label_r
     - 129
   * - subClassOf
     - 122
   * - subClassOf_r
     - 122
   * - comment
     - 11
   * - comment_r
     - 11
   * - domain
     - 5
   * - domain_r
     - 5
   * - range
     - 5
   * - range_r
     - 5
   * - subPropertyOf
     - 4
   * - subPropertyOf_r
     - 4
   * - creator
     - 2
   * - creator_r
     - 2
   * - date
     - 1
   * - date_r
     - 1
   * - description
     - 1
   * - description_r
     - 1
   * - format
     - 1
   * - format_r
     - 1
   * - imports
     - 1
   * - imports_r
     - 1
   * - language
     - 1
   * - language_r
     - 1
   * - publisher
     - 1
   * - publisher_r
     - 1
   * - seeAlso
     - 1
   * - seeAlso_r
     - 1
   * - title
     - 1
   * - title_r
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
