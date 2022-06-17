import sys
from pathlib import Path
from typing import List

import click

from hyperfocus import __app_name__, __version__, printer
from hyperfocus.config import Config
from hyperfocus.database import database
from hyperfocus.models import MODELS, Status, Task
from hyperfocus.services import Session

DEFAULT_DB_PATH = Path.home() / f".{__app_name__}.sqlite"


class _Helper:
    def __init__(self, session: Session):
        self._session = session

    def show_tasks(self, exclude: List[Status] = None, newline=False) -> None:
        exclude = exclude or []
        tasks = self._session.daily_tracker_service.get_tasks(exclude=exclude)
        if not tasks:
            click.echo("No tasks yet for today...")
            raise click.exceptions.Exit
        click.secho(printer.tasks(tasks=tasks, newline=newline))

    def get_task(self, id: int) -> Task:
        task = self._session.daily_tracker_service.get_task(id=id)
        if not task:
            click.secho(
                printer.notification(
                    text="Task id does not exist",
                    action="not found",
                    status=printer.NotificationStatus.ERROR,
                )
            )
            raise click.exceptions.Exit(code=1)

        return task

    def update_task(self, id: int, status: Status, prompt_text: str):
        if not id:
            self.show_tasks(newline=True, exclude=[status])
            id = click.prompt(printer.prompt(prompt_text), type=int)

        task = self.get_task(id=id)
        if task.status == status.value:
            click.secho(
                printer.notification(
                    text=printer.task(task=task, show_prefix=True),
                    action="no change",
                    status=printer.NotificationStatus.WARNING,
                )
            )
            raise click.exceptions.Exit

        task.status = status.value
        self._session.daily_tracker_service.update_task(task=task, status=status)
        click.secho(
            printer.notification(
                text=printer.task(task=task, show_prefix=True),
                action="updated",
                status=printer.NotificationStatus.SUCCESS,
            )
        )


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name=__app_name__)
@click.option("--all", is_flag=True, default=False, help="Show all tasks.")
@click.pass_context
def cli(ctx: click.Context, all: bool):
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    session = Session()
    if session.is_a_new_day():
        click.echo(f"✨ {printer.date(date=session.date)}")
        click.echo("✨ A new day starts, good luck!\n")

    ctx.ensure_object(dict)
    ctx.obj['SESSION'] = session

    if not ctx.invoked_subcommand:
        exclude = [] if all else [Status.DELETED]
        helper = _Helper(session=session)
        helper.show_tasks(exclude=exclude)


@cli.command()
@click.option(
    "--db-path",
    default=DEFAULT_DB_PATH,
    prompt=printer.prompt("Database location"),
    help='Database file location.'
)
def init(db_path: str):
    db_path = Path(db_path)
    config = Config(db_path=db_path)
    config.make_directory()
    config.save()
    click.secho(
        printer.notification(
            text=f"Config file created successfully in {config.file_path}",
            action="init",
            status=printer.NotificationStatus.INFO,
        )
    )

    database.connect(db_path=config.db_path)
    database.init_models(MODELS)
    click.secho(
        printer.notification(
            text=f"Database initialized successfully in {config.db_path}",
            action="init",
            status=printer.NotificationStatus.INFO,
        )
    )


@cli.command(help="Add a task.")
@click.pass_context
def add(ctx: click.Context):
    session = ctx.obj["SESSION"]

    title = click.prompt(printer.prompt("Task title"))
    details = click.prompt(printer.prompt(
        "Task details (optional)"),
        default="",
        show_default=False,
    )

    task = session.daily_tracker_service.add_task(title=title, details=details)
    click.secho(
        printer.notification(
            text=printer.task(task=task, show_prefix=True),
            action="created",
            status=printer.NotificationStatus.SUCCESS,
        )
    )


@cli.command()
@click.argument("id", required=False)
@click.pass_context
def done(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=Status.DONE, prompt_text="Mark task as done")


@cli.command()
@click.argument("id", required=False)
@click.pass_context
def reset(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=Status.TODO, prompt_text="Reset task")


@cli.command()
@click.argument("id", required=False)
@click.pass_context
def block(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=Status.BLOCKED, prompt_text="Black task")


@cli.command()
@click.argument("id", required=False)
@click.pass_context
def delete(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    helper.update_task(id=id, status=Status.DELETED, prompt_text="Delete task")


@cli.command()
@click.argument("id", required=False)
@click.pass_context
def show(ctx: click.Context, id: int):
    session = ctx.obj["SESSION"]
    helper = _Helper(session=session)

    if not id:
        helper.show_tasks(newline=True)
        id = click.prompt(printer.prompt("Show task details"), type=int)

    task = helper.get_task(id=id)
    click.secho(f"Task: #{id} {printer.task(task=task, show_details=True)}")
