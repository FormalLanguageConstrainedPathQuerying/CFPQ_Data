import pathlib

import flpq_data
from flpq_data.dataset import (
    CACHE_ENV_VAR,
    cache_root,
    cached_versions,
    clear_cache,
    version_dir,
)
from flpq_data.dataset.cache import platformdirs


def test_cache_root_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path / "custom"))
    assert cache_root() == tmp_path / "custom"


def test_cache_root_env_empty_falls_back(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, "")
    monkeypatch.setattr(
        platformdirs, "user_cache_dir", lambda app: str(tmp_path / "os-default")
    )
    assert cache_root() == tmp_path / "os-default"


def test_cache_root_os_default(monkeypatch):
    monkeypatch.delenv(CACHE_ENV_VAR, raising=False)
    monkeypatch.setattr(
        platformdirs, "user_cache_dir", lambda app: str("/home/u/.cache/flpq-data")
    )
    assert cache_root() == pathlib.Path("/home/u/.cache/flpq-data")


def test_version_dir_defaults_to_dataset_version(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path))
    assert version_dir() == tmp_path / "6.0.0"
    assert version_dir("5.0.0") == tmp_path / "5.0.0"


def test_cached_versions_missing_root(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path / "absent"))
    assert cached_versions() == []


def test_cached_versions_lists_dirs_only(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path))
    (tmp_path / "6.0.0").mkdir()
    (tmp_path / "5.0.0").mkdir()
    (tmp_path / "stray.txt").write_text("not a version")
    assert cached_versions() == ["5.0.0", "6.0.0"]


def _make_version_tree(tmp_path: pathlib.Path, *versions: str) -> None:
    for version in versions:
        (tmp_path / version / "graph").mkdir(parents=True)


def test_clear_cache_missing_root(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path / "absent"))
    assert clear_cache() == []


def test_clear_cache_removes_all(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path))
    _make_version_tree(tmp_path, "5.0.0", "6.0.0")

    removed = clear_cache()

    assert removed == [tmp_path / "5.0.0", tmp_path / "6.0.0"]
    assert cached_versions() == []


def test_clear_cache_keeps_one(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path))
    _make_version_tree(tmp_path, "5.0.0", "6.0.0")

    removed = clear_cache(keep="5.0.0")

    assert removed == [tmp_path / "6.0.0"]
    assert cached_versions() == ["5.0.0"]


def test_clear_cache_keeps_current_version(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path))
    _make_version_tree(tmp_path, "5.0.0", "6.0.0")

    removed = clear_cache(keep="6.0.0")

    assert removed == [tmp_path / "5.0.0"]
    assert cached_versions() == ["6.0.0"]


def test_clear_cache_ignores_files_and_unknown_keep(tmp_path, monkeypatch):
    monkeypatch.setenv(CACHE_ENV_VAR, str(tmp_path))
    _make_version_tree(tmp_path, "6.0.0")
    (tmp_path / "stray.txt").write_text("not a version")

    removed = clear_cache(keep="9.9.9")

    assert removed == [tmp_path / "6.0.0"]
    assert (tmp_path / "stray.txt").is_file()
    assert cached_versions() == []


def test_exports():
    assert flpq_data.cache_root() is not None
    assert flpq_data.cached_versions() is not None
    assert flpq_data.clear_cache is clear_cache
