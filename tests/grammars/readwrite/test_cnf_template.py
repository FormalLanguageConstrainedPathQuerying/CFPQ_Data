import networkx as nx
import pytest

from cfpq_data.grammars.readwrite.cnf_template import (
    cnf_template_from_cnf,
    cnf_template_from_text,
    cnf_template_to_cnf,
    cnf_template_to_text,
    materialize,
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
            (1, 0, {"label": "load_r_5"}),
            (2, 3, {"label": "assign"}),
        ]
    )

    cfg = materialize(cnf_template_from_text(template), g)

    # load_r_i resolves to the stored reversed label load_r_5.
    assert "load_r_5" in {t.value for t in cfg.terminals}
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
