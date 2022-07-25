import pytest
from freezegun import freeze_time

from hyperfocus.config.config import Config
from hyperfocus.console.commands.main import hyf
from hyperfocus.database import database
from hyperfocus.database.models import MODELS
from hyperfocus.services import DailyTracker


@pytest.fixture(scope="session")
def cli_config(test_dir):
    config = Config()
    config._dir = test_dir
    config["core.database"] = test_dir / "test_db.sqlite"
    config.save()

    database.connect(config["core.database"])
    database.init_models(MODELS)

    return config


@pytest.fixture
def cli_new_day(monkeypatch, cli_config):
    monkeypatch.setattr(Config, "load", lambda: cli_config)

    with freeze_time("2022-01-01"):
        yield hyf

    for model in MODELS:
        model.delete().execute()


@pytest.fixture
def cli(monkeypatch, cli_new_day):
    monkeypatch.setattr(DailyTracker, "is_a_new_day", lambda _: False)

    yield cli_new_day
