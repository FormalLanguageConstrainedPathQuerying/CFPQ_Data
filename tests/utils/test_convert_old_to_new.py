import pathlib
import random
from collections import Counter

import pytest
from pyformlang.cfg import CFG, Production, Terminal, Variable

from convert_old_to_new import (
    MTX_BANNER,
    MTX_TYPE,
    GraphStats,
    JAVA_START,
    JAVA_TEMPLATE,
    c_alias_cnf,
    cnf_lite,
    convert_csv_to_graph_dir,
    instantiate_template,
    iter_edges,
    java_points_to_cnf,
    rdf_cnf_grammars,
    scan_csv,
    validate_labels,
    write_cnf,
)


def write_csv(path: pathlib.Path, lines) -> pathlib.Path:
    path.write_text("\r\n".join(lines) + "\r\n")
    return path


def parse_mtx(path: pathlib.Path):
    """Parse an MTX file produced by the converter into (header, entries)."""
    with open(path, "r") as f:
        lines = f.read().splitlines()
    assert lines[0] == MTX_BANNER
    assert lines[1] == MTX_TYPE
    rows, cols, nnz = (int(x) for x in lines[2].split())
    entries = [(int(a), int(b)) for a, b in (line.split() for line in lines[3:])]
    return (rows, cols, nnz), entries


def test_iter_edges_crlf_and_lf(tmp_path):
    crlf = write_csv(tmp_path / "crlf.csv", ["0 1 a", "2 3 b"])
    lf = tmp_path / "lf.csv"
    lf.write_text("0 1 a\n2 3 b\n")

    assert list(iter_edges(crlf)) == [(0, 1, "a"), (2, 3, "b")]
    assert list(iter_edges(lf)) == list(iter_edges(crlf))


def test_iter_edges_skips_blank_lines(tmp_path):
    csv = write_csv(tmp_path / "g.csv", ["0 1 a", "", "2 3 b"])
    assert list(iter_edges(csv)) == [(0, 1, "a"), (2, 3, "b")]


@pytest.mark.parametrize(
    "line",
    [
        "0 1",  # too few fields
        "0 1 a b",  # too many fields
        "x 1 a",  # non-integer from
        "0 y a",  # non-integer to
    ],
)
def test_iter_edges_malformed(tmp_path, line):
    csv = write_csv(tmp_path / "g.csv", [line])
    with pytest.raises(ValueError):
        list(iter_edges(csv))


def test_scan_csv_stats(tmp_path):
    csv = write_csv(
        tmp_path / "g.csv",
        ["0 1 a", "1 2 a", "2 0 b", "5 5 a"],
    )
    stats = scan_csv(csv)
    assert isinstance(stats, GraphStats)
    assert stats.num_nodes == 4  # {0, 1, 2, 5}
    assert stats.max_node_id == 5
    assert stats.total_edges == 4
    assert stats.edges_per_label == {"a": 3, "b": 1}


def test_convert_golden_readme_example(tmp_path):
    # The example graph from the new-format README:
    # (0) --[a]-> (1); (2) --[a]-> (1); (0) --[b]-> (2); (2) --[b]-> (3)
    csv = write_csv(
        tmp_path / "g.csv",
        ["0 1 a", "2 1 a", "0 2 b", "2 3 b"],
    )
    graph_dir = tmp_path / "graph"
    stats = convert_csv_to_graph_dir(csv, graph_dir)

    assert sorted(p.name for p in graph_dir.iterdir()) == ["a.mtx", "b.mtx"]
    assert stats.total_edges == 4
    assert stats.edges_per_label == {"a": 2, "b": 2}

    (rows, cols, nnz), entries = parse_mtx(graph_dir / "a.mtx")
    assert (rows, cols, nnz) == (4, 4, 2)
    assert entries == [(0, 1), (2, 1)]

    (rows, cols, nnz), entries = parse_mtx(graph_dir / "b.mtx")
    assert (rows, cols, nnz) == (4, 4, 2)
    assert entries == [(0, 2), (2, 3)]


def test_convert_roundtrip_property(tmp_path):
    rng = random.Random(42)
    edges = [
        (rng.randrange(50), rng.randrange(50), rng.choice(["a", "b_r", "c_x"]))
        for _ in range(2000)
    ]
    csv = tmp_path / "g.csv"
    csv.write_text("\n".join(f"{u} {v} {l}" for u, v, l in edges) + "\n")

    graph_dir = tmp_path / "graph"
    stats = convert_csv_to_graph_dir(csv, graph_dir)

    assert stats.total_edges == len(edges)
    assert Counter(stats.edges_per_label.values()) == Counter(
        Counter(l for _, _, l in edges).values()
    )

    restored = Counter()
    for label, nnz in stats.edges_per_label.items():
        (rows, cols, header_nnz), entries = parse_mtx(graph_dir / f"{label}.mtx")
        assert header_nnz == len(entries) == nnz
        assert rows == cols == stats.max_node_id + 1
        restored.update((u, v, label) for u, v in entries)

    assert restored == Counter(edges)


def test_convert_sparse_node_ids(tmp_path):
    csv = write_csv(tmp_path / "g.csv", ["0 5 a"])
    graph_dir = tmp_path / "graph"
    stats = convert_csv_to_graph_dir(csv, graph_dir)

    (rows, cols, nnz), entries = parse_mtx(graph_dir / "a.mtx")
    assert (rows, cols, nnz) == (6, 6, 1)
    assert entries == [(0, 5)]
    assert stats.num_nodes == 2


def test_convert_preserves_duplicate_edges(tmp_path):
    csv = write_csv(tmp_path / "g.csv", ["0 1 a", "0 1 a", "1 0 a"])
    graph_dir = tmp_path / "graph"
    convert_csv_to_graph_dir(csv, graph_dir)

    (_, _, nnz), entries = parse_mtx(graph_dir / "a.mtx")
    assert nnz == 3
    assert entries == [(0, 1), (0, 1), (1, 0)]


@pytest.mark.parametrize(
    "label",
    ["", "a/b", "a b", "-a", "a\x00b"],
)
def test_validate_labels_rejects_unsafe(label):
    with pytest.raises(ValueError):
        validate_labels([label])


def test_validate_labels_accepts_dataset_labels():
    validate_labels(
        {
            "a",
            "type_r",
            "subClassOf",
            "load_0",
            "store_857_r",
            "default-namespace",
            "created_by",
        }
    )


# ---------------------------------------------------------------------------
# Grammar generation
# ---------------------------------------------------------------------------

EXPECTED_JAVA_CNf = (
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

# gson/grammar/java_points_to.cnf from the 4.0.0 bucket (byte-identical across
# all seven new-format java archives).
GSON_JAVA_POINTS_TO_CNf = (
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

GSON_RENAME = {
    "load": "load_i",
    "store": "store_i",
    "load_r": "load_r_i",
    "store_r": "store_r_i",
    "Al_st_PTh": "Al_st_PTh_i",
    "st_PTh": "st_PTh_i",
    "Al_store": "Al_store_i",
    "Al_ld_r_FTh": "Al_ld_r_FTh_i",
    "ld_r_FTh": "ld_r_FTh_i",
    "Al_load_r": "Al_load_r_i",
}


def test_java_template_golden(tmp_path):
    path = tmp_path / "java_points_to.cnf"
    write_cnf(*java_points_to_cnf({"load_0", "store_0", "alloc"}), path)
    assert path.read_text() == EXPECTED_JAVA_CNf


def test_java_template_matches_gson_family():
    def renamed(symbol: str) -> str:
        return symbol if symbol not in GSON_RENAME else GSON_RENAME[symbol]

    body = "\n".join(
        "\t".join(renamed(symbol) for symbol in [lhs, *rhs])
        for lhs, rhs in JAVA_TEMPLATE
    )
    assert body + "\n\nCount:\nPT\n" == GSON_JAVA_POINTS_TO_CNf


def test_java_points_to_cnf_requires_load_store_labels():
    with pytest.raises(ValueError):
        java_points_to_cnf({"alloc", "assign"})
    with pytest.raises(ValueError):
        java_points_to_cnf({"load_0", "alloc"})
    with pytest.raises(ValueError):
        java_points_to_cnf({"store_0", "alloc"})


def _cfg_from_instantiated_template(productions, start_symbol):
    lhs_set = {lhs for lhs, _ in productions}
    variables = {Variable(symbol) for symbol in lhs_set}
    terminals = {
        Terminal(symbol)
        for _, rhs in productions
        for symbol in rhs
        if symbol not in lhs_set
    }
    return CFG(
        variables=variables,
        terminals=terminals,
        productions={
            Production(
                Variable(lhs),
                [
                    Variable(symbol) if symbol in lhs_set else Terminal(symbol)
                    for symbol in rhs
                ],
            )
            for lhs, rhs in productions
        },
        start_symbol=Variable(start_symbol),
    )


def _words(cfg, max_length):
    return {
        " ".join(symbol.to_text() for symbol in word)
        for word in cfg.get_words(max_length=max_length)
    }


def test_java_template_language_equals_package_generator():
    from cfpq_data.grammars.generators.java_points_to_grammar import (
        java_points_to_grammar,
    )

    fields = [str(i) for i in range(6)]
    indices = set(range(6))
    index_sets = {
        symbol: indices
        for symbol in (
            "load",
            "store",
            "load_r",
            "store_r",
            "Al_st_PTh",
            "st_PTh",
            "Al_store",
            "Al_ld_r_FTh",
            "ld_r_FTh",
            "Al_load_r",
        )
    }
    mine = _cfg_from_instantiated_template(
        instantiate_template(JAVA_TEMPLATE, index_sets), JAVA_START
    )
    reference = java_points_to_grammar(fields)
    assert _words(mine, 8) == _words(reference, 8)


EXPECTED_C_ALIAS_CNf = (
    "S\td_r\tN1\n"
    "N1\tV\td\n"
    "V\tV1\tN2\n"
    "N2\tV2\tV3\n"
    "V1\n"
    "V1\tV2\tN3\n"
    "N3\ta_r\tV1\n"
    "V2\n"
    "V2\tS\n"
    "V3\n"
    "V3\ta\tN4\n"
    "N4\tV2\tV3\n"
    "\n"
    "Count:\n"
    "S\n"
)


def test_c_alias_cnf_golden(tmp_path):
    path = tmp_path / "c_alias.cnf"
    write_cnf(*c_alias_cnf(), path)
    assert path.read_text() == EXPECTED_C_ALIAS_CNf


EXPECTED_RDF_COMBINED_CNf = (
    "S\tsubClassOf_r\tN1\n"
    "N1\tS\tsubClassOf\n"
    "S\tsubClassOf_r\tsubClassOf\n"
    "S\ttype_r\tN2\n"
    "N2\tS\ttype\n"
    "S\ttype_r\ttype\n"
    "\n"
    "Count:\n"
    "S\n"
)

EXPECTED_RDF_SUBCLASSOF_CNf = (
    "S\tsubClassOf_r\tN1\n"
    "N1\tS\tsubClassOf\n"
    "S\tsubClassOf_r\tsubClassOf\n"
    "\n"
    "Count:\n"
    "S\n"
)

EXPECTED_RDF_TYPE_CNf = (
    "S\ttype_r\tN1\n" "N1\tS\ttype\n" "S\ttype_r\ttype\n" "\n" "Count:\n" "S\n"
)

EXPECTED_RDF_BROADER_TRANSITIVE_CNf = (
    "S\tbroaderTransitive\tN1\n"
    "N1\tS\tbroaderTransitive_r\n"
    "S\tbroaderTransitive\tbroaderTransitive_r\n"
    "\n"
    "Count:\n"
    "S\n"
)


def test_rdf_cnf_grammars(tmp_path):
    grammars = rdf_cnf_grammars({"subClassOf", "type"})
    assert sorted(grammars) == [
        "nested_parentheses_subClassOf.cnf",
        "nested_parentheses_subClassOf_type.cnf",
        "nested_parentheses_type.cnf",
    ]
    expected = {
        "nested_parentheses_subClassOf_type.cnf": EXPECTED_RDF_COMBINED_CNf,
        "nested_parentheses_subClassOf.cnf": EXPECTED_RDF_SUBCLASSOF_CNf,
        "nested_parentheses_type.cnf": EXPECTED_RDF_TYPE_CNf,
    }
    for filename, (productions, start_symbol) in grammars.items():
        path = tmp_path / filename
        write_cnf(productions, start_symbol, path)
        assert path.read_text() == expected[filename]


def test_rdf_broader_transitive_only_when_label_present(tmp_path):
    without = rdf_cnf_grammars({"subClassOf", "type"})
    assert "nested_parentheses_broaderTransitive.cnf" not in without

    with_bt = rdf_cnf_grammars({"subClassOf", "type", "broaderTransitive"})
    productions, start_symbol = with_bt["nested_parentheses_broaderTransitive.cnf"]
    path = tmp_path / "nested_parentheses_broaderTransitive.cnf"
    write_cnf(productions, start_symbol, path)
    assert path.read_text() == EXPECTED_RDF_BROADER_TRANSITIVE_CNf


def test_cnf_lite_breaks_long_rhs():
    assert cnf_lite([("A", ("a", "B", "c", "d"))]) == [
        ("A", ("a", "N1")),
        ("N1", ("B", "N2")),
        ("N2", ("c", "d")),
    ]


def test_cnf_lite_short_and_epsilon_untouched():
    assert cnf_lite([("A", ()), ("B", ("x",)), ("C", ("y", "z"))]) == [
        ("A", ()),
        ("B", ("x",)),
        ("C", ("y", "z")),
    ]


def test_cnf_lite_auxiliary_names_deterministic():
    productions = [("A", ("a", "b", "c")), ("D", ("d", "e", "f"))]
    assert cnf_lite(productions) == cnf_lite(list(productions))
    assert [lhs for lhs, _ in cnf_lite(productions)] == ["A", "N1", "D", "N2"]


def test_instantiate_template():
    template = [("P", ("load_r", "Q")), ("Q", ("x",)), ("R", ("y", "z"))]
    index_sets = {"load_r": {0, 1}, "Q": {1}}
    assert instantiate_template(template, index_sets) == [
        ("P", ("load_0_r", "Q_0")),
        ("P", ("load_1_r", "Q_1")),
        ("Q_1", ("x",)),
        ("R", ("y", "z")),
    ]
