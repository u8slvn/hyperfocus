import sys
from pathlib import Path
from typing import List

import click

from hyperfocus import __app_name__, __version__
from hyperfocus.config import Config
from hyperfocus.database import database
from hyperfocus.display import Formatter, NotificationStatus, Printer
from hyperfocus.models import MODELS, Task, TaskStatus
from hyperfocus.session import Session

DEFAULT_DB_PATH = Path.home() / f".{__app_name__}.sqlite"


class _Helper:
    def __init__(self, session: Session):
        self._session = session

    def show_tasks(self, exclude: List[TaskStatus] = None, newline=False) -> None:
        exclude = exclude or []
        tasks = self._session.daily_tracker.get_tasks(exclude=exclude)
        if not tasks:
            click.echo("No tasks yet for today...")
            raise click.exceptions.Exit
        Printer.tasks(tasks=tasks, newline=newline)

    def get_task(self, id: int) -> Task:
        task = self._session.daily_tracker.get_task(id=id)
        if not task:
            Printer.notification(
                text=f"Task {id} does not exist",
                action="not found",
                status=NotificationStatus.ERROR,
            )
            raise click.exceptions.Exit(code=1)

        return task

    def update_task(self, id: int, status: TaskStatus, prompt_text: str):
        if not id:
            self.show_tasks(newline=True, exclude=[status])
            id = click.prompt(Formatter.prompt(prompt_text), type=int)

        task = self.get_task(id=id)
        if task.status == status.value:
            Printer.notification(
                text=Formatter.task(task=task, show_prefix=True),
                action="no change",
                status=NotificationStatus.WARNING,
            )
            raise click.exceptions.Exit

        task.status = status
        self._session.daily_tracker.update_task(task=task, status=status)
        Printer.notification(
            text=Formatter.task(task=task, show_prefix=True),
            action="updated",
            status=NotificationStatus.SUCCESS,
        )


@click.group(invoke_without_command=True, help="Show all the tasks for the day.")
@click.version_option(
    version=__version__, prog_name=__app_name__, help="Show the version."
)
@click.option(
    "--all", is_flag=True, default=False, help="Show all tasks even the deleted ones."
)
@click.pass_context
def cli(ctx: click.Context, all: bool):
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    ctx.ensure_object(dict)
    session = Session()
    ctx.obj["SESSION"] = session

    if session.is_a_new_day():
        Printer.echo(f"✨ {Formatter.date(date=session.date)}")
        Printer.echo("✨ A new day starts, good luck!\n")

    if not ctx.invoked_subcommand:
        helper = _Helper(session=session)
        exclude = [] if all else [TaskStatus.DELETED]
        helper.show_tasks(exclude=exclude)


@cli.command(help="Initialize hyperfocus config and database.")
@click.option(
    "--db-path",
    default=DEFAULT_DB_PATH,
    prompt=Formatter.prompt("Database location"),
    help="Database file location.",
)
def init(db_path: str):
    db_path = Path(db_path)
    config = Config(db_path=db_path)
    config.make_directory()
    config.save()
    Printer.notification(
        text=f"Config file created successfully in {config.file_path}",
        action="init",
        status=NotificationStatus.INFO,
    )

    database.connect(db_path=config.db_path)
    database.init_models(MODELS)
    Printer.notification(
        text=f"Database initialized successfully in {config.db_path}",
        action="init",
        status=NotificationStatus.INFO,
    )


@cli.command(help="Add a today task.")
@click.pass_context
def add(ctx: click.Context):
    session = ctx.obj["SESSION"]

    title = click.prompt(Formatter.prompt("Task title"))
    details = click.prompt(
        Formatter.prompt("Task details (optional)"),
        default="",
        show_default=False,
    )

    task = session.daily_tracker.add_task(title=title, details=details)
    Printer.notification(
        text=Formatter.task(task=task, show_prefix=True),
        action="created",
        status=NotificationStatus.SUCCESS,
    )


@cli.command(help="Mark a task as done.")
@click.argument("id", required=False)
@click.pass_context
def done(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=TaskStatus.DONE, prompt_text="Mark task as done")


@cli.command(help="Restore a task at initial status.")
@click.argument("id", required=False)
@click.pass_context
def reset(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=TaskStatus.TODO, prompt_text="Reset task")


@cli.command(help="Mark a task as block.")
@click.argument("id", required=False)
@click.pass_context
def block(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=TaskStatus.BLOCKED, prompt_text="Black task")


@cli.command(help="Mark a task as deleted (Deleted tasks won't appear in the list).")
@click.argument("id", required=False)
@click.pass_context
def delete(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=TaskStatus.DELETED, prompt_text="Delete task")


@cli.command(help="Show the details of a task.")
@click.argument("id", required=False)
@click.pass_context
def show(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    if not id:
        helper.show_tasks(newline=True)
        id = click.prompt(Formatter.prompt("Show task details"), type=int)

    task = helper.get_task(id=id)
    Printer.task(task=task, show_details=True, show_prefix=True)
