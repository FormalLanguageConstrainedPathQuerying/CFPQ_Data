from __future__ import annotations

from typing import AbstractSet, Iterable, Optional
from abc import abstractmethod, ABC

from pyformlang.cfg import *


class Grammar(ABC):
    """
    Grammar - a class representing a context free base grammars
    """

    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[Production] = None):
        """
        Generic constructor

        :param variables: set of :class:`~pyformlang.cfg.Variable`, optional
        The variables of the CFG
        :param terminals: set of :class:`~pyformlang.cfg.Terminal`, optional
        The terminals of the CFG
        :param start_symbol: :class:`~pyformlang.cfg.Variable`, optional
        The start symbol
        :param productions: set of :class:`~pyformlang.cfg.Production`, optional
        The productions or rules of the CFG
        """
        self.variables = variables
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions


class BaseGrammar(Grammar):

    pass


class CNFGrammar(Grammar):
    """
    CNFGrammar - a class representing a context free grammar in Chomsky Normal Form
    """

    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[Production] = None):
        """
        CNFGrammar constructor

        :param variables: set of :class:`~pyformlang.cfg.Variable`, optional
        The variables of the CFG
        :param terminals: set of :class:`~pyformlang.cfg.Terminal`, optional
        The terminals of the CFG
        :param start_symbol: :class:`~pyformlang.cfg.Variable`, optional
        The start symbol
        :param productions: set of :class:`~pyformlang.cfg.Production`, optional
        The productions or rules of the CFG
        """
        cfg = CFG(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )
        eps = cfg.generate_epsilon()
        cfg = cfg.to_normal_form()

        if eps is True:
            cfg._productions |= {Production(cfg._start_symbol, [])}

        super(CNFGrammar, self).__init__(
            variables=cfg._variables,
            terminals=cfg._terminals,
            start_symbol=cfg._start_symbol,
            productions=cfg._productions
        )

    def dump_to_txt(self, path: str) -> str:
        """
        Saving grammar to txt file

        :param path: path to txt file
        :return: path
        """
        cfg = CFG(
            variables=self.variables,
            terminals=self.terminals,
            start_symbol=self.start_symbol,
            productions=self.productions
        )
        with open(path, 'w') as f:
            f.write(cfg.to_text())
        return path


class RSA(Grammar):
    """
    RSA - Recursive State Automata
    """
    def __init__(self,
                 start_symbol: Variable = None,
                 boxes: dict = None):
        self.variables = set()
        self.terminals = set()
        self.productions = set()

        self.start_symbol = start_symbol
        self.boxes = boxes

        cnt = 1
        for x in boxes:
            head = Variable(x)
            self.variables.add(head)
            for box in boxes[x]:
                name = {box.start_state: head}
                for s in box.states:
                    if s not in name:
                        name[s] = Variable(f'S{cnt}')
                        cnt += 1
                        self.variables.add(name[s])
                    if s in box.final_states:
                        self.productions.add(Production(name[s], []))
                for v in box._transition_function._transitions:
                    for label in box._transition_function._transitions[v]:
                        to = box._transition_function._transitions[v][label]

                        if label.value == label.value.lower():
                            self.terminals.add(Terminal(label.value))
                            self.productions.add(Production(name[v], [Terminal(label.value), name[to]]))
                        else:
                            self.productions.add(Production(name[v], [Variable(label.value), name[to]]))
        super(RSA, self).__init__(
            variables=self.variables,
            terminals=self.terminals,
            start_symbol=self.start_symbol,
            productions=self.productions
        )
