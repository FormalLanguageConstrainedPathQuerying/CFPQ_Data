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

    @classmethod
    def from_grammar(cls, grammar_base):  # Grammar -> Grammar
        """
        Converting grammars into different forms (for example Grammar into CNFGrammar)

        :param grammar_base: Grammar or CNFGrammar object
        :return: CNFGrammar or Grammar object
        """
        return cls(
            variables=grammar_base.variables,
            terminals=grammar_base.terminals,
            start_symbol=grammar_base.start_symbol,
            productions=grammar_base.productions
        )

    @classmethod
    def load_from_txt(cls, path, start_symbol=Variable("S")):
        """
        Uploading grammar from *.txt

        :param path: path to *.txt file with grammar
        :return: Grammar or CNFGrammar object
        """
        with open(path, 'r') as f:
            cfg = CFG.from_text(f.read(), start_symbol)

        return cls(
            cfg.variables,
            cfg.terminals,
            cfg.start_symbol,
            cfg.productions
        )

    def dump_to_txt(cls, path):
        """
        Saving grammar to *.txt file

        :param path: path to *.txt file
        :return: path
        """
        cfg = CFG(
            variables=cls.variables,
            terminals=cls.terminals,
            start_symbol=cls.start_symbol,
            productions=cls.productions
        )
        with open(path, 'w') as f:
            f.write(cfg.to_text())
        return path


class CNFGrammar(Grammar):
    """
    CNFGrammar - a class representing a context free grammars in chomsky normal form
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
