"""Testak: agurtu() + --izena (ariketa 4.4, feature branch)."""

from agur import agurtu, main


def test_agurtu_basico():
    assert agurtu("Ane") == "Kaixo, Ane!"


def test_agurtu_strip():
    assert agurtu("  Ane  ") == "Kaixo, Ane!"


def test_agurtu_hutsik():
    try:
        agurtu("   ")
    except ValueError:
        return
    raise AssertionError("hutsik egon behar luke ValueError")


def test_main_arg_izena(capsys):
    main(["--izena", "Mikel"])
    assert capsys.readouterr().out.strip() == "Kaixo, Mikel!"
