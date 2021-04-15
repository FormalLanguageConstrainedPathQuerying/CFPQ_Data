"""Sample grammars for `labeled_barabasi_albert_graph`.
"""
from pyformlang.cfg import CFG

__all__ = ["an_bm_cm_dn"]
an_bm_cm_dn = CFG.from_text("S -> a S d | a X d\nX -> b X c | b c")
