from abc import abstractmethod, ABC
from cfpq_data.src.grammars.grammar import CNFGrammar, BaseGrammar, RSA
from cfpq_data.src.grammars.creator import TXTRSAGrammarCreator
from cfpq_data.src.grammars.serializer import BaseGrammarToTXT, CNFGrammarToTXT


class GrammarConverter(ABC):

    @abstractmethod
    def convert(self):
        pass


class BaseGrammarToCNFGrammarConverter(GrammarConverter):

    def __init__(self, grammar_obj: BaseGrammar):
        self.grammar = grammar_obj

    def convert(self) -> CNFGrammar:
        """
        Converting BaseGrammar into CNF

        :return: CNFGrammar object
        """
        source = self.grammar
        return CNFGrammar(
            variables=source.variables,
            terminals=source.terminals,
            start_symbol=source.start_symbol,
            productions=source.productions
        )


class CNFGrammarToBaseGrammarConverter(GrammarConverter):

    def __init__(self, grammar_obj: CNFGrammar):
        self.grammar = grammar_obj

    def convert(self) -> BaseGrammar:
        """
        Converting CNF into BaseGrammar

        :return: BaseGrammar object
        """
        source = self.grammar
        return BaseGrammar(
            variables=source.variables,
            terminals=source.terminals,
            start_symbol=source.start_symbol,
            productions=source.productions
        )


class BaseGrammarToRSAConverter(GrammarConverter):

    def __init__(self, grammar_obj: BaseGrammar):
        self.grammar = grammar_obj

    def convert(self) -> RSA:
        """
        Converting BaseGrammar into RSA

        :return: RSA object
        """
        grammar_obj = self.grammar
        path = BaseGrammarToTXT(grammar_obj=grammar_obj, path='tmp.txt').dump()
        g = TXTRSAGrammarCreator(path=path, start_symbol=grammar_obj.start_symbol).create()
        return g


class CNFGrammarToRSAConverter(GrammarConverter):

    def __init__(self, grammar_obj: CNFGrammar):
        self.grammar = grammar_obj

    def convert(self) -> RSA:
        """
        Converting CNF into RSA

        :return: RSA object
        """
        grammar_obj = self.grammar
        path = CNFGrammarToTXT(grammar_obj=grammar_obj, path='tmp.txt').dump()
        g = TXTRSAGrammarCreator(path=path, start_symbol=grammar_obj.start_symbol).create()
        return g


class RSAToCNFGrammarConverter(GrammarConverter):

    def convert(self):
        pass


class RSAToBaseGrammarConverter(GrammarConverter):

    def convert(self):
        pass
