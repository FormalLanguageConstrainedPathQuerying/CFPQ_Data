import pytest
import cfpq_data

rsm_1 = cfpq_data.rsm_from_txt("S -> a b\n")
exp_rsm_1 = cfpq_data.rsm_from_txt("S -> b c\n")

rsm_2 = cfpq_data.rsm_from_txt("S -> b a\n")
exp_rsm_2 = cfpq_data.rsm_from_txt("S -> c b\n")


@pytest.mark.parametrize("rsm, exp_rsm", [(rsm_1, exp_rsm_1), (rsm_2, exp_rsm_2)])
def test_change_rsm_terminals(rsm, exp_rsm):
    act_rsm = cfpq_data.change_rsm_terminals(rsm, {"a": "b", "b": "c"})
    assert set(exp_rsm.to_text().split("\n")) == set(act_rsm.to_text().split("\n"))
