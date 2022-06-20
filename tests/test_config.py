from pathlib import Path

import pytest

from hyperfocus.config import Config
from hyperfocus.exceptions import ConfigError
from tests.conftest import pytest_regex


def test_config_make_directory_success(tmp_test_dir):
    dir_path = tmp_test_dir / "test_config_dir"
    db_path = Path("dummy/path")
    config = Config(db_path=db_path, dir_path=dir_path)

    config.make_directory()

    assert dir_path.exists()


def test_config_make_directory_fails():
    dir_path = Path("dumb/path/test_config")
    db_path = Path("dummy/path")
    config = Config(db_path=db_path, dir_path=dir_path)

    with pytest.raises(ConfigError, match=r"Configuration folder creation failed"):
        config.make_directory()


def test_load_config_success(fixtures_dir):
    file_path = fixtures_dir / "config.ini"

    loaded_config = Config.load(file_path=file_path)

    expected = Config(db_path=Path("dummy/path"))
    assert expected.db_path == loaded_config.db_path


def test_load_missing_config_fails():
    file_path = Path("dummy/path")

    with pytest.raises(
        ConfigError, match="Config does not exist, please run init command first"
    ):
        _ = Config.load(file_path=file_path)


def test_config_save_success(tmp_test_dir):
    db_path = Path("dummy/path")
    config = Config(db_path=db_path, dir_path=tmp_test_dir)

    config.save()

    with open(config.file_path) as f:
        expected = pytest_regex(r"\[main\]\ndb_file_path = dummy/path\n\n")
        assert expected == f.read()


def test_config_save_fails():
    dir_path = Path("dumb/path/test_config")
    db_path = Path("dummy/path")
    config = Config(db_path=db_path, dir_path=dir_path)

    with pytest.raises(
        ConfigError, match=r"Saving config to dumb/path/test_config/config.ini failed"
    ):
        config.save()
