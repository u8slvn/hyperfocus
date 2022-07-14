from hyperfocus.termui import printer


def test_banner(capsys):
    printer.banner("foobar")

    captured = capsys.readouterr()
    assert "foobar\n" == captured.out
