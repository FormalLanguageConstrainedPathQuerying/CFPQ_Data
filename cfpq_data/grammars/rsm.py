"""Recursive State Machine.
"""
import re
from typing import Tuple, Sequence

from pyformlang.cfg import Variable, CFG, Production, Terminal
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["RSM"]


class RSM:
    """Recursive State Machine [1]_.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
       Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """

    def __init__(
        self,
        start_symbol: Variable,
        boxes: Sequence[Tuple[Variable, DeterministicFiniteAutomaton]],
    ):
        """Initialize a Recursive State Machine [1]_.

        Parameters
        ----------
        start_symbol : Variable
            Start symbol of a Recursive State Machine.

        boxes : Sequence[Tuple[Variable, DeterministicFiniteAutomaton]]
            Boxes of a Recursive State Machine.

        References
        ----------
        .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
           Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
           Lecture Notes in Computer Science, vol 2102.
           Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
        """
        self.start_symbol: Variable = start_symbol
        self.boxes: Sequence[Tuple[Variable, DeterministicFiniteAutomaton]] = boxes

    def to_text(self) -> str:
        """Turns the Recursive State Machine [1]_
        into its string representation.

        Examples
        --------
        >>> import cfpq_data
        >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
        >>> text = rsm.to_text()

        Returns
        -------
        text : str
            The Recursive State Machine
            text representation.

        References
        ----------
        .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
           Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
           Lecture Notes in Computer Science, vol 2102.
           Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
        """
        productions = [f"{box[0]} -> {box[1].to_regex()}" for box in self.boxes]
        return "\n".join(productions)

    def to_cfg(self):
        """Create a context-free grammar [1]_
        from Recursive State Machine [2]_.

        Examples
        --------
        >>> import cfpq_data
        >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
        >>> cfg = rsm.to_cfg()
        >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
        [True, True, True]

        Returns
        -------
        cfg : CFG
            Context-free grammar.

        References
        ----------
        .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
        .. [2] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
           Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
           Lecture Notes in Computer Science, vol 2102.
           Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
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
            start_symbol=self.start_symbol,
            productions=productions,
        )

    def contains(self, word: str) -> bool:
        """Gives the membership of a word
        to the Recursive State Machine [1]_

        Parameters
        ----------
        word : str
            The word to check.

        Examples
        --------
        >>> import cfpq_data
        >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
        >>> [rsm.contains(word) for word in ["", "ab", "aabb"]]
        [True, True, True]

        Returns
        ----------
        contains : bool
            Whether word if in the Recursive State Machine or not.

        References
        ----------
        .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
           Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
           Lecture Notes in Computer Science, vol 2102.
           Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
        """
        return self.to_cfg().contains(word)
