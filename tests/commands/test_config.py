from hyperfocus.commands.config import ConfigCommand


def test_config_command_show_config(mocker, test_session):
    printer = mocker.patch("hyperfocus.commands.config.printer")
    test_session.config.options = {
        "foo": "bar",
        "oof": "rab",
    }

    ConfigCommand(test_session).execute(
        option=None,
        value=None,
        list_=True,
        unset=False,
    )
    printer.echo.call_args_list = [mocker.call("foo = bar"), mocker.call("oof = rab")]


def test_config_command_delete_option(mocker, test_session):
    printer = mocker.patch("hyperfocus.commands.config.printer")

    ConfigCommand(test_session).execute(
        option="foobar",
        value=None,
        list_=False,
        unset=True,
    )

    test_session.config.__delitem__.assert_called_once_with("foobar")
    test_session.config.save.assert_called_once()
    printer.success.assert_called_once_with("Config updated", event="success")


def test_config_command_edit_option(mocker, test_session):
    printer = mocker.patch("hyperfocus.commands.config.printer")

    ConfigCommand(test_session).execute(
        option="foobar",
        value="test",
        list_=False,
        unset=False,
    )

    test_session.config.__setitem__.assert_called_once_with("foobar", "test")
    test_session.config.save.assert_called_once()
    printer.success.assert_called_once_with("Config updated", event="success")
