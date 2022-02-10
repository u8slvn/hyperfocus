import pytest
from peewee import OperationalError

from hyperfocus.config import Config
from hyperfocus.database import database
from hyperfocus.exceptions import (
    DatabaseNotExists,
    DatabaseError,
    DatabaseNotinitializedError,
)
from hyperfocus.models import MODELS, db_error_handler, wrap_methods


def test_database_connect_fails_if_sqlite_file_does_not_exist(tmp_test_dir):
    test_db_path = tmp_test_dir / "dont_exist_db"
    config = Config(db_path=test_db_path)

    with pytest.raises(DatabaseNotExists):
        database.connect(config=config)


def test_database_with_models(tmp_test_dir):
    test_db_path = tmp_test_dir / "test_db.sqlite"
    test_db_path.touch()
    config = Config(db_path=test_db_path)

    database.connect(config=config)
    database.init_models(MODELS)

    core_test_db = database()
    assert core_test_db.get_tables() == ["dailytracker", "tasks"]


@pytest.mark.parametrize(
    "exception, expected",
    [
        (OperationalError("no such table dummy"), DatabaseNotinitializedError),
        (OperationalError(), DatabaseError),
    ],
)
def test_db_error_handler(exception, expected):
    @wrap_methods(db_error_handler, ["save"])
    class DummyModel:
        def save(self):
            raise exception

    dummy = DummyModel()
    with pytest.raises(expected):
        dummy.save()
