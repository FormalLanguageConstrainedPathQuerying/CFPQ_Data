import pytest

import flpq_data

cfg_1 = flpq_data.java_points_to_grammar(["0"])
expected_cfg_1 = flpq_data.cfg_from_text(
    """S -> PTh alloc
    PTh -> epsilon
    PTh -> assign PTh
    PTh -> load_0 Al store_0 PTh
    FT -> alloc_r FTh
    FTh -> epsilon
    FTh -> assign_r FTh
    FTh -> store_0_r Al load_0_r FTh
    Al -> S FT"""
)

cfg_2 = flpq_data.java_points_to_grammar(["0", "1"])
expected_cfg_2 = flpq_data.cfg_from_text(
    """S -> PTh alloc
    PTh -> epsilon
    PTh -> assign PTh
    PTh -> load_0 Al store_0 PTh
    PTh -> load_1 Al store_1 PTh
    FT -> alloc_r FTh
    FTh -> epsilon
    FTh -> assign_r FTh
    FTh -> store_0_r Al load_0_r FTh
    FTh -> store_1_r Al load_1_r FTh
    Al -> S FT"""
)


avrora = flpq_data.download_graph("avrora")
cfg_avrora = flpq_data.java_points_to_grammar_from_graph(
    flpq_data.graph_from_mtx_dir(avrora / "graph")
)
expected_productions_count_avrora = 1723

eclipse = flpq_data.download_graph("eclipse")
cfg_eclipse = flpq_data.java_points_to_grammar_from_graph(
    flpq_data.graph_from_mtx_dir(eclipse / "graph")
)
expected_productions_count_eclipse = 1525


@pytest.mark.parametrize(
    "grammar,expected_grammar", [(cfg_1, expected_cfg_1), (cfg_2, expected_cfg_2)]
)
def test_java_points_to_grammar(grammar, expected_grammar):
    for word in expected_grammar.get_words(4):
        assert grammar.contains(word)


@pytest.mark.parametrize(
    "grammar,expected_productions_count",
    [
        (cfg_avrora, expected_productions_count_avrora),
        (cfg_eclipse, expected_productions_count_eclipse),
    ],
)
def test_java_points_to_grammar_from_graph(grammar, expected_productions_count):
    assert len(grammar.productions) == expected_productions_count
