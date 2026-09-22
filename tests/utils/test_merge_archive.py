import pathlib
import shutil

from check_archive_structure import validate_archive
from merge_archive import main, merge_archives
from test_check_archive_structure import (
    _partial_tree,
    _query_dir,
    _tarball,
    _valid_tree,
)


def _new_query_partial(root: pathlib.Path, name: str = "g") -> pathlib.Path:
    d = root / name
    _query_dir(d, "cfpq", "t", ".cnf")
    (d / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/t\n- Language: a*.\n- Purpose: test.\n"
    )
    return d


def _unpacked(output: pathlib.Path, tmp_path: pathlib.Path) -> pathlib.Path:
    dest = tmp_path / "unpacked"
    shutil.unpack_archive(output, dest)
    return next(dest.iterdir())


def test_merge_writes_valid_archive(tmp_path):
    existing = _valid_tree(tmp_path)
    partial = _new_query_partial(tmp_path / "p")
    output = tmp_path / "out" / "g.tar.gz"
    output.parent.mkdir()

    problems = merge_archives(existing, partial, output)

    assert problems == []
    assert validate_archive(output) == []
    merged = _unpacked(output, tmp_path / "u")
    assert (merged / "queries" / "cfpq" / "s").is_dir()
    assert (merged / "queries" / "cfpq" / "t").is_dir()


def test_merge_appends_readme_sections(tmp_path):
    existing = _valid_tree(tmp_path)
    partial = _new_query_partial(tmp_path / "p")
    output = tmp_path / "out" / "g.tar.gz"
    output.parent.mkdir()

    merge_archives(existing, partial, output)

    readme = _unpacked(output, tmp_path / "u") / "queries" / "README.md"
    text = readme.read_text(encoding="utf-8")
    assert text.count("# Queries for g") == 1
    assert "## cfpq/s" in text and "## cfpq/t" in text


def test_merge_collision(tmp_path):
    existing = _valid_tree(tmp_path)
    partial = _partial_tree(tmp_path / "p")  # adds cfpq/s, which exists
    output = tmp_path / "out" / "g.tar.gz"

    problems = merge_archives(existing, partial, output)

    assert any("already exists in the existing archive" in p for p in problems)
    assert not output.exists()


def test_merge_name_mismatch(tmp_path):
    existing = _valid_tree(tmp_path)
    partial = _new_query_partial(tmp_path / "p", name="other")
    output = tmp_path / "out" / "g.tar.gz"

    problems = merge_archives(existing, partial, output)

    assert any("named after the same graph" in p for p in problems)


def test_merge_invalid_existing(tmp_path):
    existing = _valid_tree(tmp_path)
    (existing / "graph" / "a.mtx").unlink()
    partial = _new_query_partial(tmp_path / "p")
    output = tmp_path / "out" / "g.tar.gz"

    problems = merge_archives(existing, partial, output)

    assert any(p.startswith("existing archive:") for p in problems)
    assert not output.exists()


def test_merge_invalid_partial(tmp_path):
    existing = _valid_tree(tmp_path)
    partial = _new_query_partial(tmp_path / "p")
    (partial / "queries" / "cfpq" / "t" / "t.cnf").write_text("not a grammar")
    output = tmp_path / "out" / "g.tar.gz"

    problems = merge_archives(existing, partial, output)

    assert any(p.startswith("partial archive:") for p in problems)
    assert not output.exists()


def test_merge_output_name_must_match_graph(tmp_path):
    existing = _valid_tree(tmp_path)
    partial = _new_query_partial(tmp_path / "p")
    output = tmp_path / "out" / "merged.tar.gz"
    output.parent.mkdir()

    problems = merge_archives(existing, partial, output)

    assert any("must be named g.tar.gz" in p for p in problems)
    assert not output.exists()


def test_merge_tarball_inputs(tmp_path):
    (tmp_path / "archives").mkdir()
    (tmp_path / "partials").mkdir()
    existing = _tarball(_valid_tree(tmp_path / "e"), tmp_path / "archives" / "g.tar.gz")
    partial = _tarball(
        _new_query_partial(tmp_path / "p"), tmp_path / "partials" / "g.tar.gz"
    )
    output = tmp_path / "out" / "g.tar.gz"
    output.parent.mkdir()

    problems = merge_archives(existing, partial, output)

    assert problems == []
    assert validate_archive(output) == []


def test_merge_partial_from_drive_url(tmp_path, monkeypatch):
    existing = _valid_tree(tmp_path)
    partial_tarball = _tarball(
        _new_query_partial(tmp_path / "p"), tmp_path / "partial.tar.gz"
    )
    output = tmp_path / "out" / "g.tar.gz"
    output.parent.mkdir()

    def fake_download(file_id, dest):
        assert file_id == "FILEID123"
        pathlib.Path(dest).write_bytes(partial_tarball.read_bytes())
        return pathlib.Path(dest)

    monkeypatch.setattr("merge_archive.download_from_drive", fake_download)

    problems = merge_archives(
        existing, "https://drive.google.com/file/d/FILEID123/view", output
    )

    assert problems == []
    assert validate_archive(output) == []


def test_merge_partial_from_bare_file_id(tmp_path, monkeypatch):
    existing = _valid_tree(tmp_path)
    partial_tarball = _tarball(
        _new_query_partial(tmp_path / "p"), tmp_path / "partial.tar.gz"
    )
    output = tmp_path / "out" / "g.tar.gz"
    output.parent.mkdir()

    def fake_download(file_id, dest):
        assert file_id == "ABC-xyz_789"
        pathlib.Path(dest).write_bytes(partial_tarball.read_bytes())
        return pathlib.Path(dest)

    monkeypatch.setattr("merge_archive.download_from_drive", fake_download)

    problems = merge_archives(existing, "ABC-xyz_789", output)

    assert problems == []


def test_merge_unknown_partial_source(tmp_path):
    existing = _valid_tree(tmp_path)
    output = tmp_path / "out" / "g.tar.gz"

    problems = merge_archives(existing, "no/such/file.tar.gz", output)

    assert any("no such file" in p for p in problems)


def test_merge_does_not_mutate_existing_directory(tmp_path):
    existing = _valid_tree(tmp_path)
    partial = _new_query_partial(tmp_path / "p")
    # A wrong output name fails the merge after the copy step.
    output = tmp_path / "out" / "merged.tar.gz"

    problems = merge_archives(existing, partial, output)

    assert any("must be named g.tar.gz" in p for p in problems)
    assert not (existing / "queries" / "cfpq" / "t").exists()
    readme = (existing / "queries" / "README.md").read_text(encoding="utf-8")
    assert "## cfpq/t" not in readme


def test_main_passes(tmp_path, capsys):
    existing = _valid_tree(tmp_path)
    partial = _new_query_partial(tmp_path / "p")
    output = tmp_path / "out" / "g.tar.gz"
    output.parent.mkdir()

    assert main([str(existing), str(partial), "-o", str(output)]) == 0
    assert "merged archive written to" in capsys.readouterr().out


def test_main_reports_problems(tmp_path, capsys):
    existing = _valid_tree(tmp_path)
    partial = _partial_tree(tmp_path / "p")  # collides on cfpq/s
    output = tmp_path / "out" / "g.tar.gz"

    assert main([str(existing), str(partial), "-o", str(output)]) == 1
    out = capsys.readouterr().out
    assert "error:" in out and "was not written" in out
