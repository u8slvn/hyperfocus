import pytest
from peewee import Model, OperationalError

from hyperfocus.database import _Database
from hyperfocus.exceptions import DatabaseError
from hyperfocus.models import db_error_handler, wrap_methods


def test_database_with_models(tmp_test_dir):
    test_db_path = tmp_test_dir / "testw_db.sqlite"
    test_db_path.touch()
    db_test = _Database()

    class TestModel(Model):
        class Meta:
            database = db_test()

    models = [TestModel]
    db_test.connect(db_path=test_db_path)
    db_test.init_models(models)

    core_db_test = db_test()
    assert core_db_test.get_tables() == ["testmodel"]
    db_test.close()
    assert core_db_test.close() is False


@pytest.mark.parametrize(
    "exception, expected",
    [
        (OperationalError("no such table dummy"), DatabaseError),
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
