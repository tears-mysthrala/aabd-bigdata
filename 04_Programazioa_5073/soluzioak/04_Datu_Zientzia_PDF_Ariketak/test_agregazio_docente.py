"""Regresión de 2.4: sumar grupos antes de buscar el máximo."""

import ast
import contextlib
import io
import unittest
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def cargar_funcion_existente():
    # Evita importar el script completo: importa ejecuta benchmark, gráficos y DVC.
    tree = ast.parse((HERE / "5073_2_Datu_Zientzia_PDF_Ariketak.py").read_text())
    node = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "ariketa_2_4"
    )
    namespace = {
        "pd": pd,
        "SALMENTA_TAULA": pd.DataFrame(
            {
                "hiria": ["A", "A", "B"],
                "kategoria": ["X", "X", "Y"],
                "produktua": ["p1", "p2", "p3"],
                "salmenta": [60, 60, 100],
            }
        ),
    }
    exec(  # noqa: S102 - solo AST de función local versionada; evita efectos al importar.
        compile(ast.Module(body=[node], type_ignores=[]), str(HERE), "exec"), namespace
    )
    return namespace["ariketa_2_4"], namespace["SALMENTA_TAULA"]


class AgregazioRegression(unittest.TestCase):
    def test_grupo_supera_la_fila_individual_en_funcion_existente(self):
        func, fixture = cargar_funcion_existente()
        with contextlib.redirect_stdout(io.StringIO()):
            # La función original usa SALMENTA_TAULA; la corregida permite inyección.
            result = func(fixture) if func.__code__.co_argcount else func()
        self.assertEqual(result["bikote_max"], ("A", "X"))
        self.assertEqual(result["balio_max"], 120)
        self.assertEqual(result["pivot"].loc["A", "X"], 120)

    def test_csv_docente_max_grupo_distinto_de_max_fila(self):
        from ariketa_2_4_2_5_docente import agregatu_salmentak

        with contextlib.redirect_stdout(io.StringIO()):
            result = agregatu_salmentak()
        self.assertEqual(result["rows"], 30)
        self.assertEqual(result["bikote_max"], ("Gasteiz", "Janaria"))
        self.assertEqual(result["balio_max"], 1417)
        self.assertEqual(result["max_individual"]["hiria"], "Donostia")
        self.assertEqual(result["max_individual"]["salmenta"], 456)
        self.assertNotEqual(result["balio_max"], result["max_individual"]["salmenta"])
        self.assertNotIn("GUZTIRA", result["bikote_max"])

    def test_amaia_se_conserva_en_left_y_concat_conserva_sus_ventas(self):
        from ariketa_2_4_2_5_docente import batu_taulak, egiaztatu_csv_2_5

        with contextlib.redirect_stdout(io.StringIO()):
            result = batu_taulak()
        self.assertEqual(result["inner"].shape, (4, 6))
        self.assertEqual(result["left"].shape, (5, 6))
        self.assertNotIn("Amaia", result["inner"]["izena"].tolist())
        amaia = result["left"].set_index("izena").loc["Amaia"]
        self.assertTrue(pd.isna(amaia["hiri_izena"]))
        self.assertEqual(len(result["concat"]), 6)
        self.assertEqual(result["concat"]["salmenta"].sum(), 705)
        invalid = egiaztatu_csv_2_5()
        self.assertTrue(all(not row["schema_valid"] for row in invalid))
        self.assertEqual(invalid[0]["sha256"], invalid[1]["sha256"])


if __name__ == "__main__":
    unittest.main()
