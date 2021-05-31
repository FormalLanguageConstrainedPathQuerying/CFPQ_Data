# ## Tutorial
#
# Release
#
# :   1.0.1
#
# Date
#
# :   May 31, 2021
#
# This guide can help you start working with CFPQ_Data.
# You can download this tutorial as a Jupyter Notebook from the link at the end of the page.
#
# All functions are documented on the Reference page.
#
# ### Graphs
#
# You are able to get a synthetic or real-world graph with CFPQ_Data.
#
# #### Create a synthetic graph
#
# You can create many different synthetic graphs by using functions from Graph generators.
#
# For example, let's create a one cycle graph, the edges of which are marked with the letter `a`.

import cfpq_data
cycle = cfpq_data.labeled_cycle_graph(5, edge_label="a")

# # Get a real graph
#
# You can get many different real-world graphs from CFPQ_Data Dataset.
#
# And present these graphs in convenient formats by using functions from Reading and writing graphs.
#
# For example, let's get a `generations` ontology graph.

generations = cfpq_data.graph_from_dataset("generations")

# # Change labels
#
# You can change the specified graph labels by using function `cfpq_data.graphs.utils.change_edges()`
# from Graph utilities.

new_cycle = cfpq_data.change_edges(cycle, {"a": "b"})

# Now the labels `a` have changed to `b`.
#
#  Grammars
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
# # Create a context-free grammar
#
# You can create context-free grammar by using function `cfpq_data.grammars.readwrite.cfg.cfg_from_text()`
# from Reading and writing grammars.

cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")

# # Use predefined context-free grammar
#
# CFPQ_Data has many predefined grammars documented on the Grammar samples page.

brackets = cfpq_data.brackets
brackets.to_text()  # 'S -> a S b\nS -> a b\n'

# # Change terminals
#
# You can change the specified grammar terminals by using
# function `cfpq_data.grammars.utils.change_terminals.change_terminals_in_cfg()`
# from Grammar utilities.

brackets1 = cfpq_data.change_terminals_in_cfg(brackets, {"a": "b", "b": "c"})
brackets1.to_text()  # 'S -> b S c\nS -> b c\n'
