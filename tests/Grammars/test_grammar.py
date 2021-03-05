from cfpq_data import Grammar, CNFGrammar
from pyformlang.cfg import *


def test_load_grammar(grammar_name):
    assert Grammar.load_from_txt(grammar_name)


def test_load_cnfgrammar(grammar_name):
    assert CNFGrammar.load_from_txt(grammar_name)


def test_grammar_from_grammar(grammar_name):
    cfg = Grammar.load_from_txt(grammar_name)
    assert CNFGrammar.from_grammar(cfg)


def test_grammar_from_cnfgrammar(grammar_name):
    cfg = CNFGrammar.load_from_txt(grammar_name)
    assert Grammar.from_grammar(cfg)


def test_cnf(grammar_name):
    cfg = Grammar.load_from_txt(grammar_name)
    cfg = CNFGrammar.from_grammar(cfg)
    cfg = CFG(
        variables=cfg.variables,
        terminals=cfg.terminals,
        start_symbol=cfg.start_symbol,
        productions=cfg.productions
    )
    epsilon_production = Production(cfg.start_symbol, [])
    if epsilon_production in cfg.productions:
        cfg.productions.remove(Production(cfg.start_symbol, []))
    assert cfg.is_normal_form()


def test_dump_grammar(grammar_name):
    cfg = Grammar.load_from_txt(grammar_name)
    assert cfg.dump_to_txt('tmp1.txt')


def test_dump_cnfgrammar(grammar_name):
    cfg = CNFGrammar.load_from_txt(grammar_name)
    assert cfg.dump_to_txt('tmp2.txt')