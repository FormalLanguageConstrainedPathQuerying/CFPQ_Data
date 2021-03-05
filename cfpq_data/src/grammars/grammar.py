from typing import AbstractSet, Iterable, Optional
from abc import abstractmethod, ABC

from pyformlang.cfg import *


class Grammar(ABC):

    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[Production] = None):
        self.variables = variables
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions

    @classmethod
    @abstractmethod
    def from_grammar(cls, grammar_base):  # Grammar -> Grammar
        pass

    @classmethod
    def _load_from_txt_(cls, path):
        productions = []
        with open(path, 'r') as f:
            for line in f:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        cfg = CFG.from_text('\n'.join(productions))

        return [
            cfg.variables,
            cfg.terminals,
            cfg.start_symbol,
            cfg.productions
        ]

    @classmethod
    @abstractmethod
    def load_from_txt(self, path):
        _1, _2, _3, _4 = self._load_from_txt_(path)
        return Grammar(_1, _2, _3, _4)


class CNFGrammar(Grammar):

    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[Production] = None):
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

    @classmethod
    def load_from_txt(self, path):
        _1, _2, _3, _4 = self._load_from_txt_(path)
        return CNFGrammar(_1, _2, _3, _4)

    @classmethod
    def from_grammar(cls, grammar_base):
        return CNFGrammar(
            grammar_base.variables,
            grammar_base.terminals,
            grammar_base.start_symbol,
            grammar_base.productions
        )


class BaseGrammar(Grammar):

    @classmethod
    def load_from_txt(self, path):
        _1, _2, _3, _4 = self._load_from_txt_(path)
        return BaseGrammar(_1, _2, _3, _4)

    @classmethod
    def from_grammar(cls, grammar_base):
        return BaseGrammar(
            grammar_base.variables,
            grammar_base.terminals,
            grammar_base.start_symbol,
            grammar_base.productions
        )