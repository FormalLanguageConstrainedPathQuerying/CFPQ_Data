from __future__ import annotations

from typing import AbstractSet, Iterable, Optional
from abc import abstractmethod, ABC

from pyformlang.cfg import *
from pyformlang.regular_expression import Regex


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
    def from_grammar(cls, source: Grammar) -> Grammar:
        """
        Converting grammars into different forms (for example Grammar into CNFGrammar)

        :param source: Grammar or CNFGrammar object
        :return: CNFGrammar or Grammar object
        """
        return cls(
            variables=source.variables,
            terminals=source.terminals,
            start_symbol=source.start_symbol,
            productions=source.productions
        )

    @classmethod
    def load_from_txt(cls, path: str, start_symbol: Variable = Variable("S")) -> Grammar:
        """
        Load grammar from txt file

        :param path: path to txt file with grammar
        :param start_symbol: :class:`~pyformlang.cfg.Variable`, optional
        The start symbol
        :return: Grammar or CNFGrammar object
        """
        with open(path, 'r') as f:
            cfg = CFG.from_text(f.read(), start_symbol)

        return cls(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
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

    def from_grammar(cls, source: Grammar) -> Grammar:
        """
        Converting from CNFGrammar or Grammar to RSA

        :param source: CNFGrammar or Grammar object
        :return: RSA object
        """

        rsm = RSA()
        text = str()
        rsm.start_symbol = source.start_symbol
        source.dump_to_txt('tmp.txt')
        with open('tmp.txt', 'r') as f:
            productions = f.readlines()

        changing = True
        while changing:
            changing = False
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
            rsm.boxes[head] = rsm.boxes.get(head, list()) + [
                Regex(body) \
                    .to_epsilon_nfa() \
                    .to_deterministic() \
                    .minimize()
            ]

        return rsm
