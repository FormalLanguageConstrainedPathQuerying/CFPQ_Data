import pytest

import cfpq_data

cfg_1 = cfpq_data.dyck_grammar([("a", "b"), ("c", "d")])
expected_cfg_1 = cfpq_data.cfg_from_text("S -> epsilon | a S b S | c S d S")

cfg_2 = cfpq_data.dyck_grammar([("a", "b"), ("c", "d")], eps=False)
expected_cfg_2 = cfpq_data.cfg_from_text("S -> a b | c d | a S b S | c S d S")


@pytest.mark.parametrize(
    "grammar,expected_grammar", [(cfg_1, expected_cfg_1), (cfg_2, expected_cfg_2)]
)
def test_dyck_grammar(grammar, expected_grammar):
    for word in expected_grammar.get_words(4):
        assert grammar.contains(word)
