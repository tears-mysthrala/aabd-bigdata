"""Egitura-egiaztapena; ez ditu deskargak edo kanpoko zerbitzuak exekutatzen."""
import importlib

MOD = "5073_3_Frameworkak_PDF_Ariketak"
ESPEROTAKOAK = [
    "1.1", "1.2", "1.4", "1.5", "1.6",
    "2.1", "2.2", "2.3", "2.4",
    "3.1", "3.2", "3.3", "3.4", "3.5",
    "4.1", "4.2", "4.4",
    "5.1", "5.2", "5.3", "5.4",
    "6.1", "6.2", "6.3", "6.4",
    "7.1",
]


def test_zerrenda_osoa():
    mod = importlib.import_module(MOD)
    assert mod.ARIKETA_ZERRENDA == ESPEROTAKOAK, mod.ARIKETA_ZERRENDA


def test_ariketa_guztiak():
    mod = importlib.import_module(MOD)
    for gid in ESPEROTAKOAK:
        fn = getattr(mod, f"ariketa_{gid.replace('.', '_')}", None)
        assert callable(fn), f"falta ariketa_{gid}"


if __name__ == "__main__":
    test_zerrenda_osoa()
    test_ariketa_guztiak()
    print(f"{len(ESPEROTAKOAK)} ariketa-sarrera (1.3/4.3 PDFan ez daude)")
