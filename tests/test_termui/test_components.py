import datetime

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import icons, printer
from hyperfocus.termui.components import NewDay, ProgressBar, TasksTable


def test_tasks_table(capsys):
    tasks = [
        Task(id=1, title="foo"),
        Task(id=1, title="bar", details="hello"),
    ]
    printer.echo(TasksTable(tasks))

    expected = (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        "  1   ⬢ foo      □     \n"
        "  1   ⬢ bar      ■     \n"
        "\n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected


def test_progress_bar(capsys):
    tasks = [
        Task(title="foo"),
        Task(title="bar", status=TaskStatus.DONE),
    ]

    printer.echo(ProgressBar(tasks))

    expected = (
        f" {icons.TASK_STATUS} 50% [{icons.PROGRESSBAR * 15}"
        f"{icons.PROGRESSBAR_EMPTY * 15}]\n\n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected


def test_new_day(capsys):
    date = datetime.date(2022, 1, 1)

    printer.echo(NewDay(date))

    expected = f"> {icons.NEW_DAY} Sat, 01 January 2022: A new day starts, good luck!\n"
    captured = capsys.readouterr()
    assert captured.out == expected
