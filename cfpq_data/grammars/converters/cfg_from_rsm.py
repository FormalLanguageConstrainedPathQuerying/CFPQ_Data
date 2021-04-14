"""Create a context free grammar [1]_
from Recursive State Machine [2]_.

References
----------
.. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
.. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
   and Semyon Grigorev "Context-Free Path Querying
   by Kronecker Product", ADBIS 2020, pp 49-59, 2020
"""
from pyformlang.cfg import CFG, Variable, Production, Terminal

from cfpq_data.grammars.rsm import RSM

__all__ = ["cfg_from_rsm"]


def cfg_from_rsm(rsm: RSM) -> CFG:
    """Create a context free grammar [1]_
    from Recursive State Machine [2]_.

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_txt("S -> a S* b S* | epsilon")
    >>> cfg = cfpq_data.cfg_from_rsm(rsm)
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    .. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    variables = set()
    terminals = set()
    productions = set()

    for symbol, dfa in rsm.boxes:
        variables.add(Variable(symbol))

        naming = {dfa.start_state: Variable(symbol)}

        for state in dfa.states:
            if state not in naming:
                naming[state] = Variable(f"S{len(naming)}")
                variables.add(naming[state])

            if state in dfa.final_states:
                productions.add(Production(naming[state], []))

        for v, label, to in dfa._transition_function.get_edges():
            if label.value == label.value.lower():
                terminals.add(Terminal(label.value))
                mid = Terminal(label.value.lower())
            else:
                mid = Variable(label.value.upper())

            productions.add(Production(naming[v], [mid, naming[to]]))

    return CFG(
        variables=variables,
        terminals=terminals,
        start_symbol=rsm.start_symbol,
        productions=productions,
    )
