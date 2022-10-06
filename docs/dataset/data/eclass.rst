.. _eclass:

eclass
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - eclass_514en
   * - Version
     - 4.0.0
   * - Direct download (.csv + .md)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/eclass.tar.gz>`_
   * - Origin
     - `link <http://www.ebusiness-unibw.org/ontologies/eclass/5.1.4>`_


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
   * - 239111
     - 360248


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - subClassOf
     - 90962
   * - type
     - 72517
   * - label
     - 72515
   * - comment
     - 72515
   * - hierarchyCode
     - 30329
   * - range
     - 7136
   * - subPropertyOf
     - 7136
   * - domain
     - 7136
   * - creator
     - 1
   * - imports
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
