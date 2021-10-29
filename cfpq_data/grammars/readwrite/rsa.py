"""Read (and write) a Recursive State Automaton from (and to) different sources."""
import logging
import pathlib
from typing import Union

from pyformlang.cfg import Epsilon, Variable, Production
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton.finite_automaton import to_symbol
from pyformlang.regular_expression import Regex
from pyformlang.rsa import Box, RecursiveAutomaton as RSA

__all__ = [
    "rsa_from_text",
    "rsa_to_text",
    "rsa_from_txt",
    "rsa_to_txt",
]


def rsa_from_text(text: str, *, start_symbol: Symbol = Symbol("S")) -> RSA:
    """Create a Recursive State Automaton [1]_ from text.

    Parameters
    ----------
    text : str
        The text with which the Recursive State Machine will be created.

    start_symbol : Symbol
        Start symbol of a Recursive State Machine.

    Examples
    --------
    >>> from cfpq_data import *
    >>> rsa = rsa_from_text("S -> a*")
    >>> cfg_to_text(cfg_from_rsa(rsa))
    'S -> \\nS -> a S'

    Returns
    -------
    rsa : RSA
        Recursive State Automaton.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    productions = dict()
    boxes = set()
    labels = set()

    for production in text.splitlines():
        if " -> " not in production:
            continue

        head, body = production.split(" -> ")
        labels.add(to_symbol(head))

        if body == "":
            body = Epsilon().to_text()

        if head in productions:
            productions[head] += " | " + body
        else:
            productions[head] = body

    for head, body in productions.items():
        boxes.add(Box(Regex(body).to_epsilon_nfa().minimize(), to_symbol(head)))

    rsa = RSA(labels=labels, initial_label=start_symbol, boxes=boxes)

    logging.info(f"Create {rsa=} from {text=}, {start_symbol=}")

    return rsa


def rsa_to_text(rsa: RSA) -> str:
    """Turns a Recursive State Automaton [1]_ into its text representation.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    Examples
    --------
    >>> from cfpq_data import *
    >>> rsa = rsa_from_text("S -> a*")
    >>> rsa_to_text(rsa)
    'S -> (a)*'

    Returns
    -------
    text : str
        Recursive State Automaton text representation.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    productions = []

    for symbol in rsa.labels:
        box = rsa.get_box(symbol)
        productions.append(f"{box.label.value} -> {box.dfa.to_regex()}")

    productions.sort(
        key=lambda s: (s.split(" -> ")[0] != rsa.initial_label.value, s),
    )

    text = "\n".join(productions)

    logging.info(f"Turn {rsa=} into {text=}")

    return text


def rsa_from_txt(
    path: Union[pathlib.Path, str], *, start_symbol: Symbol = Symbol("S")
) -> RSA:
    """Create a Recursive State Automaton [1]_ from TXT file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with which the Recursive State Machine
        will be created.

    start_symbol : Symbol
        Start symbol of a Recursive State Machine.

    Examples
    --------
    >>> from cfpq_data import *
    >>> rsa_1 = rsa_from_text("S -> a*")
    >>> path = rsa_to_txt(rsa_1, "test.txt")
    >>> rsa = rsa_from_txt(path)
    >>> rsa_to_text(rsa)
    'S -> (a)*'

    Returns
    -------
    rsa : RSA
        Recursive State Automaton.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    with open(path, "r") as f:
        productions = f.read()

    rsa = rsa_from_text(productions, start_symbol=start_symbol)

    logging.info(f"Create {rsa=} from {path=}, {start_symbol=}")

    return rsa


def rsa_to_txt(rsa: RSA, path: Union[pathlib.Path, str]) -> pathlib.Path:
    """Saves a Recursive State Automaton text representation into TXT file.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    path : Union[Path, str]
        The path to the TXT file where Recursive State Machine
        text representation will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> rsa = rsa_from_text("S -> (a S* b S*)*")
    >>> path = rsa_to_txt(rsa, "test.txt")

    Returns
    -------
    path : Path
        The path to the TXT file where Recursive State Automaton
        text representation will be saved.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    with open(path, "w") as f:
        f.write(rsa_to_text(rsa))

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {rsa=} to {dest=}")

    return dest
