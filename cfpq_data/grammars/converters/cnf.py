"""Create a context-free grammar
in Chomsky normal form
from different formats.
"""
from pyformlang.cfg import CFG, Production
from pyformlang.rsa import RecursiveAutomaton as RSA

from cfpq_data.grammars.converters.cfg import cfg_from_rsm, cfg_from_rsa
from cfpq_data.grammars.rsm import RSM

__all__ = [
    "cnf_from_cfg",
    "cnf_from_rsm",
    "cnf_from_rsa",
]


def cnf_from_cfg(cfg: CFG) -> CFG:
    """Create a context-free grammar
    in Chomsky normal form [1]_
    from given context-free grammar [2]_.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_text("S -> a S b S | epsilon")
    >>> cnf = cfpq_data.cnf_from_cfg(cfg)
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    generate_epsilon = cfg.generate_epsilon()

    cnf = cfg.to_normal_form()

    if generate_epsilon is True:
        cnf._productions.add(Production(cnf.start_symbol, []))

    return cnf


# TODO: Remove in cfpq_data 2.0.0
def cnf_from_rsm(rsm: RSM) -> CFG:
    """Create a context-free grammar
    in Chomsky normal form [1]_
    from Recursive State Machine [2]_.

    .. deprecated:: 2.0.0

       The function `cnf_from_rsm` will be replaced
       with function `cnf_from_rsa`

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> cnf = cfpq_data.cnf_from_rsm(rsm)
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    import warnings

    msg = (
        "\nThe function `cnf_from_rsm` will be replaced "
        "with function `cnf_from_rsa` in "
        "cfpq_data 2.0.0\n"
    )

    warnings.warn(msg, FutureWarning, stacklevel=2)

    return cnf_from_cfg(cfg_from_rsm(rsm))


def cnf_from_rsa(rsa: RSA) -> CFG:
    """Create a context-free grammar
    in Chomsky normal form [1]_
    from Recursive State Automaton [2]_.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = CFG.from_text("S -> (a S* b S*)*")
    >>> rsa = RSA.from_cfg(cfg)
    >>> cnf = cfpq_data.cnf_from_rsa(rsa)
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    return cnf_from_cfg(cfg_from_rsa(rsa))
