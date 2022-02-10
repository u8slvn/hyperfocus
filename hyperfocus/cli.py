from pathlib import Path
from typing import Optional

import typer

from hyperfocus import __app_name__, __version__, app, config, printer
from hyperfocus.models import Status
from hyperfocus.services import DailyTrackerService, AppService

app = app.HyperfocusTyper()


@app.command()
def init(
    db_path: str = typer.Option(
        config.DEFAULT.db_path,
        "--db-path",
        prompt=str(printer.prompt("Database location")),
    ),
):
    AppService.initialize(db_path=Path(db_path))


@app.command()
def add():
    daily_tracker = DailyTrackerService()
    title = typer.prompt(printer.prompt("Task title"), type=str)
    details = typer.prompt(
        printer.prompt("Task description (optional)"), default="", show_default=False
    )
    daily_tracker.add_task(title=title, details=details)


def _update_task(id: int, prompt_text: str, status: Status) -> None:
    daily_tracker = DailyTrackerService()
    if not id:
        daily_tracker.show_tasks(newline=True, exclude=[status])
        id = typer.prompt(printer.prompt(prompt_text), type=int)
    daily_tracker.update_task(id=id, status=status)


@app.command()
def delete(id: Optional[int] = typer.Argument(None)):
    _update_task(id=id, prompt_text="Delete task", status=Status.DELETED)


@app.command()
def done(id: Optional[int] = typer.Argument(None)):
    _update_task(id=id, prompt_text="Mark task as done", status=Status.DONE)


@app.command()
def reset(id: Optional[int] = typer.Argument(None)):
    _update_task(id=id, prompt_text="Reset task", status=Status.TODO)


@app.command()
def block(id: Optional[int] = typer.Argument(None)):
    _update_task(id=id, prompt_text="Black task", status=Status.BLOCKED)


@app.command()
def show(id: Optional[int] = typer.Argument(None)):
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


@app.callback(invoke_without_command=True, help="Show daily tasks.")
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
        daily_tracker = DailyTrackerService()
        daily_tracker.show_tasks(exclude=exclude)
