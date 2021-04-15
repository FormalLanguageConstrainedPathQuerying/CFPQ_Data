"""Sample grammars for RDF part of CFPQ_Data dataset.
"""
from pyformlang.cfg import CFG

__all__ = ["g1", "g2", "geo"]
g1 = CFG.from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")
g2 = CFG.from_text("S -> sco_r S sco | sco")
geo = CFG.from_text("S -> bt S bt_r | bt bt_r")
