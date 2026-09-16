import bump_version
import check_version_sync
import pytest


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A throwaway copy of the three version-bearing files under ``tmp_path``.

    Both ``bump_version.ROOT`` and ``check_version_sync.ROOT`` are redirected
    here so no real file in the repository is ever touched.
    """
    (tmp_path / "cfpq_data").mkdir()
    (tmp_path / "cfpq_data" / "config.py").write_text(
        'VERSION = "5.0.0"\n', encoding="utf-8"
    )
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nversion = "5.0.0"\n', encoding="utf-8"
    )
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- a change\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(bump_version, "ROOT", tmp_path)
    monkeypatch.setattr(check_version_sync, "ROOT", tmp_path)
    return tmp_path


def test_bump_updates_all_sources(repo):
    bump_version.bump("5.1.0", date="2026-09-08")
    assert 'VERSION = "5.1.0"' in (repo / "cfpq_data" / "config.py").read_text()
    assert 'version = "5.1.0"' in (repo / "pyproject.toml").read_text()
    changelog = (repo / "CHANGELOG.md").read_text()
    assert "## [Unreleased]" in changelog
    assert "## [5.1.0] - 2026-09-08" in changelog


def test_bump_orders_unreleased_before_dated_section(repo):
    bump_version.bump("5.1.0", date="2026-09-08")
    changelog = (repo / "CHANGELOG.md").read_text()
    # Fresh empty [Unreleased] first, then the dated section, then the body.
    assert changelog.index("## [Unreleased]") < changelog.index(
        "## [5.1.0] - 2026-09-08"
    )
    assert changelog.index("## [5.1.0] - 2026-09-08") < changelog.index("- a change")


def test_bump_rejects_bad_semver(repo):
    with pytest.raises(ValueError, match="not a valid"):
        bump_version.bump("5.1")


def test_bump_rejects_mismatched_sources(tmp_path, monkeypatch):
    (tmp_path / "cfpq_data").mkdir()
    (tmp_path / "cfpq_data" / "config.py").write_text(
        'VERSION = "5.0.0"\n', encoding="utf-8"
    )
    (tmp_path / "pyproject.toml").write_text('version = "9.9.9"\n', encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("## [Unreleased]\n", encoding="utf-8")
    monkeypatch.setattr(bump_version, "ROOT", tmp_path)
    monkeypatch.setattr(check_version_sync, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="differ"):
        bump_version.bump("5.1.0")


def test_bump_requires_unreleased_section(repo):
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [5.0.0] - 2026-01-01\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="Unreleased"):
        bump_version.bump("5.1.0")


def test_bump_writes_nothing_when_a_later_step_fails(repo):
    # Drop the [Unreleased] section so the changelog step (the last transform)
    # fails; config.py and pyproject.toml must remain untouched on disk.
    (repo / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
    before_config = (repo / "cfpq_data" / "config.py").read_text()
    before_pyproject = (repo / "pyproject.toml").read_text()
    with pytest.raises(ValueError, match="Unreleased"):
        bump_version.bump("5.1.0")
    assert (repo / "cfpq_data" / "config.py").read_text() == before_config
    assert (repo / "pyproject.toml").read_text() == before_pyproject


def test_main_returns_zero_and_reports(repo, capsys):
    rc = bump_version.main(["5.1.0", "--date", "2026-09-08"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "bumped to 5.1.0" in out


def test_main_returns_one_on_bad_version(repo, capsys):
    rc = bump_version.main(["nope"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "not a valid" in err
