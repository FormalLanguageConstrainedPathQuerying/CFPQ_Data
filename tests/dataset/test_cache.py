import pathlib

import flpq_data
from flpq_data.dataset import CACHE_ENV_VAR, cache_root, cached_versions, version_dir
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


def test_exports():
    assert flpq_data.cache_root() is not None
    assert flpq_data.cached_versions() is not None
