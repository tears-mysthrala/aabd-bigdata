"""Preparar archivos para Moodle y paquetes de reproducción por tarea.

Lee exclusivamente las siete carpetas enumeradas. No conecta con Moodle.
"""

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
TASKS = {
    "63638": ("63638_Interpretacion_AI4I", "Interpretación AI4I", "publicada"),
    "63320": ("63320_Regresion_Logistica", "Regresión logística", "publicada"),
    "63321": ("63321_KNN", "KNN", "publicada"),
    "63325": ("63325_Jupyter_LogReg_KNN", "Jupyter: LogReg vs KNN", "plantillas"),
    "63544": ("63544_Arbol_Decision", "Árbol de decisión", "vacía; criterio declarado"),
    "63386": ("63386_Random_Forest", "Random Forest", "vacía; criterio declarado"),
    "63380": ("63380_SVM", "SVM", "vacía; criterio declarado"),
}
ALLOW = {
    ".pdf",
    ".sh",
    ".ipynb",
    ".md",
    ".png",
    ".csv",
    ".json",
    ".ows",
    ".py",
    ".txt",
    ".tab",
    ".data",
    ".names",
    ".ttf",
}
EXCLUDED = {
    "tmp",
    "qa",
    "renders",
    "renderizados",
    "portabilidad",
    "__pycache__",
    ".pdf-deps",
    ".pytest_cache",
}
MAX_FILE_BYTES = 50_000_000


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_files(folder):
    out = []
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder)
        if any(
            (part.startswith(".") and part != ".gitignore") or part in EXCLUDED
            for part in relative.parts
        ):
            continue
        if relative.parts[0] == "verificacion" and path.name.startswith("pagina-"):
            continue
        if path.is_symlink():
            raise ValueError(f"No se admite enlace simbólico: {relative}")
        if path.is_file() and (
            path.suffix.lower() in ALLOW or path.name in {"SHA256SUMS", ".gitignore"}
        ):
            assert path.resolve().is_relative_to(folder.resolve())
            out.append(path)
    return out


def main():
    upload_root = BASE / "para_subir"
    upload_root.mkdir(exist_ok=True)
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "submitted_to_moodle": False,
        "tasks": [],
    }
    rows = []
    for identifier, (name, title, statement) in TASKS.items():
        folder = BASE / name
        assert folder.is_dir(), f"Falta carpeta: {name}"
        pdfs = sorted(folder.glob("*.pdf"))
        assert len(pdfs) == 1, f"Se espera un PDF principal en {name}: {pdfs}"
        assert (folder / "README.md").is_file()
        files = source_files(folder)
        assert pdfs[0] in files
        assert len(files) >= 4
        upload = upload_root / identifier
        upload.mkdir(exist_ok=True)
        principal = upload / pdfs[0].name
        shutil.copyfile(pdfs[0], principal)
        reproduction = upload / f"reproduccion_{identifier}.zip"
        with zipfile.ZipFile(
            reproduction, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for path in files:
                archive.write(path, arcname=str(Path(name) / path.relative_to(folder)))
        required = [principal, reproduction]
        if identifier == "63325":
            for item in [
                "iris_logreg_knn.ipynb",
                "txostena_beteta.md",
                "erabaki_mugak.png",
            ]:
                target = upload / item
                shutil.copyfile(folder / item, target)
                required.append(target)
        assert len(required) <= 20
        assert all(path.stat().st_size < MAX_FILE_BYTES for path in required)
        with zipfile.ZipFile(reproduction) as archive:
            assert archive.testzip() is None
            assert all(
                not Path(info.filename).is_absolute()
                and ".." not in Path(info.filename).parts
                for info in archive.infolist()
            )
        data = {
            "id": identifier,
            "title": title,
            "moodle_url": f"https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id={identifier}",
            "teacher_statement": statement,
            "prepared_on_assumptions": identifier in {"63544", "63386", "63380"},
            "source_folder": name,
            "source_files": [
                {
                    "path": str(path.relative_to(BASE)),
                    "bytes": path.stat().st_size,
                    "sha256": digest(path),
                }
                for path in files
            ],
            "upload_files": [
                {
                    "path": str(path.relative_to(BASE)),
                    "bytes": path.stat().st_size,
                    "sha256": digest(path),
                }
                for path in required
            ],
        }
        manifest["tasks"].append(data)
        rows.append(
            f"| {identifier}: {title} | {statement} | [{principal.name}]({identifier}/{principal.name}) | [Reproducción]({identifier}/{reproduction.name}) |"
        )
        print(
            identifier,
            title,
            len(files),
            "archivos fuente;",
            len(required),
            "archivos de entrega",
        )
    instructions = """# Archivos preparados para subir

Cada carpeta numérica corresponde a la tarea del mismo ID en Moodle. Para las prácticas Orange, el PDF es el informe principal y el ZIP conserva workflow, datos, capturas, salidas y scripts. No es necesario pegar texto en el portal.

En Jupyter, entregar el notebook `.ipynb`, el informe `.md` y la imagen `.png` juntos. El PDF permite leer el informe sin dependencias; el ZIP conserva todo el conjunto.

Árbol, Random Forest y SVM tienen introducción Moodle vacía. Los trabajos siguen la estructura académica de las otras prácticas: datos, modelo, salidas, interpretación y conclusiones. Esta es una elección razonada y declarada, sin afirmar cobertura de una rúbrica que no se publica.

AI4I es una revisión con capturas reales para la tarea de interpretación. Regresión lineal ya contaba con un informe y no se recrea en este lote. Antes de modificar una entrega existente, revisar su contenido; este programa no se conecta con Moodle ni guarda entregas.

Los formularios consultados mostraban 50 MB por archivo y máximo 20 archivos. Todos los archivos de cada carpeta respetan esos límites conservadoramente. El formato ZIP acompaña al informe para preservar rutas relativas.

| Tarea | Consigna | Informe | Paquete |
|---|---|---|---|
"""
    (upload_root / "README.md").write_text(instructions + "\n".join(rows) + "\n")
    (BASE / "entregas_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    master = BASE / "Trabajos_Moodle_2026-10-05.zip"
    with zipfile.ZipFile(
        master, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path in sorted(upload_root.rglob("*")):
            if path.is_file():
                archive.write(
                    path,
                    arcname=str(
                        Path("Trabajos_Moodle_2026-10-05")
                        / path.relative_to(upload_root)
                    ),
                )
    with zipfile.ZipFile(master) as archive:
        assert archive.testzip() is None
    print("Paquete completo:", master)


if __name__ == "__main__":
    main()
