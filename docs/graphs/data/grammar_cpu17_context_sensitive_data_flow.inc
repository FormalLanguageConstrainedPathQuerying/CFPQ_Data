Canonical Grammar
-----------------

Productions with index :math:`i` are duplicated for each call site in the analyzed program.
The start nonterminal is :math:`A`.

.. math::

   A \, \rightarrow \, A \, A \mid a \mid \varepsilon \, \\
   A \, \rightarrow \, call_i \, A \, ret_i \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   A -> A A | a | epsilon
   A -> call_i A ret_i
