Canonical Grammar
-----------------

Productions with index :math:`i` are duplicated for each field number from the analyzed program classes.
The start nonterminal is :math:`V`.

.. math::

   M \, \rightarrow \, d \, V \, d \, \\
   V \, \rightarrow \, A \, V \, A \mid f_i \, V \, f_i \mid M \mid \varepsilon \, \\
   A \, \rightarrow \, a \, M? \mid \varepsilon \, \\
   A \, \rightarrow \, M? \, a \mid \varepsilon \, \\

`Pyformlang RSA <https://github.com/Aunsiels/pyformlang/tree/master/pyformlang/rsa>`_:

.. code-block:: text

   M -> d V d
   V -> A V A | f_i V f_i | M | epsilon
   A -> a M? | epsilon
   A -> M? a | epsilon
