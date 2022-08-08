import click

from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter, printer, prompt
from hyperfocus.termui.components import SuccessNotification


@click.command(help="Add task to current working day")
@click.argument("title", metavar="<title>", type=click.STRING)
@click.option("-d", "--details", "add_details", is_flag=True, help="add task details")
def add(title: str, add_details: bool) -> None:
    session = get_current_session()

    details = prompt.prompt("Task details") if add_details else ""

    task = session.daily_tracker.create_task(title=title, details=details)
    printer.echo(
        SuccessNotification(
            text=f"{formatter.task(task=task, show_prefix=True)} created",
        )
    )
