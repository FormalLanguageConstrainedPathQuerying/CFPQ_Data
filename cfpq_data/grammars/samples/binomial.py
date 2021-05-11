"""Sample grammars for `labeled_binomial_graph`.
"""
from pyformlang.cfg import CFG

__all__ = [
    "sg",
]

#: $S \, \rightarrow \, \overline{a} \, S \, a \, \mid \,
#: \overline{a} \, a \, \\$
sg = CFG.from_text("S -> a_r S a | a_r a")
