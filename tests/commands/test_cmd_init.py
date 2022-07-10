from hyperfocus.commands.cmd_init import InitCommand
from hyperfocus.config.config import Config
from hyperfocus.database._database import _Database


def test_init_command(mocker):
    create_config = mocker.patch(
        "hyperfocus.commands.cmd_init.InitCommand.create_config",
        return_value=mocker.sentinel.config,
    )
    init_database = mocker.patch(
        "hyperfocus.commands.cmd_init.InitCommand.init_database"
    )

    InitCommand().execute(db_path="/dummy/path/database.sqlite")

    create_config.assert_called_once_with(db_path="/dummy/path/database.sqlite")
    init_database.assert_called_once_with(config=mocker.sentinel.config)


def test_init_command_create_config(mocker):
    printer = mocker.patch("hyperfocus.commands.cmd_init.printer")
    config = mocker.MagicMock(spec=Config, instance=True)
    mocker.patch("hyperfocus.commands.cmd_init.Config", return_value=config)

    returned_config = InitCommand.create_config(db_path="/dummy/path/database.sqlite")

    assert returned_config == config
    config.make_directory.assert_called_once()
    config.__setitem__.assert_called_once_with(
        "core.database", "/dummy/path/database.sqlite"
    )
    config.save.assert_called_once()
    printer.info.assert_called_once()


def test_init_command_init_database(mocker):
    printer = mocker.patch("hyperfocus.commands.cmd_init.printer")
    config = mocker.MagicMock(spec=Config, instance=True)
    database = mocker.Mock(spec=_Database, instance=True)
    mocker.patch("hyperfocus.commands.cmd_init.database", database)

    InitCommand.init_database(config=config)

    assert config.__getitem__.call_count == 2
    database.connect.assert_called_once()
    database.init_models.assert_called_once()
    printer.info.assert_called_once()
