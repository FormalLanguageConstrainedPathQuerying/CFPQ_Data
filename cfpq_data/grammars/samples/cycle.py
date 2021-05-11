"""Sample grammars for `labeled_cycle_graph`.
"""
from pyformlang.cfg import CFG

__all__ = [
    "a_star_0",
    "a_star_1",
    "a_star_2",
]

#: $S \, \rightarrow \, a \, S \, \mid \, \varepsilon \, \\$
a_star_0 = CFG.from_text("S -> a S | epsilon")

#: $S \, \rightarrow \, S \, S \, \mid \, a \, \mid \, \varepsilon \, \\$
a_star_1 = CFG.from_text("S -> S S | a | epsilon")

#: $S \, \rightarrow \, S \, S \, \mid \, \, S \, S \, S \, \mid \,
#: a \, \mid \, \varepsilon \, \\$
a_star_2 = CFG.from_text("S -> S S | S S S | a | epsilon")
