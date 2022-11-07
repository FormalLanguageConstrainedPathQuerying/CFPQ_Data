# ## Tutorial
#
# Release
#
# :   4.0.0
#
# Date
#
# :   Nov 07, 2022
#
# This guide can help you start working with CFPQ_Data.
#
# **You can download this tutorial as a Jupyter Notebook from the link at the end of the page.**
#
# ### Import
#
# First you need to import the package.

import cfpq_data

# # Load graph
#
# After the package is imported, we can load the graphs.
#
# ## Load graph archive from Dataset
#
# We can load the archive with the graph using function `download`.

bzip_path = cfpq_data.download("bzip")

# # Load graph by path
#
# We can load the graph along the specified path using function `graph_from_csv`.

bzip = cfpq_data.graph_from_csv(bzip_path)

# Create graph
#
# We can also create a synthetic graph using one of the generators in module Graph generators.
#
# # Create a one cycle graph
#
# For example, let's create a one cycle graph, with 5 nodes, the edges of which are marked with the letter `a`.

cycle = cfpq_data.labeled_cycle_graph(5, label="a")

# Change edges
#
# We can change the specified graph labels by using function `change_edges`
# from Graph utilities.

new_cycle = cfpq_data.change_edges(cycle, {"a": "b"})

# Now the labels `a` have changed to `b`.
#
# # Grammars
#
# Also, we can create our own grammar or use a predefined one.
#
# ## Regular grammars
#
# Currently, we have one representation of regular grammars documented on the Grammars page:
#
# 1. [Regular expression](https://en.wikipedia.org/wiki/Regular_expression#Formal_definition)
#
# ## Create a regular expression
#
# A regular expression can be created by using function `regex_from_text`
# from Reading and writing grammars.

regex = cfpq_data.regex_from_text("a (bc|d*)")

# # Сontext-free grammars
#
# Currently, we have three representations of context-free grammars (CFGs) documented on the Grammars page:
#
# 1. [Classic](https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions)
#
# 1. [Chomsky Normal Form](https://en.wikipedia.org/wiki/Chomsky_normal_form)
#
# 1. [Recursive State Machine](https://link.springer.com/chapter/10.1007/978-3-030-54832-2_6#Sec2)
#
# # Create a context-free grammar
#
# A context-free grammar can be created by using function `cfg_from_text`
# from Reading and writing grammars.

cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

# Benchmarks
#
# In addition, one of the prepared benchmarks that contains graphs, queries, other input data, and results for
# a particular formal-language-constrained path querying problem can be downloaded.
#
# Currently, we provide the following benchmarks documented on the Benchmarks page:
#
# 1. MS_Reachability
#
# # Load benchmark archive
#
# You can load the archive with the benchmark using function `download_benchmark`.

ms_reachability_path = cfpq_data.download_benchmark("MS_Reachability")

# # MS_Reachability benchmark
#
# MS_Reachability benchmark can be used for the experimental study of the algorithms that solve the multiple-source
# formal-language-constrained reachability problem. This benchmark is described on the MS_Reachability page.
#
# For this benchmark we provide some useful functions from
# Graph utilities.
# For example, the set of source vertices can be saved to the TXT file or it can be loaded from benchmark by using
# functions `multiple_source_from_txt` and
# `multiple_source_to_txt`.

s = {1, 2, 5, 10}
path = cfpq_data.multiple_source_to_txt(s, "test.txt")
source_vertices = cfpq_data.multiple_source_from_txt(path)
