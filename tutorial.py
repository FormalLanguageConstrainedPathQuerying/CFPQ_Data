# ## Tutorial
#
# Release
#
# :   2.0.0
#
# Date
#
# :   Nov 07, 2021
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
# You can create your own context-free grammar (CFG) or use a predefined one.
# Now we have three representations of CFG documented on the Grammars page:
#
# 1. [Classic](https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions)
#
# 1. [Chomsky Normal Form](https://en.wikipedia.org/wiki/Chomsky_normal_form)
#
# 1. [Recursive State Machine](https://link.springer.com/chapter/10.1007/978-3-030-54832-2_6#Sec2)
#
# ## Create a context-free grammar
#
# You can create context-free grammar by using function `cfg_from_text`
# from Reading and writing grammars.

cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")
