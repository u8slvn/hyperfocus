import pytest
from peewee import OperationalError

from hyperfocus.database import database
from hyperfocus.exceptions import DatabaseError, DatabaseNotinitializedError
from hyperfocus.models import MODELS, db_error_handler, wrap_methods


def test_database_with_models(tmp_test_dir):
    test_db_path = tmp_test_dir / "test_db.sqlite"
    test_db_path.touch()

    database.connect(db_path=test_db_path)
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
