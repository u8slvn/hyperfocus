from pathlib import Path
from typing import Optional

import typer
from services import DailyTrackerService, Session

from hyperfocus import __app_name__, __version__, app, printer
from hyperfocus.config import Config, ConfigInitializer
from hyperfocus.database import database
from hyperfocus.models import MODELS, Status

hyperfocus_app = app.HyperfocusTyper()


@hyperfocus_app.command()
def init(
    db_path: str = typer.Option(
        hyperfocus_app.default_db_path,
        "--db-path",
        prompt=str(printer.prompt("Database location")),
    ),
):
    config = Config(db_path=Path(db_path))
    config_initializer = ConfigInitializer(config=config)
    config_initializer.make_directory()
    config_initializer.create_database_file()
    config.save()
    typer.secho(
        printer.notification(
            text=f"Config file created successfully in {config.file_path}",
            action="init",
            status=printer.NotificationStatus.INFO,
        )
    )

    database.connect(db_path=config.db_path)
    database.init_models(MODELS)
    typer.secho(
        printer.notification(
            text=f"Database initialized successfully in {config.db_path}",
            action="init",
            status=printer.NotificationStatus.INFO,
        )
    )


@hyperfocus_app.command()
def add():
    session = Session()
    title = typer.prompt(printer.prompt("Task title"), type=str)
    details = typer.prompt(
        printer.prompt("Task description (optional)"), default="", show_default=False
    )
    task = session.daily_tracker.create_task(title=title, details=details)
    typer.secho(
        printer.notification(
            text=printer.task(task=task, show_prefix=True),
            action="created",
            status=printer.NotificationStatus.SUCCESS,
        )
    )


def _update_task(id: int, prompt_text: str, status: Status) -> None:
    config = Config.load()
    database.connect(db_path=config.db_path)
    daily_tracker = DailyTrackerService()
    if not id:
        daily_tracker.show_tasks(newline=True, exclude=[status])
        id = typer.prompt(printer.prompt(prompt_text), type=int)
    daily_tracker.update_task(id=id, status=status)


@hyperfocus_app.command()
def delete(id: int = typer.Argument(None)):
    _update_task(id=id, prompt_text="Delete task", status=Status.DELETED)


@hyperfocus_app.command()
def done(id: int = typer.Argument(None)):
    _update_task(id=id, prompt_text="Mark task as done", status=Status.DONE)


@hyperfocus_app.command()
def reset(id: int = typer.Argument(None)):
    _update_task(id=id, prompt_text="Reset task", status=Status.TODO)


@hyperfocus_app.command()
def block(id: int = typer.Argument(None)):
    _update_task(id=id, prompt_text="Black task", status=Status.BLOCKED)


@hyperfocus_app.command()
def show(id: int = typer.Argument(None)):
    config = Config.load()
    database.connect(db_path=config.db_path)
    daily_tracker = DailyTrackerService()
    if not id:
        daily_tracker.show_tasks(newline=True)
        id = typer.prompt(printer.prompt("Show task details"), type=int)
    daily_tracker.show_task(id=id)


def _version_callback(value: bool):
    if not value:
        return
    typer.echo(f"{__app_name__} version {__version__}")
    raise typer.Exit()


@hyperfocus_app.callback(invoke_without_command=True, help="Show daily tasks.")
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Print the Hyperfocus version.",
        callback=_version_callback,
        is_eager=True,
    ),
    all: Optional[bool] = typer.Option(
        None,
        "--all",
        help="Show all tasks.",
    ),
):
    if ctx.invoked_subcommand is None:
        exclude = [] if all else [Status.DELETED]
        config = Config.load()
        database.connect(db_path=config.db_path)
        daily_tracker = DailyTrackerService()
        daily_tracker.show_tasks(exclude=exclude)
