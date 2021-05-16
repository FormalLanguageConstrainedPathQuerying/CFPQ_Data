.. _tutorial:

.. currentmodule:: cfpq_data

Tutorial
========

.. only:: html

   :Release: |release|
   :Date: |today|

.. currentmodule:: cfpq_data

This guide can help you start working with CFPQ_Data.

We use the NetworkX `MultiDiGraph
<https://networkx.org/documentation/latest/reference/classes/multidigraph.html>`_ to represent the labeled graph.
To familiarize yourself with this representation, see `NetworkX tutorial
<https://networkx.org/documentation/latest/tutorial.html>`_.

We use the Pyformlang `CFG
<https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_ to represent the
context-free grammar.
To familiarize yourself with this representation, see `Pyformlang usage
<https://pyformlang.readthedocs.io/en/latest/usage.html#context-free-grammar>`_.

All functions are documented on the :ref:`reference` page.

Graphs
------

You are able to get a synthetic or real-world graph with CFPQ_Data.

Create a synthetic graph
^^^^^^^^^^^^^^^^^^^^^^^^

You can create many different synthetic graphs by using functions from :ref:`graphs_generators`.

For example, let's create a one cycle graph, the edges of which are marked with the letter ``a``.

.. nbplot::

    import cfpq_data
    cycle = cfpq_data.labeled_cycle_graph(5, edge_label="a")

Get a real graph
^^^^^^^^^^^^^^^^

You can get many different real-world graphs from CFPQ_Data :ref:`dataset`.

And present these graphs in convenient formats by using functions from :ref:`graphs_readwrite`.

For example, let's get a ``generations`` ontology graph.

.. nbplot::

    generations = cfpq_data.graph_from_dataset("generations")

Change labels
^^^^^^^^^^^^^

You can change the specified graph labels by using function :func:`cfpq_data.graphs.utils.change_edges`
from :ref:`graphs_utils`.

.. nbplot::

    new_cycle = cfpq_data.change_edges(cycle, {"a": "b"})

Now the labels ``a`` have changed to ``b``.

Grammars
--------

You can create your own context-free grammar (CFG) or use a predefined one.
Now we have three representations of CFG documented on the :ref:`grammars` page:

1. `Classic <https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions>`_
2. `Chomsky Normal Form <https://en.wikipedia.org/wiki/Chomsky_normal_form>`_
3. `Recursive State Machine <https://link.springer.com/chapter/10.1007/978-3-030-54832-2_6#Sec2>`_

Create a context-free grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create context-free grammar by using function :func:`cfpq_data.grammars.readwrite.cfg.cfg_from_text`
from :ref:`grammars_readwrite`.

.. nbplot::

    cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

Use predefined context-free grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CFPQ_Data has many predefined grammars documented on the :ref:`grammars_samples` page.

.. nbplot::

    brackets = cfpq_data.brackets
    brackets.to_text()  # 'S -> a S b\nS -> a b\n'

Change terminals
^^^^^^^^^^^^^^^^

You can change the specified grammar terminals by using
function :func:`cfpq_data.grammars.utils.change_terminals.change_terminals_in_cfg`
from :ref:`grammars_utils`.

.. nbplot::

    brackets1 = cfpq_data.change_terminals_in_cfg(brackets, {"a": "b", "b": "c"})
    brackets1.to_text()  # 'S -> b S c\nS -> b c\n'

.. code-links::
