from __future__ import annotations

from typing import Type

from peewee import Model, SqliteDatabase


class _Database:
    def __init__(self) -> None:
        self._engine = SqliteDatabase(None)

    def __call__(self) -> SqliteDatabase:
        return self._engine

    def connect(self, file: str) -> None:
        self._engine.init(file, pragmas={"foreign_keys": 1})

    def init_models(self, models: list[Type[Model]]) -> None:
        with self._engine:
            self._engine.create_tables(models=models)

    def close(self) -> None:
        self._engine.close()
