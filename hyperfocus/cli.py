import sys
from typing import List

import click

from hyperfocus import __app_name__, __version__, formatter, printer
from hyperfocus.app import Hyperfocus
from hyperfocus.config import DEFAULT_DB_PATH, Config
from hyperfocus.database import database
from hyperfocus.exceptions import TaskError
from hyperfocus.models import MODELS, Task, TaskEvents, TaskStatus
from hyperfocus.session import Session, get_current_session


class _CLIHelper:
    def __init__(self, session: Session):
        self._session = session

    def show_tasks(self, exclude: List[TaskStatus] = None, newline=False) -> None:
        exclude = exclude or []
        tasks = self._session.daily_tracker.get_tasks(exclude=exclude)
        if not tasks:
            printer.echo("No tasks for today...")
            raise click.exceptions.Exit
        printer.tasks(tasks=tasks, newline=newline)

    def get_task(self, id: int) -> Task:
        task = self._session.daily_tracker.get_task(id=id)
        if not task:
            raise TaskError(f"Task {id} does not exist", event="not found")

        return task

    def update_task(self, id: int, status: TaskStatus, prompt_text: str):
        if not id:
            self.show_tasks(newline=True, exclude=[status])
            id = printer.ask(prompt_text, type=int)

        task = self.get_task(id=id)
        if task.status == status.value:
            printer.warning(
                text=formatter.task(task=task, show_prefix=True),
                event=TaskEvents.NO_CHANGE,
            )
            raise click.exceptions.Exit

        task.status = status
        self._session.daily_tracker.update_task(task=task, status=status)
        printer.success(
            text=formatter.task(task=task, show_prefix=True),
            event=TaskEvents.UPDATED,
        )


@click.group(
    cls=Hyperfocus, invoke_without_command=True, help="Show all the tasks for the day."
)
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

    session = Session()
    session.bind_context(ctx=ctx)

    if session.is_a_new_day():
        printer.echo(f"✨ {formatter.date(date=session.date)}")
        printer.echo("✨ A new day starts, good luck!\n")

    if not ctx.invoked_subcommand:
        helper = _CLIHelper(session=session)
        exclude = [] if all else [TaskStatus.DELETED]
        helper.show_tasks(exclude=exclude)


@cli.command(help="Initialize hyperfocus config and database.")
@click.option(
    "--db-path",
    default=DEFAULT_DB_PATH,
    prompt=formatter.prompt("Database location"),
    help="Database file location.",
)
def init(db_path: str):
    config = Config(db_path=db_path)
    config.make_directory()
    config.save()
    printer.info(
        text=f"Config file created successfully in {config.file_path}",
        event=TaskEvents.INIT,
    )

    database.connect(db_path=config.db_path)
    database.init_models(MODELS)
    printer.info(
        text=f"Database initialized successfully in {config.db_path}",
        event=TaskEvents.INIT,
    )


@cli.command(help="Add a today task.")
def add():
    session = get_current_session()

    title = printer.ask("Task title")
    details = printer.ask("Task details (optional)", default="", show_default=False)

    task = session.daily_tracker.add_task(title=title, details=details)
    printer.success(
        text=formatter.task(task=task, show_prefix=True),
        event=TaskEvents.CREATED,
    )


@cli.command(help="Mark a task as done.")
@click.argument("id", required=False)
def done(id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(id=id, status=TaskStatus.DONE, prompt_text="Mark task as done")


@cli.command(help="Restore a task at initial status.")
@click.argument("id", required=False)
def reset(id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(id=id, status=TaskStatus.TODO, prompt_text="Reset task")


@cli.command(help="Mark a task as block.")
@click.argument("id", required=False)
def block(id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(id=id, status=TaskStatus.BLOCKED, prompt_text="Black task")


@cli.command(help="Mark a task as deleted (Deleted tasks won't appear in the list).")
@click.argument("id", required=False)
def delete(id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(id=id, status=TaskStatus.DELETED, prompt_text="Delete task")


@cli.command(help="Show the details of a task.")
@click.argument("id", required=False)
def show(id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    if not id:
        helper.show_tasks(newline=True)
        id = printer.ask("Show task details", type=int)

    task = helper.get_task(id=id)
    printer.task(task=task, show_details=True, show_prefix=True)
