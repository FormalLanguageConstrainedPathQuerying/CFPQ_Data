.. _people:

people
======

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - people_pets
   * - Version
     - 4.0.0
   * - Direct download
     - `.tar.gz <https://drive.google.com/uc?export=download&id=1uIFg-JRXY6I6lvmRdXEXksdoYiVet4Pi>`_
   * - Origin
     - `.rdf <http://owl.man.ac.uk/tutorial/people+pets.rdf>`_


Graph Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Num Nodes
     - Num Edges
   * - 337
     - 1280


Edges Statistics
----------------

.. list-table::
   :header-rows: 1

   * - Edge Label
     - Num Edge Label
   * - type
     - 161
   * - type_r
     - 161
   * - comment
     - 95
   * - comment_r
     - 95
   * - label
     - 95
   * - label_r
     - 95
   * - first
     - 57
   * - first_r
     - 57
   * - rest
     - 57
   * - rest_r
     - 57
   * - onProperty
     - 33
   * - onProperty_r
     - 33
   * - subClassOf
     - 33
   * - subClassOf_r
     - 33
   * - someValuesFrom
     - 25
   * - someValuesFrom_r
     - 25
   * - intersectionOf
     - 22
   * - intersectionOf_r
     - 22
   * - equivalentClass
     - 21
   * - equivalentClass_r
     - 21
   * - allValuesFrom
     - 6
   * - allValuesFrom_r
     - 6
   * - has_pet
     - 6
   * - has_pet_r
     - 6
   * - range
     - 5
   * - range_r
     - 5
   * - disjointWith
     - 4
   * - disjointWith_r
     - 4
   * - unionOf
     - 4
   * - unionOf_r
     - 4
   * - inverseOf
     - 3
   * - inverseOf_r
     - 3
   * - subPropertyOf
     - 3
   * - subPropertyOf_r
     - 3
   * - complementOf
     - 2
   * - complementOf_r
     - 2
   * - domain
     - 2
   * - domain_r
     - 2
   * - drives
     - 1
   * - drives_r
     - 1
   * - is_pet_of
     - 1
   * - is_pet_of_r
     - 1
   * - maxCardinality
     - 1
   * - maxCardinality_r
     - 1
   * - minCardinality
     - 1
   * - minCardinality_r
     - 1
   * - reads
     - 1
   * - reads_r
     - 1
   * - service_number
     - 1
   * - service_number_r
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
