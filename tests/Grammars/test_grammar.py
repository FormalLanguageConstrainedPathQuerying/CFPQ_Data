from cfpq_data import Grammar, CNFGrammar
from pyformlang.cfg import *

def test_load_Grammar(grammar_name):
    assert Grammar.load_from_txt(grammar_name)

def test_load_CNFGrammar(grammar_name):
    assert CNFGrammar.load_from_txt(grammar_name)

def test_grammar_from_Grammar(grammar_name):
    cfg = Grammar.load_from_txt(grammar_name)
    assert CNFGrammar.from_grammar(cfg)

def test_grammar_from_CNFGrammar(grammar_name):
    cfg = CNFGrammar.load_from_txt(grammar_name)
    assert Grammar.from_grammar(cfg)

def test_CNF(grammar_name):
    cfg = Grammar.load_from_txt(grammar_name)
    cfg = CNFGrammar.from_grammar(cfg)
    assert CFG.is_normal_form(cfg)

def test_dump_Grammar(grammar_name):
    cfg = Grammar.load_from_txt(grammar_name)
    assert cfg.dump_to_txt('tmp1.txt')

def test_dump_CNFGrammar(grammar_name):
    cfg = CNFGrammar.load_from_txt(grammar_name)
    assert cfg.dump_to_txt('tmp2.txt')