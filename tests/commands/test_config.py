import pytest

from hyperfocus.commands.config import ConfigCmd


@pytest.fixture
def printer(mocker):
    yield mocker.patch("hyperfocus.commands.config.printer")


def test_config_cmd_show_config(mocker, session, printer):
    session.config.options = {
        "foo": "bar",
        "oof": "rab",
    }

    ConfigCmd(session).execute(
        option=None,
        value=None,
        list_=True,
        unset=False,
    )
    printer.echo.call_args_list = [mocker.call("foo = bar"), mocker.call("oof = rab")]


def test_config_cmd_delete_option(session, printer):
    ConfigCmd(session).execute(
        option="foobar",
        value=None,
        list_=False,
        unset=True,
    )

    session.config.__delitem__.assert_called_once_with("foobar")
    session.config.save.assert_called_once()
    printer.success.assert_called_once_with("Config updated", event="success")


def test_config_cmd_edit_option(session, printer):
    ConfigCmd(session).execute(
        option="foobar",
        value="test",
        list_=False,
        unset=False,
    )

    session.config.__setitem__.assert_called_once_with("foobar", "test")
    session.config.save.assert_called_once()
    printer.success.assert_called_once_with("Config updated", event="success")
