from __future__ import annotations

from pathlib import Path

import pytest

from hyperfocus.config.exceptions import ConfigFileError
from hyperfocus.config.file import ConfigFile

from tests.conftest import pytest_regex


TEST_MODEL = {
    "core": {
        "force_color": False,
    }
}


@pytest.mark.parametrize(
    "config_path",
    [
        "/path/file.ini",
        Path("/path/file.ini"),
    ],
)
def test_config_file_path(config_path):
    config_file = ConfigFile(config_path, model={})

    assert Path(config_file.path) == Path("/path/file.ini")


def test_config_file_exists(test_dir, dummy_dir):
    config_path1 = dummy_dir / "config.ini"
    config_path2 = test_dir / "config.ini"
    config_path2.touch()
    config_file1 = ConfigFile(config_path1, model=TEST_MODEL)
    config_file2 = ConfigFile(config_path2, model=TEST_MODEL)

    assert config_file1.exists() is False
    assert config_file2.exists() is True


def test_config_file_read(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config_file = ConfigFile(config_path, model=TEST_MODEL)

    result = config_file.read()

    expected_result = {
        "core": {
            "database": "/test/database.sqlite",
            "force_color": True,
        },
        "alias": {
            "st": "status",
            "del": "delete",
        },
    }
    assert result == expected_result


def test_config_file_write(test_dir):
    config_path = test_dir / "config.ini"
    config_path.touch()
    config_file = ConfigFile(config_path, model=TEST_MODEL)

    config = {
        "section": {
            "test": "test",
        },
    }
    config_file.write(config)

    with open(config_path) as f:
        expected = pytest_regex(r"\[section\]\ntest = (.*)")
        assert expected == f.read()


def test_config_file_write_fails(dummy_dir):
    config_path = dummy_dir / "config.ini"
    config_file = ConfigFile(config_path, model=TEST_MODEL)

    # match=r"Saving config to (.*) failed: (.*)"
    with pytest.raises(ConfigFileError):
        config_file.write(config={})
