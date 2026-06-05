.. _taxonomy:

taxonomy
========

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - taxonomy
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1spRUicn0pZ9MbyiidA5A9XEP_qfrbFet>`_
   * - Origin
     - `.rdf.xz <https://ftp.uniprot.org/pub/databases/uniprot/current_release/rdf/taxonomy.rdf.xz>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 5728398
     - 29844250


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 2508635
   * - type_r
     - 2508635
   * - partOfLineage
     - 2441076
   * - partOfLineage_r
     - 2441076
   * - scientificName
     - 2112637
   * - scientificName_r
     - 2112637
   * - subClassOf
     - 2112637
   * - subClassOf_r
     - 2112637
   * - narrowerTransitive
     - 2112633
   * - narrowerTransitive_r
     - 2112633
   * - rank
     - 1882006
   * - rank_r
     - 1882006
   * - otherName
     - 889344
   * - otherName_r
     - 889344
   * - obsolete
     - 328439
   * - obsolete_r
     - 328439
   * - seeAlso
     - 145407
   * - seeAlso_r
     - 145407
   * - depiction
     - 56228
   * - depiction_r
     - 56228
   * - height
     - 56169
   * - height_r
     - 56169
   * - width
     - 56169
   * - width_r
     - 56169
   * - replacedBy
     - 53962
   * - replacedBy_r
     - 53962
   * - replaces
     - 53962
   * - replaces_r
     - 53962
   * - commonName
     - 41607
   * - commonName_r
     - 41607
   * - mnemonic
     - 26101
   * - mnemonic_r
     - 26101
   * - name
     - 17833
   * - name_r
     - 17833
   * - strain
     - 11389
   * - strain_r
     - 11389
   * - synonym
     - 9457
   * - synonym_r
     - 9457
   * - host
     - 6433
   * - host_r
     - 6433
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
