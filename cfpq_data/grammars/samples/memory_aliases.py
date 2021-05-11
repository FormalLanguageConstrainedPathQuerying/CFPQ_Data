"""Sample grammars for MemoryAliases part of CFPQ_Data dataset.
"""
from pyformlang.cfg import CFG

from cfpq_data.grammars.readwrite.rsm import rsm_from_text

__all__ = [
    "g1",
    "g2",
]

#: $S \, \rightarrow \, \overline{d} \, V \, d \, \\
#: V \, \rightarrow \, V_1 \, V_2 \, V_3 \, \\
#: V_1 \, \rightarrow \, \varepsilon \, \\
#: V_1 \, \rightarrow \, V_2 \, \overline{a} \, V_1 \, \\
#: V_2 \, \rightarrow \, \varepsilon \, \\
#: V_2 \, \rightarrow \, S \, \\
#: V_3 \, \rightarrow \, \varepsilon \, \\
#: V_3 \, \rightarrow \, a \, V_2 \, V_3 \, \\$
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

#: $S \, \rightarrow \, \overline{d} \, V \, d \, \\
#: V \, \rightarrow \, ((S?) \, \overline{a})^{*} \, (S?) \, (a \, (S?))^{*} \, \\$
g2 = rsm_from_text("S -> d_r V d\nV -> ((S?) a_r)* (S?) (a (S?))*")
