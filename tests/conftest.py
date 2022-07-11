import datetime
import re
import shutil
from pathlib import Path

import pytest

from hyperfocus.config.config import Config
from hyperfocus.database import database
from hyperfocus.database._database import _Database
from hyperfocus.database.models import MODELS
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


class PytestRegex:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.findall(actual))

    def __repr__(self):
        return self._regex.pattern


pytest_regex = PytestRegex


@pytest.fixture
def test_database(mocker, test_dir):
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
