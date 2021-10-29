.. _tutorial:

.. currentmodule:: cfpq_data

Tutorial
========

.. only:: html

   :Release: |release|
   :Date: |today|

This guide can help you start working with CFPQ_Data.

**You can download this tutorial as a Jupyter Notebook from the link at the end of the page.**

.. topic:: NetworkX

    We use the NetworkX `MultiDiGraph
    <https://networkx.org/documentation/latest/reference/classes/multidigraph.html>`_ to represent the labeled graph.
    To familiarize yourself with this representation and find useful functions, see `NetworkX tutorial
    <https://networkx.org/documentation/latest/tutorial.html>`_.

.. topic:: Pyformlang

    We use the Pyformlang `CFG
    <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_ to represent
    the context-free grammar.
    To familiarize yourself with this representation and find useful functions, see `Pyformlang usage
    <https://pyformlang.readthedocs.io/en/latest/usage.html#context-free-grammar>`_.

.. note::

   All functions are documented on the :ref:`reference` page.

Import
------

First you need to import the package.

.. nbplot::

   import cfpq_data

Load graph
----------

After the package is imported, we can load the graphs.

Load graph archive from Dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can load the archive with the graph using function `download <cfpq_data.dataset.download>`.

.. nbplot::

   bzip_path = cfpq_data.download("bzip")

Load graph by path
^^^^^^^^^^^^^^^^^^

We can load the graph along the specified path using function `graph_from_csv <cfpq_data.graphs.readwrite.csv.graph_from_csv>`.

.. nbplot::

   bzip = cfpq_data.graph_from_csv(bzip_path)

Create graph
------------

We can also create a synthetic graph using one of the generators in module :ref:`graphs_generators`.

Create a one cycle graph
^^^^^^^^^^^^^^^^^^^^^^^^

For example, let's create a one cycle graph, with 5 nodes, the edges of which are marked with the letter ``a``.

.. nbplot::

    cycle = cfpq_data.labeled_cycle_graph(5, label="a")

Change edges
------------

We can change the specified graph labels by using function `change_edges <cfpq_data.graphs.utils.change_edges>`
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

You can create context-free grammar by using function `cfg_from_text <cfpq_data.grammars.readwrite.cfg.cfg_from_text>`
from :ref:`grammars_readwrite`.

.. nbplot::

    cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

.. code-links::
