import click
from click.testing import CliRunner

from hyperfocus.console.core.group import DefaultCommandGroup


runner = CliRunner()


def test_group_command_return_command_without_checking_for_alias(hyf_group):
    result = runner.invoke(hyf_group, ["alias"])

    assert result.output == "alias\n"


def test_group_command_handle_alias(mocker, hyf_group):
    config = {"alias.foo": "alias"}
    mocker.patch("hyperfocus.console.core.group.Config.load", return_value=config)

    result = runner.invoke(hyf_group, ["foo"])

    assert result.output == "alias\n"


@click.group(cls=DefaultCommandGroup)
def default_command_group():
    ...


@default_command_group.command(default_command=True)
@click.argument("arg")
def foo(arg):
    click.echo(arg)


@default_command_group.command()
@click.argument("arg")
def bar(arg):
    click.echo(arg)


def test_default_command_group_without_args():
    result = runner.invoke(default_command_group)

    assert result.exit_code == 0
    assert result.output == (
        "Usage: default-command-group [OPTIONS] COMMAND [ARGS]...\n"
        "\n"
        "Options:\n"
        "  --help  Show this message and exit.\n"
        "\n"
        "Commands:\n"
        "  bar\n"
        "  foo\n"
    )


def test_default_command_group_with_default_command_arg():
    result = runner.invoke(default_command_group, ["hello"])

    assert result.exit_code == 0
    assert result.output == "hello\n"


def test_default_command_group_default_command():
    result = runner.invoke(default_command_group, ["foo", "hello"])

    assert result.exit_code == 0
    assert result.output == "hello\n"


def test_default_command_group_non_default_command():
    result = runner.invoke(default_command_group, ["bar", "hello"])

    assert result.exit_code == 0
    assert result.output == "hello\n"
