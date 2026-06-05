.. _enzyme:

enzyme
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - enzyme
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1G4R2susqQeUsFbC8oUNXzmdMbHNI8sDE>`_
   * - Origin
     - `link <http://purl.uniprot.org/core/Enzyme>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 48815
     - 173086


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 14989
   * - type_r
     - 14989
   * - comment
     - 11954
   * - comment_r
     - 11954
   * - altLabel
     - 10088
   * - altLabel_r
     - 10088
   * - subClassOf
     - 8163
   * - subClassOf_r
     - 8163
   * - broaderTransitive
     - 8156
   * - broaderTransitive_r
     - 8156
   * - activity
     - 6825
   * - activity_r
     - 6825
   * - label
     - 6825
   * - label_r
     - 6825
   * - prefLabel
     - 6788
   * - prefLabel_r
     - 6788
   * - narrowerTransitive
     - 6781
   * - narrowerTransitive_r
     - 6781
   * - cofactorLabel
     - 1831
   * - cofactorLabel_r
     - 1831
   * - replacedBy
     - 1411
   * - replacedBy_r
     - 1411
   * - obsolete
     - 1375
   * - obsolete_r
     - 1375
   * - replaces
     - 1356
   * - replaces_r
     - 1356
   * - imports
     - 1
   * - imports_r
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
