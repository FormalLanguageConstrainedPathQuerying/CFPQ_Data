import pytest
import cfpq_data


cfg_1 = cfpq_data.cfg_from_txt("S -> a S b | a b")
rsm_1 = cfpq_data.rsm_from_cfg(cfg=cfg_1)

cfg_2 = cfpq_data.cfg_from_txt("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")
rsm_2 = cfpq_data.rsm_from_cfg(cfg=cfg_2)


@pytest.mark.parametrize("grammar_1, grammar_2", [(rsm_1, rsm_2)])
def test_cfg_from_cnf(grammar_1, grammar_2):
    assert grammar_1.contains(["a", "b"]) and grammar_2.contains(["sco_r", "sco"])