from hyperfocus.commands.init import InitCmd
from hyperfocus.config.config import Config
from hyperfocus.database._database import Database


def test_init_command(mocker):
    printer = mocker.patch("hyperfocus.commands.init.printer")
    printer.ask.return_value = "/dummy/path/database.sqlite"
    config = mocker.MagicMock(spec=Config, instance=True)
    mocker.patch("hyperfocus.commands.init.Config", return_value=config)
    database = mocker.Mock(spec=Database, instance=True)
    mocker.patch("hyperfocus.commands.init.database", database)

    InitCmd().execute()

    config.make_directory.assert_called_once()
    config.__setitem__.assert_called_once_with(
        "core.database", "/dummy/path/database.sqlite"
    )
    config.save.assert_called_once()
    assert config.__getitem__.call_count == 2
    database.connect.assert_called_once()
    database.init_models.assert_called_once()
    assert printer.info.call_count == 2
