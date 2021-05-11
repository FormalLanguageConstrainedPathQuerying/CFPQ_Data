"""Sample grammars for `labeled_two_cycles_graph`.
"""
from pyformlang.cfg import CFG

__all__ = [
    "brackets",
]

#: $S \, \rightarrow \, a \, S \, b \, \mid \, a \, b \, \\$
brackets = CFG.from_text("S -> a S b | a b")
