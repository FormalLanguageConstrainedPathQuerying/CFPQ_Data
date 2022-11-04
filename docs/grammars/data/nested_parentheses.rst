.. _nested_parentheses:

Nested Parentheses
==================

.. contents:: Table of Contents

Info
----

.. list-table::
   :header-rows: 1

   * -
     -
   * - Full Name
     - Nested Parentheses Grammar
   * - Version
     - 4.0.0
   * - Class
     - Context-Free
   * - Example download (.txt)
     - `.tar.gz <https://cfpq-data.storage.yandexcloud.net/4.0.0/grammar/example/nested_parentheses.tar.gz>`_
   * - Origin
     - `link <https://en.wikipedia.org/wiki/Dyck_language>`_


Grammar Parameters
------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - :math:`\textit{types}`
     - List of pairs :math:`(\textit{op}_i, \textit{cp}_i)` with opening and closing parentheses for each type
   * - :math:`\textit{eps}`
     - :math:`\textit{True}` if empty string is in the language and :math:`\textit{False}` otherwise


Grammar Template
----------------

.. math::

   S \, &\rightarrow \, \varepsilon \, \qquad \qquad &\textit{if } \textit{eps} = \textit{True} \, \\
   S \, &\rightarrow \, \textit{op}_i \, \textit{cp}_i \qquad \qquad &\textit{if } \textit{eps} = \textit{False} \, \\
   S \, &\rightarrow \, \textit{op}_i \, S \, \textit{cp}_i \, &\\
   &\forall \, (\textit{op}_i, \textit{cp}_i) \, \in \, \textit{types} \, &\\


Grammar Description
-------------------
Nested parentheses grammars generate languages of the nested parentheses of :math:`|\textit{types}|` types.
For example, such a grammar with :math:`\textit{types} = \{(a, b)\}`
and :math:`\textit{eps} = \textit{True}` generates the language :math:`\{a^n b^n \ | \ n \geq 0\}`.


Example Grammars
----------------
The nested parentheses grammar with :math:`\textit{types} = \{(a, b)\}` and :math:`\textit{eps} = \textit{True}`.

.. math::

   S \, \rightarrow \, \varepsilon \, \mid \, a \, S \, b \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> epsilon | a S b

----

The nested parentheses grammar with :math:`\textit{types} = \{(a, b)\}` and :math:`\textit{eps} = \textit{False}`.

.. math::

   S \, \rightarrow \, a \, b \, \mid \, a \, S \, b \, \\

`Pyformlang CFG <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_:

.. code-block:: python

   S -> a b | a S b

----
