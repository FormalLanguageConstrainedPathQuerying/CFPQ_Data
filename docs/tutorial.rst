.. _tutorial:

.. currentmodule:: cfpq_data

Tutorial
========

.. only:: html

   :Release: |release|
   :Date: |today|

This guide can help you start working with CFPQ_Data.

**You can download this tutorial as a Jupyter Notebook from the link at the end of the page.**

**NetworkX.** We use the NetworkX `MultiDiGraph
<https://networkx.org/documentation/latest/reference/classes/multidigraph.html>`_ to represent the labeled graph.
To familiarize yourself with this representation and find useful functions, see `NetworkX tutorial
<https://networkx.org/documentation/latest/tutorial.html>`_.

**Pyformlang.** We use the Pyformlang `Regex
<https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html>`_ to represent regular grammars.
Also, we use the Pyformlang `CFG
<https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_ and `RSA
<https://pyformlang.readthedocs.io/en/latest/modules/rsa.html>`_ to represent context-free grammars.
To familiarize yourself with this representations and find useful functions, see `Pyformlang usage
<https://pyformlang.readthedocs.io/en/latest/usage.html>`_.

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

We can load the archive with the graph using function :obj:`download <cfpq_data.dataset.download>`.

.. nbplot::

   bzip_path = cfpq_data.download("bzip")

Load graph by path
^^^^^^^^^^^^^^^^^^

The archive unpacks to a directory with one MatrixMarket file per edge
label in its ``graph`` subdirectory (see :ref:`graph_file_structure`). We
can load the graph along the specified path using function
:obj:`graph_from_mtx_dir <cfpq_data.graphs.readwrite.mtx.graph_from_mtx_dir>`.

.. nbplot::

   bzip = cfpq_data.graph_from_mtx_dir(bzip_path / "graph")

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

We can change the specified graph labels by using function :obj:`change_edges <cfpq_data.graphs.utils.change_edges>`
from :ref:`graphs_utils`.

.. nbplot::

    new_cycle = cfpq_data.change_edges(cycle, {"a": "b"})

Now the labels ``a`` have changed to ``b``.

Add reverse edges
-----------------

In addition, we can add reverse edges to the graph by using function :obj:`add_reverse_edges <cfpq_data.graphs.utils.add_reverse_edges>`
from :ref:`graphs_utils`. This is extremely useful if graph analysis is formulated using such reverse edges.

.. nbplot::

    new_cycle_with_reversed = cfpq_data.add_reverse_edges(new_cycle)

Now, for each edge with label ``a`` this graph contains the reversed edge with label ``a_r``.

Load grammar
------------

Graph archives from the dataset are self-contained: besides the graph they carry the
queries that apply to the graph under ``queries/`` — one directory per query with its
grammar template and a precomputed ``results.mtx`` (see :ref:`graph_file_structure`).
The grammar templates themselves are described on the :ref:`grammar_templates` page.

A grammar template may use indexed symbols (e.g. ``load_i``); we materialize it over a
concrete graph with functions :obj:`cnf_template_from_text <cfpq_data.queries.cfpq.readwrite.cnf_template.cnf_template_from_text>`
and :obj:`materialize <cfpq_data.queries.cfpq.readwrite.cnf_template.materialize>`,
which expand every index present in the graph edge labels:

.. nbplot::

    import networkx as nx
    g = nx.MultiDiGraph()
    _ = g.add_edges_from(
        [(0, 1, {"label": "load_0"}), (1, 2, {"label": "store_0"}),
         (0, 3, {"label": "alloc"})]
    )
    text = ("PT\tPTh\talloc\n"
            "PT\talloc\n"
            "PTh\tload_i\tAl_st_PTh_i\n"
            "Al_st_PTh_i\tAl\tst_PTh_i\n"
            "st_PTh_i\tstore_i\tPTh\n"
            "Al\tPT\n"
            "\n"
            "Count:\n"
            "PT")
    template = cfpq_data.cnf_template_from_text(text)
    cfg = cfpq_data.materialize(template, g)

Regular grammars
----------------

Currently, we have one representation of regular grammars:

1. `Regular expression <https://en.wikipedia.org/wiki/Regular_expression#Formal_definition>`_

Create a regular expression
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, a regular expression can be created by using function :obj:`regex_from_text <cfpq_data.queries.rpq.readwrite.regex.regex_from_text>`
from :ref:`cfpq_readwrite`.

.. nbplot::

    regex = cfpq_data.regex_from_text("a (bc|d*)")

Load regular expression by path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can load the regular expression along the specified path using function :obj:`regex_from_txt <cfpq_data.queries.rpq.readwrite.regex.regex_from_txt>`.

.. nbplot::
   path = cfpq_data.regex_to_txt(regex, "test.txt")
   regex_by_path = cfpq_data.regex_from_txt(path)

Сontext-free grammars
---------------------

Currently, we have three representations of context-free grammars (CFGs):

1. `Classic <https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions>`_
2. `Chomsky Normal Form <https://en.wikipedia.org/wiki/Chomsky_normal_form>`_
3. `Recursive State Machine <https://link.springer.com/chapter/10.1007/978-3-030-54832-2_6>`_

Create a classic context-free grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A classic context-free grammar can be created by using function :obj:`cfg_from_text <cfpq_data.queries.cfpq.readwrite.cfg.cfg_from_text>`
from :ref:`cfpq_readwrite`.

.. nbplot::

    cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

Load context-free grammar by path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can load the classic context-free grammar along the specified path using function :obj:`cfg_from_txt <cfpq_data.queries.cfpq.readwrite.cfg.cfg_from_txt>`.

.. nbplot::
   path = cfpq_data.cfg_to_txt(cfg, "test.txt")
   cfg_by_path = cfpq_data.cfg_from_txt(path)

Generate grammar
----------------

We can also generate a grammar for specified template using one of the generators in module :ref:`cfpq_generators`.

Generate a Dyck grammar
^^^^^^^^^^^^^^^^^^^^^^^

For example, let's generate a :ref:`dyck` grammar of the balanced strings with ``a`` as an opening parenthesis, ``b`` as a closing parenthesis, and without the empty string.

.. nbplot::

    dyck_cfg = cfpq_data.dyck_grammar([("a", "b")], eps=False)

Generate a Java Points-to grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Also, let's generate a :ref:`java_points-to` grammar for the field-sensitive analysis of Java programs with field names ``f0`` and ``f1``.

.. nbplot::

    java_pt_cfg = cfpq_data.java_points_to_grammar(["f0", "f1"])

.. code-links::
