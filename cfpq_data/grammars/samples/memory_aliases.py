"""Sample grammars for MemoryAliases part of CFPQ_Data dataset.
"""
from pyformlang.cfg import CFG

from cfpq_data.grammars.creators.rsm_from_txt import rsm_from_txt

__all__ = ["g1", "g2"]
g1 = CFG.from_text(
    """
    S -> d_r V d
    V -> V1 V2 V3
    V1 -> epsilon
    V1 -> V2 a_r V1
    V2 -> epsilon
    V2 -> S
    V3 -> epsilon
    V3 -> a V2 V3
    """
)
g2 = rsm_from_txt("S -> d_r V d\nV -> ((S?) a_r)* (S?) (a (S?))*")
