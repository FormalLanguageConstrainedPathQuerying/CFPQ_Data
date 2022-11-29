import pytest

import cfpq_data

cfg_1 = cfpq_data.c_alias_grammar()
expected_cfg_1 = cfpq_data.cfg_from_text(
    "S -> d_r V d\nV -> V1 V2 V3\nV1 -> \nV1 -> V2 a_r V1\nV2 -> \nV2 -> S\nV3 -> \nV3 -> a V2 V3"
)

cfg_2 = cfpq_data.c_alias_grammar(
    assigment_labels=("assign", "assign_r"), dereference_labels=("deref", "deref_r")
)
expected_cfg_2 = cfpq_data.cfg_from_text(
    "S -> deref_r V deref\nV -> V1 V2 V3\nV1 -> \nV1 -> V2 assign_r V1\nV2 -> \nV2 -> S\nV3 -> \nV3 -> assign V2 V3"
)


@pytest.mark.parametrize(
    "grammar,expected_grammar", [(cfg_1, expected_cfg_1), (cfg_2, expected_cfg_2)]
)
def test_c_alias_grammar(grammar, expected_grammar):
    for word in expected_grammar.get_words(4):
        assert grammar.contains(word)
