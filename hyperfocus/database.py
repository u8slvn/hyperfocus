from pathlib import Path
from typing import List

from peewee import Model, SqliteDatabase

from hyperfocus.exceptions import DatabaseDoesNotExists


class _Database:
    """Handle database session."""
    def __init__(self):
        self._database = SqliteDatabase(None)

    def __call__(self):
        """Return the raw peewee db."""
        return self._database

    def connect(self, db_path: Path):
        """Connect to database."""
        self._database.init(db_path, pragmas={"foreign_keys": 1})

    def init_models(self, models: List[Model]):
        """Initialize database with a list of model."""
        with self._database:
            self._database.create_tables(models=models)


database = _Database()
