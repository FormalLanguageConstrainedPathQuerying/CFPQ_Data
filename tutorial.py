# ## Tutorial
#
# Release
#
# :   4.0.2
#
# Date
#
# :   Nov 30, 2022
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
# # Add reverse edges
#
# In addition, we can add reverse edges to the graph by using function `add_reverse_edges`
# from Graph utilities. This is extremely useful if graph analysis is formulated using such reverse edges.

new_cycle_with_reversed = cfpq_data.add_reverse_edges(new_cycle)

# Now, for each edge with label `a` this graph contains the reversed edge with label `a_r`.
#
# # Load grammar
#
# Also, we can load the grammars generated from grammar templates that are described on the Grammars page.
#
# ## Load grammars archive from Dataset
#
# We can load the archive with the grammars for the specified template using function `download_grammars`.

c_alias_path = cfpq_data.download_grammars("c_alias")

# # Load grammars archive for specified graph
#
# For some grammar templates we also can load the archive with the grammars for specific graphs.

java_pt_avrora_path = cfpq_data.download_grammars("java_points_to", graph_name="avrora")

# Regular grammars
#
# Currently, we have one representation of regular grammars:
#
# 1. [Regular expression](https://en.wikipedia.org/wiki/Regular_expression#Formal_definition)
#
# # Create a regular expression
#
# For example, a regular expression can be created by using function `regex_from_text`
# from Reading and writing grammars.

regex = cfpq_data.regex_from_text("a (bc|d*)")

# # Load regular expression by path
#
# We can load the regular expression along the specified path using function `regex_from_txt`.

path = cfpq_data.regex_to_txt(regex, "test.txt")
regex_by_path = cfpq_data.regex_from_txt(path)

# Сontext-free grammars
#
# Currently, we have three representations of context-free grammars (CFGs):
#
# 1. [Classic](https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions)
#
# 1. [Chomsky Normal Form](https://en.wikipedia.org/wiki/Chomsky_normal_form)
#
# 1. [Recursive State Machine](https://link.springer.com/chapter/10.1007/978-3-030-54832-2_6#Sec2)
#
# # Create a classic context-free grammar
#
# A classic context-free grammar can be created by using function `cfg_from_text`
# from Reading and writing grammars.

cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

# # Load context-free grammar by path
#
# We can load the classic context-free grammar along the specified path using function `cfg_from_txt`.

path = cfpq_data.cfg_to_txt(cfg, "test.txt")
cfg_by_path = cfpq_data.cfg_from_txt(path)

# Generate grammar
#
# We can also generate a grammar for specified template using one of the generators in module Grammar generators.
#
# # Generate a Dyck grammar
#
# For example, let's generate a Dyck grammar of the balanced strings with `a` as an opening parenthesis, `b` as a closing parenthesis, and without the empty string.

dyck_cfg = cfpq_data.dyck_grammar([("a", "b")], eps=False)

# # Generate a Java Points-to grammar
#
# Also, let's generate a Java Points-to grammar for the field-sensitive analysis of Java programs with field names `f0` and `f1`.

java_pt_cfg = cfpq_data.java_points_to_grammar(["f0", "f1"])

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
