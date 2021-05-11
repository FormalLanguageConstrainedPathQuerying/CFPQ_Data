"""Sample grammars for RDF part of CFPQ_Data dataset.
Introduced in `"Context-Free Path Queries on RDF Graphs" <https://arxiv.org/abs/1506.00743>`_
"""
from pyformlang.cfg import CFG

__all__ = [
    "g1",
    "g2",
    "geo",
]

#: $S \, \rightarrow \, \overline{subClassOf} \, S \, subClassOf \, \mid \,
#: \overline{subClassOf} \, subClassOf \, \\
#: S \, \rightarrow \, \overline{type} \, S \, type \, \mid \,
#: \overline{type} \, type \, \\$
g1 = CFG.from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")

#: $S \, \rightarrow \, \overline{subClassOf} \, S \, subClassOf \, \mid \,
#: \overline{subClassOf} \, subClassOf \, \\$
g2 = CFG.from_text("S -> sco_r S sco | sco")

#: $S \, \rightarrow \, broaderTransitive \, S \, \overline{broaderTransitive} \, \mid \,
#: broaderTransitive \, \overline{broaderTransitive} \, \\$
geo = CFG.from_text("S -> bt S bt_r | bt bt_r")
