"""Comprueba trazabilidad y estructura; no sustituye la revisión docente.

Desde la raíz: python 00_Transversal/MOCK_EXAMS_2026-10/comprobar.py
Solo lee archivos locales. No modifica fuentes, ejecuta ejercicios ni usa red.
"""

import ast
import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check():
    manifest = json.loads((HERE / "manifest.json").read_text())
    require(len(manifest) == 7, "Se esperan siete modelos")
    documents = set(HERE.glob("*.md"))
    source_paths = set()
    section_count = 0
    block_count = 0
    for model in manifest:
        exam = ROOT / model["exam"]
        solution = ROOT / model["solution"]
        exam_text = exam.read_text()
        solution_text = solution.read_text()
        documents.update([exam, solution])
        sources = set(model["sources"])
        require(sources == set(model["source_sha256"]), "Fuentes y hashes no coinciden")
        for source in sources:
            path = ROOT / source
            require(
                "Mock_Exams_2026-10" not in source, "Fuente circular de un simulacro"
            )
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            require(
                actual == model["source_sha256"][source],
                f"Fuente cambiada: {source}. Revisar el temario antes de renovar su hash.",
            )
            source_paths.add(source)
        sections = model["sections"]
        section_ids = [row["id"] for row in sections]
        is_programming = model["folder"] == "04_Programazioa_5073"
        expected = (
            [f"T{i}" for i in range(1, 31)] + [f"P{i}" for i in range(1, 5)]
            if is_programming
            else [str(i) for i in range(1, 6)]
        )
        require(section_ids == expected, f"Apartados sin trazar: {model['folder']}")
        referenced = set()
        for row in sections:
            require(row["references"], f"Sin fuente: {model['folder']}/{row['id']}")
            for reference in row["references"]:
                require(reference["location"].strip(), "Falta el pasaje docente")
                require(reference["source"] in sources, "Referencia sin hash de fuente")
                referenced.add(reference["source"])
        require(
            referenced == sources, "Hay fuentes listadas sin un apartado que las use"
        )
        section_count += len(sections)
        for doc in [exam, solution]:
            blocks = re.findall(r"```python\n(.*?)```", doc.read_text(), re.DOTALL)
            ast.parse("\n\n".join(blocks), filename=str(doc.relative_to(ROOT)))
            block_count += len(blocks)
        if is_programming:
            questions = re.findall(
                r"^\*\*(\d+)\..*?\*\*\n\n((?:- [ABCD]\) .*\n){4})",
                exam_text,
                re.MULTILINE,
            )
            require(
                [int(n) for n, _ in questions] == list(range(1, 31)), "Test incompleto"
            )
            for _, options in questions:
                require(
                    re.findall(r"^- ([ABCD])\)", options, re.MULTILINE) == list("ABCD"),
                    "Opciones inválidas",
                )
            answers = re.findall(
                r"^\| (\d+) \| ([ABCD]) \|", solution_text, re.MULTILINE
            )
            require(
                [int(n) for n, _ in answers] == list(range(1, 31)), "Clave incompleta"
            )
            require(
                Counter(key for _, key in answers) == {"A": 8, "B": 8, "C": 7, "D": 7},
                "Clave desequilibrada",
            )
            points_minutes = re.findall(
                r"^### P\d\..*?\(([\d.]+) puntos; (\d+) min\)", exam_text, re.MULTILINE
            )
            require(
                sum(float(p) for p, _ in points_minutes) == 7,
                "Práctica distinta de 7 puntos",
            )
            require(
                sum(int(m) for _, m in points_minutes) == 115,
                "Tiempo de práctica incoherente",
            )
        else:
            points_minutes = re.findall(
                r"^## \d\..*?\(([\d.]+) puntos?; (\d+) min\)", exam_text, re.MULTILINE
            )
            require(len(points_minutes) == 5, "Faltan puntos o tiempos")
            require(
                sum(float(p) for p, _ in points_minutes) == 10, "Puntos distintos de 10"
            )
            require(
                sum(int(m) for _, m in points_minutes) == model["minutes"],
                "Duración incoherente",
            )

    data = ROOT / "04_Programazioa_5073/data/mock_exams_2026_10"
    documents.add(data / "README.md")
    with (data / "refrigeracion.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    unique = {tuple(row.values()) for row in rows}
    clean = []
    for row in unique:
        _, _, temperature, power, label = row
        t, p, y = float(temperature or "nan"), float(power or "nan"), float(label)
        if (
            math.isfinite(t)
            and -30 <= t <= 15
            and math.isfinite(p)
            and 0 <= p <= 6000
            and y in {0, 1}
        ):
            clean.append(row)
    require(
        (len(rows), len(unique), len(clean)) == (322, 320, 308),
        "CSV o reglas cambiados",
    )
    require(sum(float(row[-1]) == 1 for row in clean) == 32, "Etiquetas cambiadas")

    link_count = 0
    for document in sorted(documents):
        for target in re.findall(
            r"\[[^\]]+\]\((<[^>]+>|[^\s)]+)\)", document.read_text()
        ):
            target = target.strip("<>")
            if target.startswith(("https://", "http://", "#")):
                continue
            path = document.parent / unquote(target.split("#", 1)[0])
            require(
                path.exists(), f"Enlace roto: {document.relative_to(ROOT)} → {target}"
            )
            link_count += 1
    print(
        json.dumps(
            {
                "models": 7,
                "sections": section_count,
                "sources": len(source_paths),
                "local_links": link_count,
                "python_blocks_parsed": block_count,
                "csv_rows": len(rows),
                "csv_clean": len(clean),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    check()
