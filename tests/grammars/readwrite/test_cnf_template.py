import networkx as nx
import pytest

from cfpq_data.grammars.readwrite.cnf_template import (
    cnf_template_from_cnf,
    cnf_template_from_text,
    cnf_template_to_cnf,
    cnf_template_to_text,
    materialize,
    materialize_grammar,
)

AVRORA_TEMPLATE = (
    "PT\tPTh\talloc\n"
    "PTh\tassign\tPTh\n"
    "FT\talloc_r\tFTh\n"
    "FTh\tassign_r\tFTh\n"
    "Al\tPT\tFT\n"
    "PT\talloc\n"
    "FT\talloc_r\n"
    "PTh\tassign\n"
    "FTh\tassign_r\n"
    "PTh\tload\tAl_st_PTh\n"
    "FTh\tstore_r\tAl_ld_r_FTh\n"
    "Al_st_PTh\tAl\tst_PTh\n"
    "Al_ld_r_FTh\tAl\tld_r_FTh\n"
    "st_PTh\tstore\tPTh\n"
    "ld_r_FTh\tload_r\tFTh\n"
    "PTh\tload\tAl_store\n"
    "Al_store\tAl\tstore\n"
    "FTh\tstore_r\tAl_load_r\n"
    "Al_load_r\tAl\tload_r\n"
    "\n"
    "Count:\n"
    "PT\n"
)


def _java_graph(fields):
    g = nx.MultiDiGraph()
    edges = [(0, 1, {"label": "alloc"}), (1, 2, {"label": "assign"})]
    for k in fields:
        edges += [
            (0, 1, {"label": f"load_{k}"}),
            (1, 2, {"label": f"store_{k}"}),
        ]
    g.add_edges_from(edges)
    return g


def test_cnf_template_from_text():
    cfg = cnf_template_from_text(AVRORA_TEMPLATE)

    assert cfg.start_symbol.value == "PT"
    assert len(cfg.productions) == 19
    assert {v.value for v in cfg.variables} == {
        "PT",
        "PTh",
        "FT",
        "FTh",
        "Al",
        "Al_st_PTh",
        "Al_ld_r_FTh",
        "st_PTh",
        "ld_r_FTh",
        "Al_store",
        "Al_load_r",
    }
    assert {t.value for t in cfg.terminals} == {
        "alloc",
        "assign",
        "alloc_r",
        "assign_r",
        "load",
        "store",
        "load_r",
        "store_r",
    }


def test_cnf_template_to_text_round_trip():
    cfg = cnf_template_from_text(AVRORA_TEMPLATE)

    text = cnf_template_to_text(cfg)
    assert text.endswith("\n\nCount:\nPT")

    again = cnf_template_from_text(text)
    assert {
        (p.head.value, tuple(s.value for s in p.body)) for p in cfg.productions
    } == {(p.head.value, tuple(s.value for s in p.body)) for p in again.productions}


def test_cnf_template_file_round_trip(tmp_path):
    cfg = cnf_template_from_text(AVRORA_TEMPLATE)
    path = cnf_template_to_cnf(cfg, tmp_path / "g.cnf")

    assert cnf_template_from_cnf(path).start_symbol.value == "PT"


def test_materialize_bare_style():
    cfg = materialize(cnf_template_from_text(AVRORA_TEMPLATE), _java_graph(["0", "1"]))

    assert {t.value for t in cfg.terminals} == {
        "alloc",
        "assign",
        "alloc_r",
        "assign_r",
        "load_0",
        "load_1",
        "load_0_r",
        "load_1_r",
        "store_0",
        "store_1",
        "store_0_r",
        "store_1_r",
    }


def test_materialize_i_style():
    template = (
        "PT\tPTh\talloc\n"
        "PTh\tassign\n"
        "PTh\tload_i\tAl_st_PTh_i\n"
        "Al_st_PTh_i\tAl\tst_PTh_i\n"
        "st_PTh_i\tstore_i\tPTh\n"
        "FTh\tload_r_i\n"
        "Al\tPT\n"
        "\n"
        "Count:\n"
        "PT\n"
    )
    g = nx.MultiDiGraph()
    g.add_edges_from(
        [
            (0, 1, {"label": "alloc"}),
            (0, 1, {"label": "load_5"}),
            (1, 2, {"label": "store_7"}),
            (1, 0, {"label": "load_5_r"}),
            (2, 3, {"label": "assign"}),
        ]
    )

    cfg = materialize(cnf_template_from_text(template), g)

    # load_r_i resolves to the derived reversed label load_5_r.
    assert "load_5_r" in {t.value for t in cfg.terminals}
    # The families have different indices (5 vs 7): the union is expanded and
    # the productions referencing the absent labels are inert.
    assert {"load_5", "load_7", "store_5", "store_7"} <= {
        t.value for t in cfg.terminals
    }


def test_materialize_inert_symbols():
    template = (
        "S\tsubClassOf\tN1\n" "N1\tS\ttype\n" "S\ttype_r\ttype\n" "\n" "Count:\n" "S\n"
    )
    g = nx.MultiDiGraph()
    g.add_edge(0, 1, label="type")

    cfg = materialize(cnf_template_from_text(template), g)

    # subClassOf has no matching label: it stays an inert terminal; type_r
    # resolves to the derived reversed label.
    assert {t.value for t in cfg.terminals} == {"subClassOf", "type", "type_r"}


def test_materialize_rejects_indexed_start_symbol():
    template = "load_i\tPTh\n" "PTh\talloc\n" "\n" "Count:\n" "load_i\n"

    with pytest.raises(ValueError, match="must not be indexed"):
        materialize(cnf_template_from_text(template), _java_graph(["0"]))


FSJPT_TEMPLATE = (
    "PT\tPTh\talloc\n"
    "PTh\tassign\tPTh\n"
    "FT\talloc_r\tFTh\n"
    "FTh\tassign_r\tFTh\n"
    "Al\tPT\tFT\n"
    "PT\talloc\n"
    "FT\talloc_r\n"
    "PTh\tassign\n"
    "FTh\tassign_r\n"
    "PTh\tload_i\tAl_st_PTh_i\n"
    "FTh\tstore_r_i\tAl_ld_r_FTh_i\n"
    "Al_st_PTh_i\tAl\tst_PTh_i\n"
    "Al_ld_r_FTh_i\tAl\tld_r_FTh_i\n"
    "st_PTh_i\tstore_i\tPTh\n"
    "ld_r_FTh_i\tload_r_i\tFTh\n"
    "PTh\tload_i\tAl_store_i\n"
    "Al_store_i\tAl\tstore_i\n"
    "FTh\tstore_r_i\tAl_load_r_i\n"
    "Al_load_r_i\tAl\tload_r_i\n"
    "\n"
    "Count:\n"
    "PT\n"
)

CSCVF_TEMPLATE = (
    "A\n"
    "A\tA\tB\n"
    "A\tA\ta\n"
    "B\tcall_i\tAR_i\n"
    "AR_i\tA\tret_i\n"
    "\n"
    "Count:\n"
    "A\n"
)

FSCA_TEMPLATE = (
    "M\tDV\td\n"
    "DV\tdbar\tV\n"
    "V\tA_r\tV\n"
    "V\tV\tA\n"
    "V\tFV_i\tf_i\n"
    "V\tM\n"
    "V\n"
    "FV_i\tfbar_i\tV\n"
    "A\ta\tM\n"
    "A\ta\n"
    "A\n"
    "A_r\tM\tabar\n"
    "A_r\tabar\n"
    "A_r\n"
    "\n"
    "Count:\n"
    "V\n"
)


def test_materialize_fsjpt_indexed():
    g = _java_graph(["0", "1"])
    cfg = materialize(cnf_template_from_text(FSJPT_TEMPLATE), g)

    assert cfg.start_symbol.value == "PT"
    terminals = {t.value for t in cfg.terminals}
    assert {"load_0", "load_1", "store_0", "store_1"} <= terminals
    assert {"alloc", "assign", "alloc_r", "assign_r"} <= terminals
    # Indexed nonterminals are expanded per index
    variables = {v.value for v in cfg.variables}
    assert {"Al_st_PTh_0", "Al_st_PTh_1", "st_PTh_0", "st_PTh_1"} <= variables


def test_materialize_cscvf_indexed():
    g = nx.MultiDiGraph()
    g.add_edges_from(
        [
            (0, 1, {"label": "call_0"}),
            (1, 2, {"label": "ret_0"}),
            (0, 3, {"label": "call_1"}),
            (3, 4, {"label": "ret_1"}),
            (0, 5, {"label": "a"}),
        ]
    )
    cfg = materialize(cnf_template_from_text(CSCVF_TEMPLATE), g)

    assert cfg.start_symbol.value == "A"
    terminals = {t.value for t in cfg.terminals}
    assert {"call_0", "call_1", "ret_0", "ret_1", "a"} <= terminals
    variables = {v.value for v in cfg.variables}
    assert {"AR_0", "AR_1"} <= variables


def test_materialize_fsca_indexed():
    g = nx.MultiDiGraph()
    g.add_edges_from(
        [
            (0, 1, {"label": "f_0"}),
            (1, 2, {"label": "fbar_0"}),
            (0, 3, {"label": "f_1"}),
            (3, 4, {"label": "fbar_1"}),
            (0, 5, {"label": "a"}),
            (5, 6, {"label": "d"}),
        ]
    )
    cfg = materialize(cnf_template_from_text(FSCA_TEMPLATE), g)

    assert cfg.start_symbol.value == "V"
    terminals = {t.value for t in cfg.terminals}
    assert {"f_0", "f_1", "fbar_0", "fbar_1", "a", "d"} <= terminals
    variables = {v.value for v in cfg.variables}
    assert {"FV_0", "FV_1"} <= variables


def test_materialize_grammar_convenience(tmp_path):
    cnf_path = tmp_path / "test.cnf"
    cnf_path.write_text(FSJPT_TEMPLATE)
    g = _java_graph(["2"])

    cfg = materialize_grammar(cnf_path, g)

    assert cfg.start_symbol.value == "PT"
    terminals = {t.value for t in cfg.terminals}
    assert "load_2" in terminals
    assert "store_2" in terminals
