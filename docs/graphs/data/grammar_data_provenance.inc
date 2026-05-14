Canonical Grammar
-----------------

This grammar describes derivation chains in provenance graphs.
The start nonterminal is :math:`S`.

.. math::

   S \, \rightarrow \, Step \mid S \, Step \, \\
   Step \, \rightarrow \, used_r \, Generated \mid wasDerivedFrom_r \, \\
   Generated \, \rightarrow \, wasGeneratedBy_r \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> Step
   S -> S Step
   Step -> used_r Generated
   Step -> wasDerivedFrom_r
   Generated -> wasGeneratedBy_r
