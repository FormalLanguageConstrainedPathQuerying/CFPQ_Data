"""Sample grammars for `labeled_two_cycles_graph`.
"""
from pyformlang.cfg import CFG

__all__ = ["brackets"]
brackets = CFG.from_text("S -> a S b | a b")
