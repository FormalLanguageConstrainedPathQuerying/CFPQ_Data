import pytest
import cfpq_data

cfg_1 = cfpq_data.cfg_from_txt("S -> a S b S\nS -> a b\n")
exp_cfg_1 = cfpq_data.cfg_from_txt("S -> b S c S\nS -> b c\n")

cfg_2 = cfpq_data.cfg_from_txt("S -> a b c d\n")
exp_cfg_2 = cfpq_data.cfg_from_txt("S -> b c c d\n")


@pytest.mark.parametrize("cfg, exp_cfg", [(cfg_1, exp_cfg_1), (cfg_2, exp_cfg_2)])
def test_change_cfg_terminals(cfg, exp_cfg):
    act_cfg = cfpq_data.change_cfg_terminals(cfg, {"a": "b", "b": "c"})
    assert set(exp_cfg.to_text().split("\n")) == set(act_cfg.to_text().split("\n"))
