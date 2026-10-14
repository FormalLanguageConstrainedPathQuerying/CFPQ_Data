import pathlib
import tempfile

from check_archive_structure import unpack_single_dir, validate_archive
from strip_reverse_edges import main, strip_reverse_edges
from test_check_archive_structure import README, _tarball, _valid_tree

MTX = (
    "%%MatrixMarket matrix coordinate pattern general\n"
    "%%GraphBLAS type bool\n2 2 1\n0 1\n"
)

REVERSES_BODY = (
    "20 stored edges:\n"
    "\n"
    "- `a`: 5 edges\n"
    "- `a_r`: 5 edges\n"
    "- `load_<i>` (i = 0..1, 2 labels): 6 edges\n"
    "- `load_r_<i>` (i = 0..1, 2 labels): 4 edges"
)


def _reversed_tree(root: pathlib.Path, name: str = "g") -> pathlib.Path:
    """A valid tree plus stored reverse matrices and a reverses README."""
    tree = _valid_tree(root, name)
    (tree / "graph" / "a_r.mtx").write_text(MTX)
    (tree / "graph" / "load_0.mtx").write_text(MTX)
    (tree / "graph" / "load_r_0.mtx").write_text(MTX)
    (tree / "README.md").write_text(README.replace("Label a: one edge.", REVERSES_BODY))
    return tree


def test_strip_removes_stored_reverses(tmp_path):
    tree = _reversed_tree(tmp_path)
    output = tmp_path / "g.tar.gz"

    report = strip_reverse_edges(tree, output)

    assert report.problems == []
    assert report.removed == ["a_r", "load_r_0"]
    assert report.total_before == 20
    assert report.total_after == 11
    assert output.is_file()
    assert validate_archive(output) == []

    with tempfile.TemporaryDirectory() as tmp:
        root = unpack_single_dir(output, pathlib.Path(tmp))
        assert not (root / "graph" / "a_r.mtx").exists()
        assert not (root / "graph" / "load_r_0.mtx").exists()
        assert (root / "graph" / "a.mtx").is_file()
        assert (root / "graph" / "load_0.mtx").is_file()
        text = (root / "README.md").read_text(encoding="utf-8")
        assert "11 stored edges:" in text
        assert "`a_r`" not in text
        assert "`load_r_<i>`" not in text
        assert "- `a`: 5 edges" in text


def test_strip_tarball_source(tmp_path):
    tarball = _tarball(_reversed_tree(tmp_path), tmp_path / "source.tar.gz")

    report = strip_reverse_edges(tarball, tmp_path / "g.tar.gz")

    assert report.problems == []
    assert report.removed == ["a_r", "load_r_0"]
    assert validate_archive(tmp_path / "g.tar.gz") == []


def test_strip_is_idempotent(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "README.md").write_text(README.replace("Label a: one edge.", "1 edge."))

    report = strip_reverse_edges(tree, tmp_path / "g.tar.gz")

    assert report.problems == []
    assert report.removed == []
    assert report.total_before == 0
    assert report.total_after == 0
    assert validate_archive(tmp_path / "g.tar.gz") == []


def test_strip_rejects_wrong_output_name(tmp_path):
    tree = _reversed_tree(tmp_path)
    output = tmp_path / "other.tar.gz"

    report = strip_reverse_edges(tree, output)

    assert report.problems
    assert "must be named g.tar.gz" in report.problems[0]
    assert not output.exists()


def test_strip_rejects_tree_without_graph_dir(tmp_path):
    tree = tmp_path / "g"
    tree.mkdir()

    report = strip_reverse_edges(tree, tmp_path / "g.tar.gz")

    assert report.problems
    assert "no graph/ directory" in report.problems[0]


def test_strip_rejects_not_an_archive(tmp_path):
    source = tmp_path / "g.tar.gz"
    source.write_text("not a tarball")

    report = strip_reverse_edges(source, tmp_path / "out.tar.gz")

    assert report.problems
    assert not (tmp_path / "out.tar.gz").exists()


def test_main_strips_and_reports(tmp_path, capsys):
    tree = _reversed_tree(tmp_path)
    output = tmp_path / "g.tar.gz"

    assert main([str(tree), "-o", str(output)]) == 0

    out = capsys.readouterr().out
    assert "removed 2 reverse matrix file(s)" in out
    assert "20 -> 11" in out
    assert validate_archive(output) == []


def test_main_reports_problems(tmp_path, capsys):
    tree = _reversed_tree(tmp_path)

    assert main([str(tree), "-o", str(tmp_path / "other.tar.gz")]) == 1
    assert "error:" in capsys.readouterr().out


def test_readme_without_total_line(tmp_path):
    tree = _valid_tree(tmp_path)
    (tree / "graph" / "a_r.mtx").write_text(MTX)
    (tree / "README.md").write_text(
        README.replace(
            "Label a: one edge.",
            "- `a`: 5 edges\n- `a_r`: 5 edges",
        )
    )

    report = strip_reverse_edges(tree, tmp_path / "g.tar.gz")

    assert report.problems == []
    assert report.removed == ["a_r"]
    assert report.total_before == 0
    assert report.total_after == 5
