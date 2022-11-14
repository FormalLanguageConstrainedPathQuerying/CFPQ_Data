import pytest

import cfpq_data

cfg_1 = cfpq_data.nested_parentheses_grammar([("a", "b"), ("c", "d")])
expected_cfg_1 = cfpq_data.cfg_from_text("S -> epsilon | a S b | c S d")

cfg_2 = cfpq_data.nested_parentheses_grammar([("a", "b"), ("c", "d")], eps=False)
expected_cfg_2 = cfpq_data.cfg_from_text("S -> a b | c d | a S b | c S d")

foaf = cfpq_data.download("foaf")
cfg_foaf = cfpq_data.nested_parentheses_grammar_from_graph(
    cfpq_data.graph_from_csv(foaf), n_types=2
)
expected_cfg_foaf = cfpq_data.cfg_from_text(
    "S -> epsilon | type S type_r | label S label_r"
)

core = cfpq_data.download("core")
cfg_core = cfpq_data.nested_parentheses_grammar_from_graph(
    cfpq_data.graph_from_csv(core), n_types=1, eps=True
)
expected_cfg_core = cfpq_data.cfg_from_text("S -> type type_r | type S type_r")


@pytest.mark.parametrize(
    "grammar,expected_grammar", [(cfg_1, expected_cfg_1), (cfg_2, expected_cfg_2)]
)
def test_nested_parentheses_grammar(grammar, expected_grammar):
    for word in expected_grammar.get_words(4):
        assert grammar.contains(word)


@pytest.mark.parametrize(
    "grammar,expected_grammar",
    [(cfg_foaf, expected_cfg_foaf), (cfg_core, expected_cfg_core)],
)
def test_nested_parentheses_grammar_from_graph(grammar, expected_grammar):
    for word in expected_grammar.get_words(4):
        assert grammar.contains(word)
