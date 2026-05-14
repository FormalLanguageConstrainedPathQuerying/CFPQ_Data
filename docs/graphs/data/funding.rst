.. _funding:

funding
=======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - funding
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/funding.tar.gz>`_
   * - Origin
     - `link <http://purl.org/cerif/frapo/Funding>`_


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
   * - 778
     - 2172


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 304
   * - type_r
     - 304
   * - label
     - 231
   * - label_r
     - 231
   * - comment
     - 229
   * - comment_r
     - 229
   * - subClassOf
     - 90
   * - subClassOf_r
     - 90
   * - subPropertyOf
     - 76
   * - subPropertyOf_r
     - 76
   * - range
     - 40
   * - range_r
     - 40
   * - description
     - 39
   * - description_r
     - 39
   * - domain
     - 37
   * - domain_r
     - 37
   * - inverseOf
     - 17
   * - inverseOf_r
     - 17
   * - first
     - 6
   * - first_r
     - 6
   * - rest
     - 6
   * - rest_r
     - 6
   * - unionOf
     - 3
   * - unionOf_r
     - 3
   * - contributor
     - 1
   * - contributor_r
     - 1
   * - creator
     - 1
   * - creator_r
     - 1
   * - date
     - 1
   * - date_r
     - 1
   * - imports
     - 1
   * - imports_r
     - 1
   * - rights
     - 1
   * - rights_r
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
