"""Create a context free grammar
in Chomsky normal form [1]_
from given context free grammar [2]_.

References
----------
.. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
.. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
"""
from pyformlang.cfg import CFG, Production

__all__ = ["cnf_from_cfg"]


def cnf_from_cfg(cfg: CFG) -> CFG:
    """Create a context free grammar
    in Chomsky normal form [1]_
    from given context free grammar [2]_.

    Parameters
    ----------
    cfg : CFG
        Context free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_txt("S -> a S b S | epsilon")
    >>> cnf = cfpq_data.cnf_from_cfg(cfg)
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context free grammar in Chomsky normal form.

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
