import click
from click.testing import CliRunner

from hyperfocus.termui import prompt


runner = CliRunner()


@click.group()
def prompt_cli():
    ...


@prompt_cli.command()
def foo():
    click.echo(prompt.confirm("Foo"))
    click.echo(prompt.confirm("Foo", default=True))
    click.echo(prompt.confirm("Foo", default=False))


@prompt_cli.command()
def bar():
    click.echo(prompt.prompt("Bar"))
    click.echo(prompt.prompt("Bar", default="baz"))


def test_confirm():
    result = runner.invoke(prompt_cli, "foo", input="y\n\n\n")

    assert result.exit_code == 0
    assert result.output == (
        "? Foo [y/n]: y\n"
        "True\n"
        "? Foo [Y/n]: \n"
        "True\n"
        "? Foo [y/N]: \n"
        "False\n"
    )


def test_prompt():
    result = runner.invoke(prompt_cli, "bar", input="foobar\n\n")

    assert result.exit_code == 0
    assert result.output == ("? Bar: foobar\n" "foobar\n" "? Bar [baz]: \n" "baz\n")
