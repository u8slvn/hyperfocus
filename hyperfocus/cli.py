import sys
from typing import List, Optional

import click
import pyperclip

from hyperfocus import __app_name__, __version__, formatter, printer
from hyperfocus.app import Hyperfocus
from hyperfocus.config import DEFAULT_DB_PATH, Config
from hyperfocus.database import database
from hyperfocus.exceptions import TaskError
from hyperfocus.models import MODELS, Task, TaskStatus
from hyperfocus.session import Session, get_current_session


class _CLIHelper:
    def __init__(self, session: Session):
        self._session = session

    def check_task_id_or_ask(
        self, task_id: int, text: str, exclude: Optional[List[TaskStatus]] = None
    ) -> int:
        if task_id:
            return task_id

        exclude = exclude or []
        self.show_tasks(newline=True, exclude=exclude)
        return printer.ask(text, type=int)

    def show_tasks(
        self, exclude: Optional[List[TaskStatus]] = None, newline=False
    ) -> None:
        exclude = exclude or []
        tasks = self._session.daily_tracker.get_tasks(exclude=exclude)
        if not tasks:
            printer.echo("No tasks for today...")
            raise click.exceptions.Exit
        printer.tasks(tasks=tasks, newline=newline)

    def get_task(self, task_id: int) -> Task:
        task = self._session.daily_tracker.get_task(task_id=task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist", event="not found")

        return task

    def update_task(self, task_id: int, status: TaskStatus, text: str):
        task_id = self.check_task_id_or_ask(
            task_id=task_id, text=text, exclude=[status]
        )

        task = self.get_task(task_id=task_id)
        if task.status == status.value:
            printer.warning(
                text=formatter.task(task=task, show_prefix=True),
                event="no change",
            )
            raise click.exceptions.Exit

        task.status = status
        self._session.daily_tracker.update_task(task=task, status=status)
        printer.success(
            text=formatter.task(task=task, show_prefix=True),
            event="updated",
        )


@click.group(cls=Hyperfocus, help="Minimalist task manager")
@click.version_option(
    version=__version__, prog_name=__app_name__, help="show the version"
)
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    session = Session()
    session.bind_context(ctx=ctx)

    if session.is_a_new_day():
        printer.echo(f"✨ {formatter.date(date=session.date)}")
        printer.echo("✨ A new day starts, good luck!\n")


@cli.command(help="initialize hyperfocus config and database")
@click.option(
    "--db-path",
    default=DEFAULT_DB_PATH,
    prompt=formatter.prompt("Database location"),
    help="database file location",
)
def init(db_path: str):
    config = Config(db_path=db_path)
    config.make_directory()
    config.save()
    printer.info(
        text=f"Config file created successfully in {config.file_path}",
        event="init",
    )

    database.connect(db_path=config.db_path)
    database.init_models(MODELS)
    printer.info(
        text=f"Database initialized successfully in {config.db_path}",
        event="init",
    )


@cli.command(help="show current working day status")
def status():
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.show_tasks(newline=True)


@cli.command(help="add task to current working day")
@click.argument("title", metavar="<title>", type=click.STRING)
@click.option("-d", "--details", "add_details", is_flag=True, help="add task details")
def add(title: str, add_details: bool):
    session = get_current_session()

    details = printer.ask("Task details") if add_details else ""

    task = session.daily_tracker.add_task(title=title, details=details)
    printer.success(
        text=formatter.task(task=task, show_prefix=True),
        event="created",
    )


@cli.command(help="mark task as done")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def done(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(
        task_id=task_id, status=TaskStatus.DONE, text="Mark task as done"
    )


@cli.command(help="reset task as todo")
@click.argument("task_id", metavar="<id>", required=False, type=int)
def reset(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(task_id=task_id, status=TaskStatus.TODO, text="Reset task")


@cli.command(help="mark task as blocked")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def block(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(task_id=task_id, status=TaskStatus.BLOCKED, text="Block task")


@cli.command(help="delete given task")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def delete(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(task_id=task_id, status=TaskStatus.DELETED, text="Delete task")


@cli.command(help="show task details")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def show(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    task_id = helper.check_task_id_or_ask(task_id=task_id, text="Show task details")

    task = helper.get_task(task_id=task_id)
    printer.task(task=task, show_details=True, show_prefix=True)


@cli.command(help="copy task details into clipboard")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def copy(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    task_id = helper.check_task_id_or_ask(task_id=task_id, text="Copy task details")

    task = helper.get_task(task_id=task_id)
    if not task.details:
        raise TaskError(f"Task {task_id} does not have details", event="not found")

    pyperclip.copy(task.details)
    printer.success(text=f"Task {task_id} details copied to clipboard", event="copied")
