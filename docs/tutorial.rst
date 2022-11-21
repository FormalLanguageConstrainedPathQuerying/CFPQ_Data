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

    We use the Pyformlang `Regex
    <https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html>`_ to represent regular grammars.
    Also, we use the Pyformlang `CFG
    <https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html>`_ and `RSA
    <https://pyformlang.readthedocs.io/en/latest/modules/rsa.html>`_ to represent context-free grammars.
    To familiarize yourself with this representations and find useful functions, see `Pyformlang usage
    <https://pyformlang.readthedocs.io/en/latest/usage.html>`_.

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

Load grammar
------------

Also, we can load the grammars generated from grammar templates that are described on the :ref:`grammar_templates` page.

Load grammars archive from Dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can load the archive with the grammars for the specified template using function `download_grammars <cfpq_data.dataset.download_grammars>`.

.. nbplot::

   c_alias_path = cfpq_data.download_grammars("c_alias")

Load grammars archive for specified graph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For some grammar templates we also can load the archive with the grammars for specific graphs.

.. nbplot::

   java_pt_avrora_path = cfpq_data.download_grammars("java_points_to", graph_name="avrora")

Regular grammars
----------------

Currently, we have one representation of regular grammars:

1. `Regular expression <https://en.wikipedia.org/wiki/Regular_expression#Formal_definition>`_

Create a regular expression
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, a regular expression can be created by using function `regex_from_text <cfpq_data.grammars.readwrite.regex.regex_from_text>`
from :ref:`grammars_readwrite`.

.. nbplot::

    regex = cfpq_data.regex_from_text("a (bc|d*)")

Load regular expression by path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can load the regular expression along the specified path using function `regex_from_txt <cfpq_data.grammars.readwrite.regex.regex_from_txt>`.

.. nbplot::
   path = cfpq_data.regex_to_txt(regex, "test.txt")
   regex_by_path = cfpq_data.regex_from_txt(path)

Сontext-free grammars
---------------------

Currently, we have three representations of context-free grammars (CFGs):

1. `Classic <https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions>`_
2. `Chomsky Normal Form <https://en.wikipedia.org/wiki/Chomsky_normal_form>`_
3. `Recursive State Machine <https://link.springer.com/chapter/10.1007/978-3-030-54832-2_6#Sec2>`_

Create a classic context-free grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A classic context-free grammar can be created by using function `cfg_from_text <cfpq_data.grammars.readwrite.cfg.cfg_from_text>`
from :ref:`grammars_readwrite`.

.. nbplot::

    cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

Load context-free grammar by path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can load the classic context-free grammar along the specified path using function `cfg_from_txt <cfpq_data.grammars.readwrite.cfg.cfg_from_txt>`.

.. nbplot::
   path = cfpq_data.cfg_to_txt(cfg, "test.txt")
   cfg_by_path = cfpq_data.cfg_from_txt(path)

Generate grammar
----------------

We can also generate a grammar for specified template using one of the generators in module :ref:`grammars_generators`.

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

Benchmarks
----------

In addition, one of the prepared benchmarks that contains graphs, queries, other input data, and results for
a particular formal-language-constrained path querying problem can be downloaded.

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
:ref:`graphs_utils`.
For example, the set of source vertices can be saved to the TXT file or it can be loaded from benchmark by using
functions `multiple_source_from_txt <cfpq_data.graphs.utils.multiple_source_utils.multiple_source_from_txt>` and
`multiple_source_to_txt <cfpq_data.graphs.utils.multiple_source_utils.multiple_source_to_txt>`.

.. nbplot::

    s = {1, 2, 5, 10}
    path = cfpq_data.multiple_source_to_txt(s, "test.txt")
    source_vertices = cfpq_data.multiple_source_from_txt(path)
.. code-links::
