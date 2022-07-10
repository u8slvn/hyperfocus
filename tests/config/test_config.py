import pytest

from hyperfocus.config.config import Config
from hyperfocus.config.exceptions import ConfigError
from tests.conftest import pytest_regex


def test_config_make_directory(locations):
    Config.make_directory()

    assert locations.CONFIG_DIR.exists()


def test_config_make_directory_fails(mocker, dummy_dir):
    mocker.patch("hyperfocus.config.config.CONFIG_DIR", dummy_dir)

    with pytest.raises(ConfigError, match=r"Configuration folder creation failed"):
        Config.make_directory()


def test_load_config(fixtures_dir):
    config_path = fixtures_dir / "config.ini"

    loaded_config1 = Config.load(config_path, reload=True)
    loaded_config2 = Config.load()

    expected_database = "/test/database.sqlite"
    assert loaded_config1["core.database"] == expected_database
    assert loaded_config2["core.database"] == expected_database
    assert id(loaded_config1) == id(loaded_config2)


def test_load_missing_config_fails(dummy_dir):
    config_path = dummy_dir / "config.ini"

    with pytest.raises(
        ConfigError, match="Config does not exist, please run init command first"
    ):
        _ = Config.load(config_path, reload=True)


def test_save_config(locations):
    config = Config()

    config.save()

    assert locations.CONFIG_PATH.exists()
    with open(locations.CONFIG_PATH) as f:
        expected = pytest_regex(r"\[core\]\ndatabase = (.*)")
        assert expected == f.read()


def test_config_save_fails(mocker, dummy_dir):
    config_path = dummy_dir / "config.ini"
    mocker.patch("hyperfocus.config.config.CONFIG_PATH", config_path)
    config = Config()

    with pytest.raises(ConfigError, match=r"Saving config to (.*) failed: (.*)"):
        config.save()


def test_update_config_options(mocker, fixtures_dir, test_dir):
    mocker.patch("hyperfocus.cli.get_commands", return_value=["test", "delete"])
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    config["core.database"] = str(test_dir / "new_config.ini")
    config.update_option("alias.st", "test")

    expected_config = {
        "core": {
            "database": str(test_dir / "new_config.ini"),
        },
        "alias": {
            "st": "test",
            "del": "delete",
        },
    }
    assert config.config == expected_config


def test_update_config_options_does_not_exist_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Variable (.*) does not exist"):
        config["dummy.database"] = "/test"


def test_update_config_options_bad_format_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Bad format config option (.*)"):
        config["core.dummy.foo"] = "/test"


def test_get_config_options(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    database = config["core.database"]
    alias_st = config.get_option("alias.st")

    assert database == "/test/database.sqlite"
    assert alias_st == "status"


def test_get_config_options_does_not_exist_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Variable '(.*)' does not exist"):
        _ = config["core.dummy"]


def test_get_config_options_bad_format_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Bad format config option (.*)"):
        _ = config["core.dummy.foo"]


def test_delete_config_options(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    del config["core.database"]
    config.delete_option("alias.st")

    expected_config = {
        "core": {},
        "alias": {
            "del": "delete",
        },
    }
    assert config.config == expected_config


def test_delete_config_options_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Variable (.*) does not exist"):
        del config["core.dummy"]


def test_delete_config_options_bad_format_fails(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    with pytest.raises(ConfigError, match=r"Bad format config option (.*)"):
        del config["core.dummy.foo"]


def test_config_contains_option(fixtures_dir):
    config_path = fixtures_dir / "config.ini"
    config = Config.load(config_path, reload=True)

    assert "core.database" in config
