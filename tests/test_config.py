import configparser
from pathlib import Path

import pytest

from hyperfocus import config
from hyperfocus.config import Config
from hyperfocus.exceptions import ConfigError, ConfigDoesNotExistError
from tests.conftest import pytest_regex


def test_init_config(mocker, tmp_test_dir):
    dir_path = tmp_test_dir / "test_config_a"
    file_path = dir_path / "config.ini"
    db_path = tmp_test_dir / "db_test_file.sqlite"
    mocker.patch("hyperfocus.config.DIR_PATH", dir_path)
    mocker.patch("hyperfocus.config.FILE_PATH", file_path)

    config.init(db_path=db_path)

    assert db_path.exists()
    assert dir_path.exists()
    assert file_path.exists()
    with open(file_path) as f:
        expected = pytest_regex(r"\[main\]\ndb_path = (.*)\/db_test_file.sqlite\n\n")
        assert expected == f.read()


def test_init_config_failed_on_dir_creation(mocker, tmp_test_dir):
    mocker.patch("hyperfocus.config.DIR_PATH", **{"mkdir.side_effect": OSError})

    with pytest.raises(ConfigError, match=r"Configuration folder creation failed"):
        config.init(db_path=Path("dummy/path"))


def test_init_config_failed_on_file_creation(mocker, tmp_test_dir):
    dir_path = tmp_test_dir / "test_config_b"
    db_path = tmp_test_dir / "db_test_file.sqlite"
    mocker.patch("hyperfocus.config.DIR_PATH", dir_path)
    mocker.patch("hyperfocus.config.FILE_PATH", **{"open.side_effect": OSError})
    dir_path = mocker.patch("hyperfocus.config.configparser.ConfigParser")
    dir_path.mkdir.side_effect = OSError

    with pytest.raises(ConfigError, match=r"Saving config to (.*) failed"):
        config.init(db_path=db_path)


def test_load_config(mocker, tmp_test_dir):
    file_path = tmp_test_dir / "test_config_file.ini"
    mocker.patch("hyperfocus.config.FILE_PATH", file_path)
    config_parser = configparser.ConfigParser()
    config_parser["main"] = {
        "db_path": "dummy/path",
    }
    with file_path.open("w") as file:
        config_parser.write(file)

    loaded_config = config.load()

    expected = Config(db_path=Path("dummy/path"))
    assert expected == loaded_config


def test_load_config_failed(mocker):
    file_path = Path("dummy/path")
    mocker.patch("hyperfocus.config.FILE_PATH", file_path)

    with pytest.raises(ConfigDoesNotExistError):
        _ = config.load()
