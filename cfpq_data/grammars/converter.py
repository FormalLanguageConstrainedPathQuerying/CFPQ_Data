from abc import abstractmethod, ABC
from pyformlang.cfg import *
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

    def __init__(self, grammar_obj: RSA):
        self.grammar = grammar_obj

    def convert(self) -> CNFGrammar:
        variables = set()
        terminals = set()
        grammar = self.grammar
        start_symbol = grammar.start_symbol
        productions = set()

        cnt = 1
        for x in grammar.boxes:
            head = Variable(x)
            variables.add(head)
            for box in grammar.boxes[x]:
                name = {box.start_state: head}
                for s in box.states:
                    if s not in name:
                        name[s] = Variable(f'S{cnt}')
                        cnt += 1
                        variables.add(name[s])
                    if s in box.final_states:
                        productions.add(Production(name[s], []))
                for v in box._transition_function._transitions:
                    for label in box._transition_function._transitions[v]:
                        to = box._transition_function._transitions[v][label]

                        if label.value == label.value.lower():
                            terminals.add(Terminal(label.value))
                            productions.add(Production(name[v], [Terminal(label.value), name[to]]))
                        else:
                            productions.add(Production(name[v], [Variable(label.value), name[to]]))

        return CNFGrammar(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )


class RSAToBaseGrammarConverter(GrammarConverter):

    def __init__(self, grammar_obj: RSA):
        self.grammar = grammar_obj

    def convert(self) -> BaseGrammar:
        variables = set()
        terminals = set()
        grammar = self.grammar
        start_symbol = grammar.start_symbol
        productions = set()

        cnt = 1
        for x in grammar.boxes:
            head = Variable(x)
            variables.add(head)
            for box in grammar.boxes[x]:
                name = {box.start_state: head}
                for s in box.states:
                    if s not in name:
                        name[s] = Variable(f'S{cnt}')
                        cnt += 1
                        variables.add(name[s])
                    if s in box.final_states:
                        productions.add(Production(name[s], []))
                for v in box._transition_function._transitions:
                    for label in box._transition_function._transitions[v]:
                        to = box._transition_function._transitions[v][label]

                        if label.value == label.value.lower():
                            terminals.add(Terminal(label.value))
                            productions.add(Production(name[v], [Terminal(label.value), name[to]]))
                        else:
                            productions.add(Production(name[v], [Variable(label.value), name[to]]))

        return BaseGrammar(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )
