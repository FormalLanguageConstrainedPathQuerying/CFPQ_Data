import check_version_sync
import pytest
import set_dev_version


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A throwaway copy of the version-bearing files under ``tmp_path``.

    Both ``check_version_sync.ROOT`` (used by ``config_version`` and
    ``pyproject_version``) and ``set_dev_version.ROOT`` (used for the file
    paths) are redirected here, so no real file is ever touched.
    """
    (tmp_path / "flpq_data").mkdir()
    (tmp_path / "flpq_data" / "config.py").write_text(
        'VERSION = "6.0.0"\n', encoding="utf-8"
    )
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nversion = "6.0.0"\n', encoding="utf-8"
    )
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [Unreleased]\n", encoding="utf-8"
    )
    monkeypatch.setattr(check_version_sync, "ROOT", tmp_path)
    monkeypatch.setattr(set_dev_version, "ROOT", tmp_path)
    return tmp_path


def test_set_dev_version_updates_both_sources(repo):
    set_dev_version.set_dev_version("6.0.0.dev123")
    assert 'VERSION = "6.0.0.dev123"' in (repo / "flpq_data" / "config.py").read_text()
    assert 'version = "6.0.0.dev123"' in (repo / "pyproject.toml").read_text()


def test_set_dev_version_leaves_changelog_untouched(repo):
    before = (repo / "CHANGELOG.md").read_text()
    set_dev_version.set_dev_version("6.0.0.dev123")
    assert (repo / "CHANGELOG.md").read_text() == before


def test_set_dev_version_rejects_non_dev(repo):
    with pytest.raises(ValueError, match="not a valid"):
        set_dev_version.set_dev_version("6.1.0")


def test_set_dev_version_rejects_mismatched_sources(tmp_path, monkeypatch):
    (tmp_path / "flpq_data").mkdir()
    (tmp_path / "flpq_data" / "config.py").write_text(
        'VERSION = "6.0.0"\n', encoding="utf-8"
    )
    (tmp_path / "pyproject.toml").write_text('version = "9.9.9"\n', encoding="utf-8")
    monkeypatch.setattr(check_version_sync, "ROOT", tmp_path)
    monkeypatch.setattr(set_dev_version, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="differ"):
        set_dev_version.set_dev_version("6.0.0.dev123")


def test_set_dev_version_writes_nothing_on_mismatch(repo):
    (repo / "pyproject.toml").write_text('version = "9.9.9"\n', encoding="utf-8")
    before_config = (repo / "flpq_data" / "config.py").read_text()
    with pytest.raises(ValueError, match="differ"):
        set_dev_version.set_dev_version("6.0.0.dev123")
    assert (repo / "flpq_data" / "config.py").read_text() == before_config


def test_main_returns_zero_and_reports(repo, capsys):
    rc = set_dev_version.main(["6.0.0.dev123"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "6.0.0.dev123" in out


def test_main_returns_one_on_bad_version(repo, capsys):
    rc = set_dev_version.main(["nope"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "not a valid" in err
