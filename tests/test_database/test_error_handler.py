from __future__ import annotations

import peewee
import pytest

from hyperfocus.database.error_handler import db_error_handler
from hyperfocus.database.exceptions import DatabaseError
from hyperfocus.utils import wrap_methods


@pytest.mark.parametrize(
    "exception, expected",
    [
        (peewee.OperationalError("no such table dummy"), DatabaseError),
        (peewee.DatabaseError(), DatabaseError),
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
