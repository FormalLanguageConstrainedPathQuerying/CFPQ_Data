from abc import abstractmethod, ABC
from pyformlang.cfg import *
from pyformlang.regular_expression import Regex
from cfpq_data.src.grammars.grammar import CNFGrammar, BaseGrammar, RSA


class GrammarCreator(ABC):

    @abstractmethod
    def create(self):
        pass


class TXTBaseGrammarCreator(GrammarCreator):

    def __init__(self, path: str, start_symbol: Variable = Variable('S')):
        self.path = path
        self.start_symbol = start_symbol

    def create(self) -> BaseGrammar:
        """
        Load BaseGrammar from txt file

        :return: BaseGrammar object
        """
        path = self.path
        start_symbol = self.start_symbol

        with open(path, 'r') as f:
            cfg = CFG.from_text(f.read(), start_symbol)

        return BaseGrammar(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
        )


class TXTCNFGrammarCreator(GrammarCreator):

    def __init__(self, path: str, start_symbol: Variable = Variable('S')):
        self.path = path
        self.start_symbol = start_symbol

    def create(self) -> CNFGrammar:
        """
        Load CNFGrammar from txt file

        :return: CNFGrammar object
        """
        path = self.path
        start_symbol = self.start_symbol

        with open(path, 'r') as f:
            cfg = CFG.from_text(f.read(), start_symbol)

        return CNFGrammar(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
        )


class TXTRSAGrammarCreator(GrammarCreator):

    def __init__(self, path: str, start_symbol: Variable = Variable('S')):
        self.path = path
        self.start_symbol = start_symbol

    def create(self) -> RSA:
        """
        Load RSAGrammar from txt file with Grammar

        :return: RSA object
        """
        path = self.path
        start_symbol = self.start_symbol

        rsa = RSA()
        rsa.start_symbol = start_symbol
        productions = []

        with open(path, 'r') as f:
            for line in f:
                production = line.replace(' -> ', ' ').split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        text = '\n'.join(productions)

        changing = True
        while changing:
            changing = False
            productions = text.split('\n')
            eps_head, eps_body = None, None
            for p in productions:
                head, body = p.split(' -> ')
                if body == '':
                    eps_head = head
                    eps_body = body
            new_productions = list()
            for p in productions:
                head, body = p.split(' -> ')
                if head == eps_head and body == eps_body:
                    continue
                new_body = list()
                for b in body.split():
                    if b == eps_head:
                        new_body.append(f'({eps_head}|$)')
                        changing = True
                    else:
                        new_body.append(b)
                new_body = " ".join(new_body)
                if head == eps_head:
                    new_body = f'({new_body})|$'
                new_productions.append(f'{head} -> {new_body}')
            text = '\n'.join(new_productions)

        changing = True
        while changing:
            changing = False
            productions = text.split('\n')
            tmp = dict()
            for p in productions:
                head, body = p.split(' -> ')
                tmp[head] = tmp.get(head, list()) + [body]
            new_productions = list()
            for head in tmp:
                if len(tmp[head]) > 1:
                    new_body = '|'.join(
                        map(
                            lambda x: f'({x})',
                            tmp[head]
                        )
                    )
                    new_productions.append(f'{head} -> {new_body}')
                    changing = True
                else:
                    new_productions.append(f'{head} -> {tmp[head][0]}')
            text = '\n'.join(new_productions)

        productions = text.split('\n')

        for p in productions:
            head, body = p.split(' -> ')
            body = body.replace('epsilon', '$').replace('eps', '$')
            if body == '':
                body = '$'
            rsa.boxes[head] = rsa.boxes.get(head, list()) + [
                Regex(body) \
                    .to_epsilon_nfa() \
                    .to_deterministic() \
                    .minimize()
            ]
        return rsa
