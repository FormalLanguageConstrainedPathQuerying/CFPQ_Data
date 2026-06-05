.. _go_hierarchy:

go_hierarchy
============

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - go_hierarchy
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1jvbxsvnlnJT058BgQREVr6rEn9nhOcHs>`_
   * - Origin
     - `.owl.xz <https://ftp.uniprot.org/pub/databases/uniprot/current_release/rdf/go-hierarchy.owl.xz>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 45007
     - 980218


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - subClassOf
     - 490109
   * - subClassOf_r
     - 490109


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
