"""Create a context-free grammar from different formats."""
import logging
import re

from pyformlang.cfg import CFG, Variable, Production, Terminal
from pyformlang.rsa import RecursiveAutomaton as RSA

__all__ = [
    "cfg_from_cnf",
    "cfg_from_rsa",
]


def cfg_from_cnf(cnf: CFG) -> CFG:
    """Create a context-free grammar [2]_ from given context-free grammar
    in Chomsky normal form [1]_.

    Parameters
    ----------
    cnf : CFG
        Context free grammar in Chomsky normal form.

    Examples
    --------
    >>> from cfpq_data import *
    >>> gr = cnf_from_text("S -> a b")
    >>> cfg = cfg_from_cnf(gr)
    >>> cfg_to_text(cfg)
    'S -> a#CNF# b#CNF#\\na#CNF# -> a\\nb#CNF# -> b'

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    cfg = CFG.from_text(cnf.to_text(), cnf.start_symbol)

    logging.info(f"Create {cfg=} from {cnf=}")

    return cfg


def cfg_from_rsa(rsa: RSA) -> CFG:
    """Create a context-free grammar [1]_ from given Recursive State Automaton [2]_.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    Examples
    --------
    >>> from cfpq_data import *
    >>> gr = rsa_from_text("S -> (a | b)*")
    >>> cfg = cfg_from_rsa(gr)
    >>> cfg_to_text(cfg)
    'S -> \\nS -> a S\\nS -> b S'

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

    cfg = CFG(
        variables=variables,
        terminals=terminals,
        start_symbol=Variable(rsa.initial_label.value),
        productions=productions,
    )

    logging.info(f"Create {cfg=} from {rsa=}")

    return cfg
