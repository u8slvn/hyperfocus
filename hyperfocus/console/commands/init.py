import click

from hyperfocus.config.config import Config
from hyperfocus.database import database
from hyperfocus.database.models import MODELS
from hyperfocus.locations import DEFAULT_DB_PATH
from hyperfocus.termui import printer, prompt
from hyperfocus.termui.components import InfoNotification


@click.command(help="Initialize hyperfocus config and database")
def init() -> None:
    db_path = prompt.prompt("Database location", default=str(DEFAULT_DB_PATH))

    config = Config()
    config.make_directory()
    config["core.database"] = db_path
    config.save()

    printer.echo(
        InfoNotification(
            text=f"Config file created successfully in {config.config_file.path}",
        )
    )

    database.connect(config["core.database"])
    database.init_models(MODELS)
    printer.echo(
        InfoNotification(
            text=f"Database initialized successfully in {config['core.database']}",
        )
    )
