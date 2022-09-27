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

You can create your own grammar or use a predefined one.

Regular grammars
^^^^^^^^^^^^^^^^
Currently, we have one representation of regular grammars documented on the :ref:`grammars` page:

1. `Regular expression <https://en.wikipedia.org/wiki/Regular_expression#Formal_definition>`_

Create a regular expression
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create a regular expression by using function `regex_from_text <cfpq_data.grammars.readwrite.regex.regex_from_text>`
from :ref:`grammars_readwrite`.

.. nbplot::

    regex = cfpq_data.regex_from_text("a (bc|d*)")

.. code-links::

Сontext-free grammars
^^^^^^^^^^^^^^^^^^^^^
Currently, we have three representations of context-free grammars (CFGs) documented on the :ref:`grammars` page:

1. `Classic <https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions>`_
2. `Chomsky Normal Form <https://en.wikipedia.org/wiki/Chomsky_normal_form>`_
3. `Recursive State Machine <https://link.springer.com/chapter/10.1007/978-3-030-54832-2_6#Sec2>`_

Create a context-free grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create a context-free grammar by using function `cfg_from_text <cfpq_data.grammars.readwrite.cfg.cfg_from_text>`
from :ref:`grammars_readwrite`.

.. nbplot::

    cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

.. code-links::

Benchmarks
----------

You can download one of the prepared benchmarks that contains graphs, queries, other input data, and results for
a particular formal-language-constrained path querying problem.

Currently, we provide the following benchmarks documented on the :ref:`benchmarks` page:

1. :ref:`msreachability`

Load benchmark archive
^^^^^^^^^^^^^^^^^^^^^^

You can load the archive with the benchmark using function `download_benchmark <cfpq_data.dataset.download_benchmark>`.

.. nbplot::

   ms_reachability_path = cfpq_data.download_benchmark("MS_Reachability")

MS_Reachability benchmark
^^^^^^^^^^^^^^^^^^^^^^^^^

MS_Reachability benchmark can be used for the experimental study of the algorithms that solve the multiple-source
formal-language-constrained reachability problem. This benchmark is described on the :ref:`msreachability` page.

For this benchmark we provide some useful functions from
:ref:`multiple_source_utils <cfpq_data.graphs.utils.multiple_source_utils>`.
For example, you can save the list of source vertices to the TXT file or read it from loaded benchmark by using
functions `multiple_source_from_txt <cfpq_data.graphs.utils.multiple_source_utils.multiple_source_from_txt>` and
`multiple_source_to_txt <cfpq_data.graphs.utils.multiple_source_utils.multiple_source_to_txt>`.

.. nbplot::

    l = [1, 2, 5, 10]
    path = multiple_source_to_txt(l, "test.txt")
    source_vertices = multiple_source_from_txt(path)
.. code-links::
