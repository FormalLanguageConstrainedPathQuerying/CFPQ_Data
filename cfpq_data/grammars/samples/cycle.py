"""Sample grammars for `labeled_cycle_graph`.
"""
from pyformlang.cfg import CFG

__all__ = ["a_star_0", "a_star_1", "a_star_2"]
a_star_0 = CFG.from_text("S -> a S | epsilon")
a_star_1 = CFG.from_text("S -> S S | a")
a_star_2 = CFG.from_text("S -> S S | S S S | a")
