from pathlib import Path

from hyperfocus.commands import HyperfocusCommand, printer
from hyperfocus.config.config import Config
from hyperfocus.database import database
from hyperfocus.database.models import MODELS


class InitCommand(HyperfocusCommand):
    def execute(self, db_path: str):
        config = self.create_config(db_path=db_path)
        self.init_database(config=config)

    @staticmethod
    def create_config(db_path: str) -> Config:
        config = Config()
        config.make_directory()
        config["core.database"] = str(Path(db_path).resolve())
        config.save()
        printer.info(
            text=f"Config file created successfully in {config.config_file.path}",
            event="init",
        )

        return config

    @staticmethod
    def init_database(config: Config) -> None:
        database.connect(config["core.database"])
        database.init_models(MODELS)
        printer.info(
            text=f"Database initialized successfully in {config['core.database']}",
            event="init",
        )
