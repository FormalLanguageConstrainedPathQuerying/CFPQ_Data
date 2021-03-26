from abc import abstractmethod, ABC
from pyformlang.cfg import *
from cfpq_data.src.grammars.grammar import CNFGrammar, BaseGrammar


class GrammarSerializer(ABC):

    @abstractmethod
    def dump(self):
        pass


class BaseGrammarToTXT(GrammarSerializer):

    def __init__(self, grammar_obj: BaseGrammar, path: str):
        self.path = path
        self.grammar = grammar_obj

    def dump(self) -> str:
        """
        Saving BaseGrammar to txt file

        :return: path
        """
        path = self.path
        source = self.grammar

        cfg = CFG(
            variables=source.variables,
            terminals=source.terminals,
            start_symbol=source.start_symbol,
            productions=source.productions
        )
        with open(path, 'w') as f:
            f.write(cfg.to_text())
        return path


class CNFGrammarToTXT(GrammarSerializer):

    def __init__(self, grammar_obj: CNFGrammar, path: str):
        self.path = path
        self.grammar = grammar_obj

    def dump(self) -> str:
        """
        Saving CNFGrammar to txt file

        :return: path
        """
        path = self.path
        source = self.grammar

        cfg = CFG(
            variables=source.variables,
            terminals=source.terminals,
            start_symbol=source.start_symbol,
            productions=source.productions
        )
        with open(path, 'w') as f:
            f.write(cfg.to_text())
        return path


class RSAToTXT(GrammarSerializer):

    def dump(self):
        pass
