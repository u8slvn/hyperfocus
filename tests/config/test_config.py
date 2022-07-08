from pathlib import Path

import pytest

from hyperfocus.config import Config, ConfigError
from tests.conftest import pytest_regex


def test_config_make_directory(mocker, test_dir):
    config_dir = test_dir / "test_config_dir"
    mocker.patch("hyperfocus.config.config.CONFIG_DIR", config_dir)

    Config.make_directory()

    assert config_dir.exists()


def test_config_make_directory_fails(mocker):
    config_dir = Path("/dummy/test_config_dir")
    mocker.patch("hyperfocus.config.config.CONFIG_DIR", config_dir)

    with pytest.raises(ConfigError, match=r"Configuration folder creation failed"):
        Config.make_directory()


def test_load_config(fixtures_dir):
    config_path = fixtures_dir / "config.ini"

    loaded_config1 = Config.load(config_path, reload=True)
    loaded_config2 = Config.load()

    expected_database = "/dummy/database.sqlite"
    assert loaded_config1["core.database"] == expected_database
    assert loaded_config2["core.database"] == expected_database
    assert id(loaded_config1) == id(loaded_config2)


def test_load_missing_config_fails():
    config_path = Path("/dummy/test_config")

    with pytest.raises(
        ConfigError, match="Config does not exist, please run init command first"
    ):
        _ = Config.load(config_path, reload=True)


def test_save_config(mocker, test_dir):
    config_path = test_dir / "test_config.ini"
    mocker.patch("hyperfocus.config.config.CONFIG_PATH", config_path)
    config = Config()

    config.save()

    assert config_path.exists()
    with open(config_path) as f:
        expected = pytest_regex(r"\[core\]\ndatabase = (.*)")
        assert expected == f.read()


def test_config_save_fails(mocker):
    config_path = Path("/dummy/config.test")
    mocker.patch("hyperfocus.config.config.CONFIG_PATH", config_path)
    config = Config()

    with pytest.raises(ConfigError, match=r"Saving config to (.*) failed:(.*)"):
        config.save()


def test_update_config_variables(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    config["core.database"] = "/test"
    config.update_variable("alias.st", "test")

    expected_config = {
        "core": {
            "database": "/test",
        },
        "alias": {
            "st": "test",
            "del": "delete",
        },
    }
    assert config.config == expected_config


def test_update_config_variables_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Variable (.*) does not exist"):
        config["dummy.database"] = "/test"


def test_get_config_variables(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    database = config["core.database"]
    alias_st = config.get_variable("alias.st")

    assert database == "/dummy/database.sqlite"
    assert alias_st == "status"


def test_get_config_variables_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Variable (.*) does not exist"):
        _ = config["core.dummy"]


def test_delete_config_variables(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    del config["core.database"]
    config.delete_variable("alias.st")

    expected_config = {
        "core": {},
        "alias": {
            "del": "delete",
        },
    }
    assert config.config == expected_config


def test_delete_config_variables_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Variable (.*) does not exist"):
        del config["core.dummy"]


def test_config_contains_variable(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    assert "core.database" in config
