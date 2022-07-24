from pathlib import Path

import pytest

from hyperfocus.config.exceptions import ConfigFileError
from hyperfocus.config.file import ConfigFile
from tests.conftest import pytest_regex


@pytest.mark.parametrize(
    "config_path",
    [
        "/path/file.ini",
        Path("/path/file.ini"),
    ],
)
def test_config_file_path(config_path):
    config_file = ConfigFile(config_path)

    assert config_file.path == "/path/file.ini"


def test_config_file_exists(test_dir, dummy_dir):
    config_path1 = dummy_dir / "config.ini"
    config_path2 = test_dir / "config.ini"
    config_path2.touch()
    config_file1 = ConfigFile(config_path1)
    config_file2 = ConfigFile(config_path2)

    assert config_file1.exists() is False
    assert config_file2.exists() is True


def test_config_file_read(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config_file = ConfigFile(config_path)

    result = config_file.read()

    expected_result = {
        "core": {
            "database": "/test/database.sqlite",
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
    config_file = ConfigFile(config_path)

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
    config_file = ConfigFile(config_path)

    # match=r"Saving config to (.*) failed: (.*)"
    with pytest.raises(ConfigFileError):
        config_file.write(config={})
