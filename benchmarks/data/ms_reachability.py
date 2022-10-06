# ## MS_Reachability
#
# ### Info
#
# ### Description
#
# This benchmark contains graphs, queries, sets of source vertices, and results for the multiple-source
# formal-language-constrained reachability problem.
# For each graph we provide the following benchmark information:
#
# * **graph** -- contains a graph and its statistics (.csv + .md)
#
# * **queries** -- contains different regular queries in the form of regular expressions
#
# * **results** -- contains files with pairs of vertices <src, dest>  where 'src' is a source vertex and 'dest' is a vertex reachable from the 'src' vertex with respect to a particular query and a set of source vertices
#
# * **src_vertices** -- contains different sets of source vertices
#
# More information about multiple-source formal-language-constrained reachability problem can be found in
# ["Multiple-Source Context-Free Path Querying in Terms of Linear Algebra"](https://openproceedings.org/2021/conf/edbt/p48.pdf)
#
# ### Graphs Used
#
# ### Query Examples
#
# $$
# \textit{type} \, \textit{isDefinedBy}^{*} \, \textit{type}\\
# $$
#
# [Pyformlang Regex](https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html#pyformlang.regular_expression.Regex):
#
# ```
# type isDefinedBy* type
# ```
#
#
# ---
#
# $$
# (\textit{rest} \, | \, \textit{label} \, | \, \textit{range} \, | \, \textit{type} \, | \, \textit{comment}) \, \textit{seeAlso}^{*}\\
# $$
#
# [Pyformlang Regex](https://pyformlang.readthedocs.io/en/latest/modules/regular_expression.html#pyformlang.regular_expression.Regex):
#
# ```
# (rest | label | range | type | comment) seeAlso*
# ```
#
# ### Useful utilities
#
# For this benchmark we provide some useful functions from
# Graph utilities.
# For example, the set of source vertices can be saved to the TXT file or it can be loaded from benchmark by using
# functions `multiple_source_from_txt` and
# `multiple_source_to_txt`.

import cfpq_data

s = {1, 2, 5, 10}
path = cfpq_data.multiple_source_to_txt(s, "test.txt")
source_vertices = cfpq_data.multiple_source_from_txt(path)
