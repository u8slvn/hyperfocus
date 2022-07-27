import pytest

from hyperfocus.config.config import Config
from hyperfocus.console.cli import hyf
from hyperfocus.database import database
from hyperfocus.database.models import MODELS, Task, WorkingDay
from hyperfocus.services import DailyTracker


@pytest.fixture(scope="session")
def cli_config(test_dir):
    config = Config()
    Config._dir = test_dir
    config["core.database"] = test_dir / "test_db.sqlite"
    config.save()

    database.connect(config["core.database"])
    database.init_models(MODELS)

    return config


@pytest.fixture
def base_cli():

    yield hyf


@pytest.fixture
def cli_new_day(monkeypatch, base_cli, cli_config, test_dir):
    monkeypatch.setattr(Config, "load", lambda: cli_config)

    yield base_cli

    Task.delete().execute()
    WorkingDay.delete().execute()


@pytest.fixture
def cli(monkeypatch, cli_new_day):
    monkeypatch.setattr(DailyTracker, "is_a_new_day", lambda _: False)

    yield cli_new_day
