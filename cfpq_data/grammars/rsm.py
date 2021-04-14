"""Recursive State Machine [1]_.

References
----------
.. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
   and Semyon Grigorev "Context-Free Path Querying
   by Kronecker Product", ADBIS 2020, pp 49-59, 2020
"""
from typing import Tuple, Sequence

from pyformlang.cfg import Variable, CFG, Production, Terminal
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["RSM"]


class RSM:
    """Recursive State Machine [1]_.

    References
    ----------
    .. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """

    def __init__(
        self,
        start_symbol: Variable,
        boxes: Sequence[Tuple[Variable, DeterministicFiniteAutomaton]],
    ):
        """Initialize a Recursive State Machine [1]_.

        References
        ----------
        .. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
           and Semyon Grigorev "Context-Free Path Querying
           by Kronecker Product", ADBIS 2020, pp 49-59, 2020
        """
        self.start_symbol: Variable = start_symbol
        self.boxes: Sequence[Tuple[Variable, DeterministicFiniteAutomaton]] = boxes

    def to_text(self) -> str:
        """Turns the Recursive State Machine [1]_
        into its string representation.

        Returns
        -------
        text : str
            The Recursive State Machine as a string.

        References
        ----------
        .. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
           and Semyon Grigorev "Context-Free Path Querying
           by Kronecker Product", ADBIS 2020, pp 49-59, 2020
        """
        productions = [f"{box[0]} -> {box[1].to_regex()}" for box in self.boxes]
        return "\n".join(productions)

    def contains(self, word: str) -> bool:
        """ Gives the membership of a word
        to the Recursive State Machine [1]_

        Parameters
        ----------
        word : str
            The word to check.

        Returns
        ----------
        contains : bool
            Whether word if in the Recursive State Machine or not.

        References
        ----------
        .. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
           and Semyon Grigorev "Context-Free Path Querying
           by Kronecker Product", ADBIS 2020, pp 49-59, 2020
        """
        variables = set()
        terminals = set()
        productions = set()

        for symbol, dfa in self.boxes:
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
            start_symbol=self.start_symbol,
            productions=productions,
        ).contains(word)
