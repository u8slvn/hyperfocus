import datetime

import pytest

from hyperfocus.config.config import Config
from hyperfocus.database._database import _Database
from hyperfocus.session import Session


@pytest.fixture
def test_session(mocker):
    class MockSession(Session):
        _database = mocker.Mock(spec=_Database, instance=True)

        def __init__(self):
            self._config = mocker.MagicMock(spec=Config, instance=True)
            self._database.connect(self._config)
            self._date = datetime.datetime(2022, 1, 1)

    return MockSession()
