from hyperfocus.termui import printer


def test_banner(capsys):
    printer.banner("foobar")

    captured = capsys.readouterr()
    assert captured.out == "> foobar\n"


def test_config(capsys):
    config = {
        "core.database": "/database.sqlite",
        "alias.st": "status",
    }

    printer.config(config)

    expected = "core.database = /database.sqlite\n" "alias.st = status\n"
    captured = capsys.readouterr()
    assert captured.out == expected
