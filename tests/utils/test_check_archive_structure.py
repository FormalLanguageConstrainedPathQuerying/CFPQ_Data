import pathlib
import shutil
import tarfile
from unittest import mock

from check_archive_structure import _audit, main, validate_archive

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

RESULTS = (
    "%%MatrixMarket matrix coordinate pattern general\n"
    "%%GraphBLAS type bool\n2 2 1\n0 1\n"
)


def _query_dir(
    tree: pathlib.Path, cls: str, name: str, representation: str
) -> pathlib.Path:
    query = tree / "queries" / cls / name
    query.mkdir(parents=True)
    (query / f"{name}{representation}").write_text(
        {
            ".cnf": "S\ta\tN1\nN1\ta\n\nCount:\nS",
            ".rsm": "S -> a*",
            ".re": "a*",
            ".mcfg": "A(a)\nS(x1) <- A(x1)",
        }[representation]
    )
    (query / "results.mtx").write_text(RESULTS)
    return query


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
    _query_dir(d, "cfpq", "s", ".cnf")
    (d / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n- Purpose: test.\n"
    )
    return d


def _partial_tree(root: pathlib.Path, name: str = "g") -> pathlib.Path:
    d = root / name
    _query_dir(d, "cfpq", "s", ".cnf")
    (d / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n- Purpose: test.\n"
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


def test_single_class_dir_missing_is_ok(tmp_path):
    tree = _valid_tree(tmp_path)
    shutil.rmtree(tree / "queries" / "rpq")

    assert validate_archive(tree) == []


def test_all_class_dirs_missing(tmp_path):
    tree = _valid_tree(tmp_path)
    for cls in ("cfpq", "rpq", "mcfpq"):
        shutil.rmtree(tree / "queries" / cls)

    problems = validate_archive(tree)

    assert any("at least one class directory is required" in p for p in problems)


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


def test_inconsistent_graph_dimensions(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "graph" / "b.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n3 3 0\n"
    )

    problems = validate_archive(tree)

    assert any("same dimensions" in p for p in problems)


def test_flat_query_file_is_rejected(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "x.cnf").write_text("S -> a")

    problems = validate_archive(tree)

    assert any("must be a query directory" in p for p in problems)


def test_missing_results_mtx(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "results.mtx").unlink()

    problems = validate_archive(tree)

    assert any("missing results.mtx" in p for p in problems)


def test_query_dir_without_representation(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "s.cnf").unlink()

    problems = validate_archive(tree)

    assert any("no cfpq representation file" in p for p in problems)


def test_stray_file_in_query_dir(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "notes.txt").write_text("extra")

    problems = validate_archive(tree)

    assert any(
        "representation files and results.mtx are allowed" in p for p in problems
    )


def test_results_mtx_wrong_dimensions(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "results.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n3 3 1\n0 1\n"
    )

    problems = validate_archive(tree)

    assert any("must be a 2x2 matrix" in p for p in problems)


def test_results_mtx_out_of_range(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "results.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n2 2 1\n0 5\n"
    )

    problems = validate_archive(tree)

    assert any("results.mtx: entry (0, 5) is outside" in p for p in problems)


def test_results_mtx_unparseable(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "results.mtx").write_text("garbage")

    problems = validate_archive(tree)

    assert any("cannot be parsed as a Boolean MatrixMarket file" in p for p in problems)


def test_unparseable_cnf(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "s.cnf").write_text("not a grammar")

    problems = validate_archive(tree)

    assert any("cannot be parsed as a cfpq query" in p for p in problems)


def test_inert_label_is_accepted(tmp_path):
    # A terminal matching no stored label stays inert on materialization;
    # the query is legal and yields an empty result.
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "s.cnf").write_text("S\tz\n\nCount:\nS")

    assert validate_archive(tree) == []


def test_reversed_label_is_accepted(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "s.cnf").write_text("S\ta_r\n\nCount:\nS")

    assert validate_archive(tree) == []


def test_indexed_placeholder_label_is_accepted(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "graph" / "a.mtx").unlink()
    (tree / "graph" / "load_0.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n2 2 1\n0 1\n"
    )
    (tree / "queries" / "cfpq" / "s" / "s.cnf").write_text("S\tload_i\n\nCount:\nS")

    assert validate_archive(tree) == []


def test_query_without_terminals(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "s.cnf").write_text("S\tN1\nN1\tS\n\nCount:\nS")

    problems = validate_archive(tree)

    assert any("uses no terminal" in p for p in problems)


def test_rsm_representation_is_accepted(tmp_path):
    tree = _valid_tree(tmp_path)
    query = _query_dir(tree, "cfpq", "t", ".rsm")
    (query / "t.rsm").write_text(
        "start: S\n[box S]\nstart: 0\nfinal: 2\n0 --a--> 1\n1 --a--> 2"
    )
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n\n## cfpq/t\n- Language: aa.\n"
    )

    assert validate_archive(tree) == []


def test_rsm_inert_label_is_accepted(tmp_path):
    tree = _valid_tree(tmp_path)
    query = _query_dir(tree, "cfpq", "t", ".rsm")
    (query / "t.rsm").write_text("S -> z*")
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n\n## cfpq/t\n- Language: z*.\n"
    )

    assert validate_archive(tree) == []


def test_unparseable_rsm(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "t.rsm").write_text("garbage")

    problems = validate_archive(tree)

    assert any("cannot be parsed as a cfpq query" in p for p in problems)


def test_rpq_and_mcfpq_queries_parse(tmp_path):
    tree = _valid_tree(tmp_path)
    _query_dir(tree, "rpq", "p", ".re")
    _query_dir(tree, "mcfpq", "m", ".mcfg")
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n"
        "\n## mcfpq/m\n- Language: a*.\n"
        "\n## rpq/p\n- Language: a*.\n"
    )

    assert validate_archive(tree) == []


def test_rpq_regular_rsm_is_accepted(tmp_path):
    tree = _valid_tree(tmp_path)
    query = _query_dir(tree, "rpq", "p", ".rsm")
    (query / "p.rsm").write_text("[box S]\nstart: 0\nfinal: 1\n0 --a--> 1")
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n\n## rpq/p\n- Language: a*.\n"
    )

    assert validate_archive(tree) == []


def test_rpq_recursive_rsm_is_rejected(tmp_path):
    tree = _valid_tree(tmp_path)
    query = _query_dir(tree, "rpq", "p", ".rsm")
    (query / "p.rsm").write_text("S -> a S b | a b")
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n\n## rpq/p\n- Language: a*b*.\n"
    )

    problems = validate_archive(tree)

    assert any("must be regular" in p for p in problems)


def test_unparseable_mcfg(tmp_path):
    tree = _valid_tree(tmp_path)
    query = _query_dir(tree, "mcfpq", "m", ".mcfg")
    (query / "m.mcfg").write_text("S(x1 x2) <- A(x1)")
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n"
        "\n## mcfpq/m\n- Language: broken.\n"
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
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n"
        "\n## cfpq/missing\n- Language: nowhere.\n"
    )

    problems = validate_archive(tree)

    assert any("does not match any query directory" in p for p in problems)


def test_undocumented_query(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "README.md").write_text("# Queries for g\n")

    problems = validate_archive(tree)

    assert any("no section describing 'cfpq/s'" in p for p in problems)


def test_empty_query_section(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n\n## cfpq/other\n- Language: a*.\n"
    )

    problems = validate_archive(tree)

    assert any("the section for 'cfpq/s' is empty" in p for p in problems)


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


def test_valid_partial_passes(tmp_path):
    assert validate_archive(_partial_tree(tmp_path), partial=True) == []


def test_valid_partial_tarball_passes(tmp_path):
    tree = _partial_tree(tmp_path)
    assert validate_archive(_tarball(tree, tmp_path / "g.tar.gz"), partial=True) == []


def test_partial_tarball_top_level_must_match_name(tmp_path):
    tree = _partial_tree(tmp_path, name="other")
    tarball = _tarball(tree, tmp_path / "g.tar.gz")

    problems = validate_archive(tarball, partial=True)

    assert any("must be named after the archive" in p for p in problems)


def test_partial_rejects_graph_dir(tmp_path):
    tree = _partial_tree(tmp_path)
    (tree / "graph").mkdir()

    problems = validate_archive(tree, partial=True)

    assert any("'graph'" in p and "unexpected entry" in p for p in problems)


def test_partial_missing_queries(tmp_path):
    tree = tmp_path / "g"
    tree.mkdir()

    problems = validate_archive(tree, partial=True)

    assert any("missing entry 'queries'" in p for p in problems)


def test_partial_requires_class_dir(tmp_path):
    tree = _partial_tree(tmp_path)
    shutil.rmtree(tree / "queries" / "cfpq")

    problems = validate_archive(tree, partial=True)

    assert any("at least one class directory is required" in p for p in problems)


def test_partial_empty_class_dir(tmp_path):
    tree = _partial_tree(tmp_path)
    shutil.rmtree(tree / "queries" / "cfpq" / "s")

    problems = validate_archive(tree, partial=True)

    assert any("must add at least one query" in p for p in problems)


def test_partial_flat_file_rejected(tmp_path):
    tree = _partial_tree(tmp_path)
    (tree / "queries" / "cfpq" / "x.cnf").write_text("S -> a")

    problems = validate_archive(tree, partial=True)

    assert any("must be a query directory" in p for p in problems)


def test_partial_missing_results(tmp_path):
    tree = _partial_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "results.mtx").unlink()

    problems = validate_archive(tree, partial=True)

    assert any("missing results.mtx" in p for p in problems)


def test_partial_unparseable_representation(tmp_path):
    tree = _partial_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "s.cnf").write_text("not a grammar")

    problems = validate_archive(tree, partial=True)

    assert any("cannot be parsed as a cfpq query" in p for p in problems)


def test_partial_readme_orphan_section(tmp_path):
    tree = _partial_tree(tmp_path)
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n"
        "\n## cfpq/missing\n- Language: nowhere.\n"
    )

    problems = validate_archive(tree, partial=True)

    assert any("does not match any query directory" in p for p in problems)


def test_partial_readme_undocumented_query(tmp_path):
    tree = _partial_tree(tmp_path)
    (tree / "queries" / "README.md").write_text("# Queries for g\n")

    problems = validate_archive(tree, partial=True)

    assert any("no section describing 'cfpq/s'" in p for p in problems)


def test_partial_readme_empty_section(tmp_path):
    tree = _partial_tree(tmp_path)
    (tree / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n\n## cfpq/other\n- Language: a*.\n"
    )

    problems = validate_archive(tree, partial=True)

    assert any("the section for 'cfpq/s' is empty" in p for p in problems)


def test_full_mode_rejects_partial_tree(tmp_path):
    tree = _partial_tree(tmp_path)

    problems = validate_archive(tree)

    assert any("missing entry 'graph'" in p for p in problems)


def test_main_partial_passes(tmp_path, capsys):
    tree = _partial_tree(tmp_path)

    assert main([str(tree), "--partial"]) == 0
    assert "partial archive structure ok" in capsys.readouterr().out


def test_main_partial_reports_problems(tmp_path, capsys):
    tree = _partial_tree(tmp_path)
    (tree / "queries" / "cfpq" / "s" / "results.mtx").unlink()

    assert main([str(tree), "--partial"]) == 1
    out = capsys.readouterr().out
    assert "error:" in out and "structure violation" in out


def _mock_s3(archives: dict[str, bytes]) -> mock.Mock:
    client = mock.Mock()
    client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key} for key in sorted(archives)]}
    ]

    def download(bucket, key, dest):
        pathlib.Path(dest).write_bytes(archives[key])

    client.download_file.side_effect = download
    return client


def test_audit_passes_valid_archives(tmp_path):
    tarball = _tarball(_valid_tree(tmp_path), tmp_path / "g.tar.gz")
    client = _mock_s3({"5.0.0/graph/g.tar.gz": tarball.read_bytes()})

    assert _audit(client, "cfpq-data", "5.0.0/graph") == []


def test_audit_reports_invalid_archive_with_its_key(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "README.md").write_text(README.replace("## License\nApache-2.0.\n", ""))
    tarball = _tarball(tree, tmp_path / "g.tar.gz")
    client = _mock_s3({"5.0.0/graph/g.tar.gz": tarball.read_bytes()})

    problems = _audit(client, "cfpq-data", "5.0.0/graph")

    assert any(
        p.startswith("5.0.0/graph/g.tar.gz:") and "'## License'" in p for p in problems
    )


def test_audit_without_archives_reports_it(tmp_path):
    client = _mock_s3({})

    problems = _audit(client, "cfpq-data", "5.0.0/graph")

    assert any("no .tar.gz objects found" in p for p in problems)


def test_main_audit_requires_credentials(capsys):
    assert main(["--audit"]) == 1
    assert "required for --audit" in capsys.readouterr().out


def test_main_audit_validates_bucket(tmp_path, monkeypatch, capsys):
    tarball = _tarball(_valid_tree(tmp_path), tmp_path / "g.tar.gz")
    client = _mock_s3({"5.0.0/graph/g.tar.gz": tarball.read_bytes()})
    monkeypatch.setattr("upload_to_s3.boto3.client", lambda *args, **kwargs: client)

    status = main(
        [
            "--audit",
            "--prefix",
            "5.0.0/graph",
            "--access-key-id",
            "key-id",
            "--secret-access-key",
            "secret",
        ]
    )

    assert status == 0
    assert "archive structure ok" in capsys.readouterr().out
