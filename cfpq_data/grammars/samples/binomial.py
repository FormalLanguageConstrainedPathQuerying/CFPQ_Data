"""Sample grammars for `labeled_binomial_graph`.
"""
from pyformlang.cfg import CFG

__all__ = ["sg"]
sg = CFG.from_text("S -> a_r a | a_r S a")
