import pathlib
import shutil
import tarfile

from check_archive_structure import main, validate_archive

README = """# g

## What is this graph?
A test graph.

## Source
A test source.

## Construction
Generated.

## Nodes
Two nodes.

## Edges and labels
Label a: one edge.

## Query classes
CFPQ applies.

## License
Apache-2.0.

## Caveats
None.
"""


def _valid_tree(root: pathlib.Path, name: str = "g") -> pathlib.Path:
    d = root / name
    (d / "graph").mkdir(parents=True)
    for cls in ("cfpq", "rpq", "mcfpq"):
        (d / "queries" / cls).mkdir(parents=True)
    (d / "README.md").write_text(README)
    (d / "graph" / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n2 2 1\n0 1\n"
    )
    (d / "queries" / "cfpq" / "s.cnf").write_text("S -> a S | epsilon")
    (d / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s.cnf\n- Language: a*.\n- Purpose: test.\n"
    )
    return d


def _tarball(tree: pathlib.Path, dest: pathlib.Path) -> pathlib.Path:
    with tarfile.open(dest, "w:gz") as tarball:
        tarball.add(tree, arcname=tree.name)
    return dest


def test_valid_directory_passes(tmp_path):
    assert validate_archive(_valid_tree(tmp_path)) == []


def test_valid_tarball_passes(tmp_path):
    tree = _valid_tree(tmp_path)
    assert validate_archive(_tarball(tree, tmp_path / "g.tar.gz")) == []


def test_tarball_top_level_must_match_name(tmp_path):
    tree = _valid_tree(tmp_path, name="other")
    tarball = _tarball(tree, tmp_path / "g.tar.gz")

    problems = validate_archive(tarball)

    assert any("must be named after the archive" in p for p in problems)


def test_extra_top_level_entry(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "notes.txt").write_text("extra")

    problems = validate_archive(tree)

    assert any("'notes.txt'" in p for p in problems)


def test_missing_class_dir(tmp_path):
    tree = _valid_tree(tmp_path)
    shutil.rmtree(tree / "queries" / "rpq")

    problems = validate_archive(tree)

    assert any("queries/rpq: missing" in p for p in problems)


def test_non_mtx_file_in_graph(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "graph" / "b.txt").write_text("not a matrix")

    problems = validate_archive(tree)

    assert any("graph/b.txt" in p for p in problems)


def test_empty_graph_dir(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "graph" / "a.mtx").unlink()

    problems = validate_archive(tree)

    assert any("at least one .mtx file" in p for p in problems)


def test_malformed_mtx(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "graph" / "a.mtx").write_text("garbage")

    problems = validate_archive(tree)

    assert any(p.startswith("graph/:") for p in problems)


def test_out_of_range_edge(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "graph" / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n2 2 1\n0 5\n"
    )

    problems = validate_archive(tree)

    assert any("outside the declared" in p for p in problems)


def test_unparseable_cnf(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s.cnf").write_text("not a grammar")

    problems = validate_archive(tree)

    assert any("cannot be parsed as a cfpq query" in p for p in problems)


def test_unknown_label(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s.cnf").write_text("S -> z | epsilon")

    problems = validate_archive(tree)

    assert any("'z' is not a stored label" in p for p in problems)


def test_reversed_label_is_accepted(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s.cnf").write_text("S -> a_r | epsilon")

    assert validate_archive(tree) == []


def test_query_without_terminals(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s.cnf").write_text("S -> epsilon")

    problems = validate_archive(tree)

    assert any("uses no terminal" in p for p in problems)


def test_rpq_and_mcfpq_queries_parse(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "rpq" / "p.re").write_text("a*")
    (tree / "queries" / "mcfpq" / "m.mcfg").write_text("A(a)\nS(x1) <- A(x1)")
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s.cnf\n- Language: a*.\n"
        "\n## mcfpq/m.mcfg\n- Language: a*.\n"
        "\n## rpq/p.re\n- Language: a*.\n"
    )

    assert validate_archive(tree) == []


def test_unparseable_mcfg(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "mcfpq" / "m.mcfg").write_text("S(x1 x2) <- A(x1)")
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s.cnf\n- Language: a*.\n"
        "\n## mcfpq/m.mcfg\n- Language: broken.\n"
    )

    problems = validate_archive(tree)

    assert any("cannot be parsed as a mcfpq query" in p for p in problems)


def test_missing_mandatory_section(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "README.md").write_text(README.replace("## License\nApache-2.0.\n", ""))

    problems = validate_archive(tree)

    assert any("'## License'" in p for p in problems)


def test_orphan_query_section(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s.cnf\n- Language: a*.\n"
        "\n## cfpq/missing.cnf\n- Language: nowhere.\n"
    )

    problems = validate_archive(tree)

    assert any("does not match any query file" in p for p in problems)


def test_undocumented_query(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "README.md").write_text("# Queries for g\n")

    problems = validate_archive(tree)

    assert any("no section describing 'cfpq/s.cnf'" in p for p in problems)


def test_empty_query_section(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s.cnf\n\n## cfpq/other.cnf\n- Language: a*.\n"
    )

    problems = validate_archive(tree)

    assert any("the section for 'cfpq/s.cnf' is empty" in p for p in problems)


def test_wrong_extension_in_class_dir(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "x.re").write_text("a*")

    problems = validate_archive(tree)

    assert any("queries/cfpq/x.re" in p for p in problems)


def test_not_an_archive(tmp_path):
    file = tmp_path / "g.tar.gz"
    file.write_text("not a tarball")

    problems = validate_archive(file)

    assert any("not a .tar.gz archive" in p for p in problems)


def test_main_reports_problems(tmp_path, capsys):
    tree = _valid_tree(tmp_path)
    (tree / "README.md").write_text(README.replace("## License\nApache-2.0.\n", ""))

    assert main([str(tree)]) == 1
    out = capsys.readouterr().out
    assert "error:" in out and "structure violation" in out


def test_main_passes_valid_archive(tmp_path, capsys):
    tree = _valid_tree(tmp_path)

    assert main([str(tree)]) == 0
    assert "archive structure ok" in capsys.readouterr().out
