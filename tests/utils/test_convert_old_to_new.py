import pathlib
import random
import shutil
import tarfile
from collections import Counter

import pytest
from pyformlang.cfg import CFG, Production, Terminal, Variable

from convert_old_to_new import (
    MTX_BANNER,
    MTX_TYPE,
    SECTIONS,
    ConversionError,
    GraphStats,
    JAVA_START,
    JAVA_TEMPLATE,
    build_archive,
    c_alias_cnf,
    cnf_lite,
    convert_csv_to_graph_dir,
    instantiate_template,
    iter_edges,
    java_points_to_cnf,
    load_record,
    make_tarball,
    rdf_cnf_grammars,
    render_readme,
    save_record,
    scan_csv,
    validate_labels,
    verify_conversion,
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


# ---------------------------------------------------------------------------
# Archive assembly and verification
# ---------------------------------------------------------------------------

JAVA_CSV = ["0 1 alloc", "1 2 load_0", "2 3 store_0", "0 2 assign"]
C_ALIAS_CSV = ["0 1 a", "1 2 d", "0 2 a"]
RDF_CSV = ["0 1 subClassOf", "1 2 type", "0 2 subClassOf"]


def test_render_readme_plain():
    readme = render_readme("generations", 129, 273)
    assert "% name: generations" in readme
    assert "% Num Nodes: 129" in readme
    assert "% Num Edges: 273" in readme
    assert "Label conventions" not in readme


def test_render_readme_reversed_labels():
    readme = render_readme("wc", 10, 20, has_reversed_labels=True)
    assert "% Label conventions:" in readme
    assert "% - Edges with the _r suffix are not stored; they are derived by" in readme
    assert "Indexed symbols" not in readme


def test_render_readme_indexed_symbols():
    readme = render_readme(
        "avrora",
        10,
        20,
        has_reversed_labels=True,
        indexed_symbols=["load", "store", "load_r", "store_r"],
    )
    assert "% - Indexed symbols load, store, load_r, store_r match the labels" in readme
    assert (
        "%   load_<k>, store_<k>, load_<k>_r, store_<k>_r for each index k." in readme
    )


@pytest.mark.parametrize(
    ("section", "lines", "grammar_files"),
    [
        ("java_points_to", JAVA_CSV, ["java_points_to.cnf"]),
        ("c_alias", C_ALIAS_CSV, ["c_alias.cnf"]),
        (
            "rdf",
            RDF_CSV,
            [
                "nested_parentheses_subClassOf.cnf",
                "nested_parentheses_subClassOf_type.cnf",
                "nested_parentheses_type.cnf",
            ],
        ),
    ],
)
def test_build_archive_layout(tmp_path, section, lines, grammar_files):
    csv = write_csv(tmp_path / "g.csv", lines)
    tree_dir, stats = build_archive("g", section, csv, tmp_path / "work")

    assert sorted(p.name for p in tree_dir.iterdir()) == [
        "README.md",
        "grammar",
        "graph",
    ]
    assert sorted(p.name for p in (tree_dir / "grammar").iterdir()) == grammar_files
    labels = {line.split()[2] for line in lines}
    assert sorted(p.name for p in (tree_dir / "graph").iterdir()) == sorted(
        f"{label}.mtx" for label in labels
    )

    readme = (tree_dir / "README.md").read_text()
    assert "% name: g" in readme
    assert f"% Num Edges: {len(lines)}" in readme
    assert stats.total_edges == len(lines)


def test_build_archive_replaces_existing_tree(tmp_path):
    csv = write_csv(tmp_path / "g.csv", C_ALIAS_CSV)
    workdir = tmp_path / "work"
    tree_dir, _ = build_archive("g", "c_alias", csv, workdir)
    (tree_dir / "stray.txt").write_text("stray")

    tree_dir, _ = build_archive("g", "c_alias", csv, workdir)
    assert not (tree_dir / "stray.txt").exists()


def test_build_archive_unknown_section(tmp_path):
    csv = write_csv(tmp_path / "g.csv", C_ALIAS_CSV)
    with pytest.raises(ValueError):
        build_archive("g", "nope", csv, tmp_path / "work")


def test_verify_conversion_passes(tmp_path):
    csv = write_csv(tmp_path / "g.csv", JAVA_CSV)
    tree_dir, _ = build_archive("g", "java_points_to", csv, tmp_path / "work")
    verify_conversion(csv, tree_dir)  # must not raise


def test_verify_conversion_detects_corrupted_entry(tmp_path):
    csv = write_csv(tmp_path / "g.csv", JAVA_CSV)
    tree_dir, _ = build_archive("g", "java_points_to", csv, tmp_path / "work")
    mtx = tree_dir / "graph" / "alloc.mtx"
    mtx.write_text(mtx.read_text().replace("0 1\n", "0 2\n", 1))
    with pytest.raises(ConversionError):
        verify_conversion(csv, tree_dir)


def test_verify_conversion_detects_missing_file(tmp_path):
    csv = write_csv(tmp_path / "g.csv", JAVA_CSV)
    tree_dir, _ = build_archive("g", "java_points_to", csv, tmp_path / "work")
    (tree_dir / "graph" / "assign.mtx").unlink()
    with pytest.raises(ConversionError):
        verify_conversion(csv, tree_dir)


def test_verify_conversion_detects_bad_nnz_header(tmp_path):
    csv = write_csv(tmp_path / "g.csv", JAVA_CSV)
    tree_dir, _ = build_archive("g", "java_points_to", csv, tmp_path / "work")
    mtx = tree_dir / "graph" / "load_0.mtx"
    mtx.write_text(mtx.read_text().replace("4 4 1\n", "4 4 2\n", 1))
    with pytest.raises(ConversionError):
        verify_conversion(csv, tree_dir)


def test_verify_conversion_detects_extra_entries(tmp_path):
    csv = write_csv(tmp_path / "g.csv", JAVA_CSV)
    tree_dir, _ = build_archive("g", "java_points_to", csv, tmp_path / "work")
    mtx = tree_dir / "graph" / "alloc.mtx"
    mtx.write_text(mtx.read_text() + "0 1\n")
    with pytest.raises(ConversionError):
        verify_conversion(csv, tree_dir)


def test_make_tarball_roundtrip(tmp_path):
    csv = write_csv(tmp_path / "g.csv", C_ALIAS_CSV)
    tree_dir, _ = build_archive("g", "c_alias", csv, tmp_path / "work")
    tarball = make_tarball(tree_dir, tmp_path / "g.tar.gz")

    with tarfile.open(tarball) as tar:
        names = sorted(member.name for member in tar.getmembers())
    assert names == [
        "g",
        "g/README.md",
        "g/grammar",
        "g/grammar/c_alias.cnf",
        "g/graph",
        "g/graph/a.mtx",
        "g/graph/d.mtx",
    ]

    extract_dir = tmp_path / "extracted"
    with tarfile.open(tarball) as tar:
        tar.extractall(extract_dir)
    assert (extract_dir / "g" / "README.md").read_text() == (
        tree_dir / "README.md"
    ).read_text()


# ---------------------------------------------------------------------------
# S3 pipeline and CLI
# ---------------------------------------------------------------------------


def test_sections_cover_dataset():
    from cfpq_data.dataset import DATASET

    all_names = [name for names in SECTIONS.values() for name in names]
    assert len(all_names) == 54
    assert len(set(all_names)) == 54  # sections are disjoint
    assert set(all_names) == set(DATASET)
    assert len(SECTIONS["rdf"]) == 20
    assert len(SECTIONS["c_alias"]) == 20
    assert len(SECTIONS["java_points_to"]) == 14


def test_record_roundtrip(tmp_path):
    record_path = tmp_path / "record.json"
    assert load_record(record_path) == {}
    record = {"g": {"old_sha256": "a", "new_sha256": "b", "key": "k", "date": "d"}}
    save_record(record_path, record)
    assert load_record(record_path) == record


def make_old_archive(tmp_path, name, lines):
    """A tarball with the old-format layout <name>/<name>.csv + README.md."""
    src = tmp_path / f"{name}_src" / name
    src.mkdir(parents=True)
    (src / f"{name}.csv").write_text("\r\n".join(lines) + "\r\n")
    (src / "README.md").write_text(f"# {name}\n")
    archive = tmp_path / f"{name}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(src, arcname=name)
    return archive


def test_convert_one_dry_run(tmp_path, monkeypatch):
    import convert_old_to_new as conv

    fixture = make_old_archive(tmp_path, "g", C_ALIAS_CSV)
    workdir = tmp_path / "work"

    def fake_download(name, dest_path):
        dest = pathlib.Path(dest_path)
        shutil.copy(fixture, dest)
        return dest

    uploads = []
    monkeypatch.setattr(conv, "download_graph", fake_download)
    monkeypatch.setattr(conv, "upload_file", lambda *a, **k: uploads.append((a, k)))
    monkeypatch.setattr(conv, "verify_public_read", lambda key: None)

    record = {}
    result = conv.convert_one(
        "g",
        "c_alias",
        client=None,
        bucket="b",
        key_prefix="5.0.0/graph",
        record=record,
        record_path=tmp_path / "record.json",
        workdir=workdir,
        dry_run=True,
    )
    assert result["status"] == "dry_run"
    assert result["num_edges"] == len(C_ALIAS_CSV)
    assert uploads == []
    assert record == {}
    assert not (workdir / "g.tar.gz").exists()  # local files cleaned up


def test_convert_one_upload_record_and_skip(tmp_path, monkeypatch):
    import convert_old_to_new as conv

    fixture = make_old_archive(tmp_path, "g", C_ALIAS_CSV)
    workdir = tmp_path / "work"
    record_path = tmp_path / "record.json"

    def fake_download(name, dest_path):
        dest = pathlib.Path(dest_path)
        shutil.copy(fixture, dest)
        return dest

    uploads = []

    def fake_upload(client, local_path, bucket, key=None):
        uploads.append(key)
        return key

    public_reads = []
    monkeypatch.setattr(conv, "download_graph", fake_download)
    monkeypatch.setattr(conv, "upload_file", fake_upload)
    monkeypatch.setattr(
        conv, "verify_public_read", lambda key: public_reads.append(key)
    )

    record = {}
    result = conv.convert_one(
        "g",
        "c_alias",
        client=object(),
        bucket="cfpq-data",
        key_prefix="5.0.0/graph",
        record=record,
        record_path=record_path,
        workdir=workdir,
    )
    assert result["status"] == "uploaded"
    assert uploads == ["5.0.0/graph/g.tar.gz"]
    assert public_reads == ["5.0.0/graph/g.tar.gz"]
    entry = record["g"]
    assert entry["key"] == "5.0.0/graph/g.tar.gz"
    assert entry["old_sha256"] == conv.sha256_of(fixture)
    assert entry["new_sha256"] == result["sha256"]
    assert load_record(record_path) == record

    # Re-run: recorded + publicly readable -> skip without downloading.
    downloads = []

    def failing_download(name, dest_dir):
        downloads.append(name)
        raise AssertionError("must not download a recorded graph")

    monkeypatch.setattr(conv, "download_graph", failing_download)
    result2 = conv.convert_one(
        "g",
        "c_alias",
        client=object(),
        bucket="cfpq-data",
        key_prefix="5.0.0/graph",
        record=record,
        record_path=record_path,
        workdir=workdir,
    )
    assert result2["status"] == "skipped"
    assert downloads == []

    # --force re-converts.
    monkeypatch.setattr(conv, "download_graph", fake_download)
    uploads.clear()
    result3 = conv.convert_one(
        "g",
        "c_alias",
        client=object(),
        bucket="cfpq-data",
        key_prefix="5.0.0/graph",
        record=record,
        record_path=record_path,
        workdir=workdir,
        force=True,
    )
    assert result3["status"] == "uploaded"
    assert len(uploads) == 1


def test_convert_one_keeps_files_on_error(tmp_path, monkeypatch):
    import convert_old_to_new as conv

    fixture = make_old_archive(tmp_path, "g", C_ALIAS_CSV)
    workdir = tmp_path / "work"

    def fake_download(name, dest_path):
        dest = pathlib.Path(dest_path)
        shutil.copy(fixture, dest)
        return dest

    monkeypatch.setattr(conv, "download_graph", fake_download)
    monkeypatch.setattr(
        conv, "build_archive", lambda *a, **k: (_ for _ in ()).throw(ValueError)
    )

    with pytest.raises(ValueError):
        conv.convert_one(
            "g",
            "c_alias",
            client=None,
            bucket="b",
            key_prefix="5.0.0/graph",
            record={},
            record_path=tmp_path / "record.json",
            workdir=workdir,
        )
    assert (workdir / "g_old.tar.gz").exists()  # kept for inspection


def test_cli_expands_sections(tmp_path, monkeypatch):
    import convert_old_to_new as conv

    seen = []

    def fake_convert_one(name, section, **kwargs):
        seen.append((name, section))
        return {
            "name": name,
            "status": "dry_run",
            "num_nodes": 1,
            "num_edges": 1,
            "num_labels": 1,
        }

    monkeypatch.setattr(conv, "convert_one", fake_convert_one)
    conv.main(["rdf", "--dry-run", "--workdir", str(tmp_path)])
    assert [name for name, _ in seen] == SECTIONS["rdf"]
    assert all(section == "rdf" for _, section in seen)


def test_cli_unknown_name_errors():
    import convert_old_to_new as conv

    with pytest.raises(SystemExit):
        conv.main(["nope", "--dry-run"])


def test_cli_requires_credentials_without_dry_run(tmp_path):
    import convert_old_to_new as conv

    with pytest.raises(SystemExit):
        conv.main(["generations", "--workdir", str(tmp_path)])
