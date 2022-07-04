from pathlib import Path
from typing import List

from peewee import Model, SqliteDatabase


class _Database:
    def __init__(self):
        self._engine = SqliteDatabase(None)

    def __call__(self):
        return self._engine

    def connect(self, db_path: Path):
        self._engine.init(db_path, pragmas={"foreign_keys": 1})

    def init_models(self, models: List[Model]):
        with self._engine:
            self._engine.create_tables(models=models)


database = _Database()
