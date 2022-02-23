from typing import List

from peewee import Model, SqliteDatabase

from hyperfocus.config import Config
from hyperfocus.exceptions import DatabaseDoesNotExists


class _Database:
    def __init__(self):
        self._database = SqliteDatabase(None)

    def __call__(self):
        return self._database

    def connect(self, config: Config):
        if not config.db_path.exists():
            raise DatabaseDoesNotExists()
        self._database.init(config.db_path, pragmas={"foreign_keys": 1})

    def init_models(self, models: List[Model]):
        with self._database:
            self._database.create_tables(models=models)


database = _Database()
