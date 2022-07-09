from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def locations(mocker, test_dir):
    test_config_dir = test_dir / "test_config"
    test_config_dir.mkdir()
    test_config_path = test_config_dir / "config.ini"

    config_dir = mocker.patch("hyperfocus.config.config.CONFIG_DIR", test_config_dir)
    config_path = mocker.patch("hyperfocus.config.config.CONFIG_PATH", test_config_path)

    yield SimpleNamespace(**{"CONFIG_DIR": config_dir, "CONFIG_PATH": config_path})


@pytest.fixture
def dummy_dir():
    return Path("/dummy")
