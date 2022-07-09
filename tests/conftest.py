import re
import shutil
from pathlib import Path

import click
import pytest

from hyperfocus.database import database
from hyperfocus.exceptions import HyperfocusException
from hyperfocus.hyf_click import HyfGroup
from hyperfocus.models import MODELS
from hyperfocus.services import DailyTrackerService, PastTrackerService
from hyperfocus.session import Session


TEST_DIR = Path(__file__).parent.resolve()
FIXTURES_DIR = TEST_DIR / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture(scope="session")
def test_dir(tmpdir_factory):
    return Path(tmpdir_factory.mktemp("hyperfocus"))


@pytest.fixture(autouse=True)
def clean_test_dir(test_dir):
    shutil.rmtree(test_dir)
    test_dir.mkdir()


@pytest.fixture
def test_db(test_dir):
    db_path = test_dir / "test_db.sqlite"
    database.connect(db_path)
    database.init_models(MODELS)
    yield
    database.close()
    db_path.unlink()


@pytest.fixture
def cli_session(mocker):
    mocker.patch("hyperfocus.session.Config")
    mocker.patch("hyperfocus.session.database")
    daily_tracker = mocker.Mock(spec=DailyTrackerService)
    mocker.patch(
        "hyperfocus.session.DailyTrackerService.today", return_value=daily_tracker
    )
    mocker.patch("hyperfocus.session.PastTrackerService", spec=PastTrackerService)
    session = Session()
    session.daily_tracker.new_day = False

    mocker.patch("hyperfocus.cli.Session", return_value=session)
    mocker.patch(
        "hyperfocus.session.click.get_current_context", **{"return_value.obj": session}
    )

    yield session


@pytest.fixture(scope="session")
def hyperfocus_cli():
    @click.group(cls=HyfGroup, invoke_without_command=True)
    @click.pass_context
    def hyperfocus_cli(ctx):
        if not ctx.invoked_subcommand:
            raise HyperfocusException("Dummy group error")

    @hyperfocus_cli.command()
    def bar():
        raise HyperfocusException("Dummy command error", event="foo")

    @hyperfocus_cli.command()
    def alias():
        click.echo("alias")

    return hyperfocus_cli


class PytestRegex:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.findall(actual))

    def __repr__(self):
        return self._regex.pattern


pytest_regex = PytestRegex
