import datetime
import re
import shutil
from pathlib import Path

import pytest

from hyperfocus.config.config import Config
from hyperfocus.database import _Database, database
from hyperfocus.database.models import MODELS
from hyperfocus.services import DailyTrackerService, PastTrackerService
from hyperfocus.session import Session


TEST_DIR = Path(__file__).parent.resolve()
FIXTURES_DIR = TEST_DIR / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture(scope="session")
def test_dir(tmpdir_factory):
    yield Path(tmpdir_factory.mktemp("hyperfocus"))


@pytest.fixture(autouse=True)
def clean_test_dir(test_dir):
    shutil.rmtree(test_dir)
    test_dir.mkdir()


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


class PytestRegex:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.findall(actual))

    def __repr__(self):
        return self._regex.pattern


pytest_regex = PytestRegex


@pytest.fixture
def test_database(test_dir):
    db_path = test_dir / "test_db.sqlite"
    database.connect(db_path)
    database.init_models(MODELS)
    yield
    database.close()
    db_path.unlink()


@pytest.fixture
def test_session(mocker):
    class MockSession(Session):
        _database = mocker.Mock(spec=_Database, instance=True)

        def __init__(self):
            self._config = mocker.MagicMock(spec=Config, instance=True)
            self._database.connect(self._config)
            self._date = datetime.datetime(2022, 1, 1)
            self._callback_commands = []

    return MockSession()
