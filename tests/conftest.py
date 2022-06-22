import re
from pathlib import Path

import click
import pytest

from hyperfocus.app import Hyperfocus
from hyperfocus.database import database
from hyperfocus.exceptions import HyperfocusException
from hyperfocus.models import MODELS
from hyperfocus.services import DailyTrackerService
from hyperfocus.session import Session

TEST_DIR = Path(__file__).parent.resolve()
FIXTURES_DIR = TEST_DIR / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture(scope="session")
def tmp_test_dir(tmpdir_factory):
    return Path(tmpdir_factory.mktemp("hyperfocus"))


@pytest.fixture(scope="session", autouse=True)
def test_db(tmp_test_dir):
    db_path = tmp_test_dir / "test_config.ini"
    database.connect(db_path=db_path)
    database.init_models(MODELS)


@pytest.fixture
def cli_session(mocker):
    mocker.patch("hyperfocus.session.Config")
    mocker.patch("hyperfocus.session.database")
    mocker.patch("hyperfocus.session.DailyTrackerService", spec=DailyTrackerService)
    session = Session()
    session.daily_tracker.new_day = False

    mocker.patch("hyperfocus.cli.Session", return_value=session)
    mocker.patch(
        "hyperfocus.session.click.get_current_context", **{"return_value.obj": session}
    )

    yield session


@pytest.fixture(scope="session")
def hyperfocus_cli():
    @click.group(cls=Hyperfocus, invoke_without_command=True)
    @click.pass_context
    def dummy_cli(ctx):
        if not ctx.invoked_subcommand:
            raise HyperfocusException("Dummy group error")

    @dummy_cli.command()
    def bar():
        raise HyperfocusException("Dummy command error", event="foo")

    return dummy_cli


class pytest_regex:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern
