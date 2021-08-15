"""Create a context-free grammar
from different formats.
"""
import re

from pyformlang.cfg import CFG, Variable, Production, Terminal
from pyformlang.rsa import RecursiveAutomaton as RSA

from cfpq_data.grammars.rsm import RSM

__all__ = [
    "cfg_from_cnf",
    "cfg_from_rsm",
    "cfg_from_rsa",
]


def cfg_from_cnf(cnf: CFG) -> CFG:
    """Create a context-free grammar [2]_
    from given context-free grammar
    in Chomsky normal form [1]_.

    Parameters
    ----------
    cnf : CFG
        Context free grammar
        in Chomsky normal form.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a S b S | epsilon")
    >>> cfg = cfpq_data.cfg_from_cnf(cnf)
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    return CFG.from_text(cnf.to_text(), cnf.start_symbol)


# TODO: Remove in cfpq_data 2.0.0
def cfg_from_rsm(rsm: RSM) -> CFG:
    """Create a context-free grammar [1]_
    from given Recursive State Machine [2]_.

    .. deprecated:: 2.0.0

       The function `cfg_from_rsm` will be replaced
       with function `cfg_from_rsa`

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> cfg = cfpq_data.cfg_from_rsm(rsm)
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    .. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    import warnings

    msg = (
        "\nThe function `cfg_from_rsm` will be replaced "
        "with function `cfg_from_rsa` in "
        "cfpq_data 2.0.0\n"
    )

    warnings.warn(msg, FutureWarning, stacklevel=2)

    return rsm.to_cfg()


def cfg_from_rsa(rsa: RSA) -> CFG:
    """Create a context-free grammar [1]_
    from given Recursive State Automaton [2]_.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = CFG.from_text("S -> (a S* b S*)*")
    >>> rsa = RSA.from_cfg(cfg)
    >>> cfg = cfpq_data.cfg_from_rsa(rsa)
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    .. [2] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    variables = set()
    terminals = set()
    productions = set()

    for symbol in rsa.labels:
        dfa = rsa.get_box(symbol).dfa

        variables.add(Variable(symbol.value))

        naming = {dfa.start_state: Variable(symbol.value)}

        for state in dfa.states:
            if state not in naming:
                naming[state] = Variable(f"S{len(naming)}")
                variables.add(naming[state])

            if state in dfa.final_states:
                productions.add(Production(naming[state], []))

        for v, label, to in dfa._transition_function.get_edges():
            if label.value == label.value.lower():
                try:
                    label_value = re.search('"TER:(.*)"', label.value).group(1)
                except AttributeError:
                    label_value = label.value

                terminals.add(Terminal(label_value))
                production_label = Terminal(label_value)
            else:
                try:
                    label_value = re.search('"VAR:(.*)"', label.value).group(1)
                except AttributeError:
                    label_value = label.value

                production_label = Variable(label_value)

            productions.add(Production(naming[v], [production_label, naming[to]]))

    return CFG(
        variables=variables,
        terminals=terminals,
        start_symbol=Variable(rsa.initial_label.value),
        productions=productions,
    )
