import re
from pathlib import Path

import pytest

from hyperfocus.database import database
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
    daily_tracker_service = mocker.create_autospec(spec=DailyTrackerService)
    session = mocker.create_autospec(spec=Session)
    session.daily_tracker = daily_tracker_service
    session.is_a_new_day.return_value = False
    mocker.patch("hyperfocus.cli.Session", return_value=session)

    yield session


class pytest_regex:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern
