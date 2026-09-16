import re

from check_version_sync import config_version, pyproject_version


def test_config_and_pyproject_versions_match():
    assert config_version() == pyproject_version()


def test_config_version_is_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", config_version())
