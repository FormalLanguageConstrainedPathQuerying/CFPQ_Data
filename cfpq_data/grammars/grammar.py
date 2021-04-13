from __future__ import annotations

from typing import AbstractSet, Iterable, Optional
from abc import ABC

from pyformlang.cfg import *


class Grammar(ABC):
    """
    Grammar - a class representing a context free base grammars
    """

    variables: AbstractSet[Variable] = None
    terminals: AbstractSet[Terminal] = None
    start_symbol: Variable = None
    productions: Iterable[Production] = None


class BaseGrammar(Grammar):

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

        self.variables = cfg._variables
        self.terminals = cfg._terminals
        self.start_symbol = cfg._start_symbol
        self.productions = cfg._productions


class RSA(Grammar):
    """
    RSA - Recursive State Automata
    """
    def __init__(self,
                 start_symbol: Variable = None,
                 boxes: dict = None):

        self.start_symbol = start_symbol
        self.boxes = boxes
