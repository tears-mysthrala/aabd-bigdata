"""Contrastar fuentes, archivos de entrega y ZIP sin contactar con Moodle."""

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

from preparar_paquetes import BASE, MAX_FILE_BYTES, TASKS


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked_path(relative):
    path = Path(relative)
    assert not path.is_absolute() and ".." not in path.parts, relative
    result = BASE / path
    assert result.resolve().is_relative_to(BASE.resolve())
    assert result.is_file() and not result.is_symlink(), relative
    return result


def check_record(record):
    path = checked_path(record["path"])
    data = path.read_bytes()
    assert len(data) == record["bytes"], path
    assert digest(data) == record["sha256"], path
    return path


def check_inner_manifests(archive, folder):
    hashes_name = f"{folder}/MANIFEST_SHA256.json"
    if hashes_name in archive.namelist():
        hashes = json.loads(archive.read(hashes_name))["files"]
        for relative, expected in hashes.items():
            assert digest(archive.read(f"{folder}/{relative}")) == expected
    sums_name = f"{folder}/SHA256SUMS"
    if sums_name in archive.namelist():
        for row in archive.read(sums_name).decode().splitlines():
            expected, relative = row.split("  ", 1)
            assert digest(archive.read(f"{folder}/{relative}")) == expected


def main():
    manifest = json.loads((BASE / "entregas_manifest.json").read_text())
    assert manifest["submitted_to_moodle"] is False
    assert {task["id"] for task in manifest["tasks"]} == set(TASKS)
    assert len(manifest["tasks"]) == 7
    sources_count, pages_count, largest_upload = 0, 0, 0
    for task in manifest["tasks"]:
        folder = task["source_folder"]
        assert folder == TASKS[task["id"]][0]
        source_records = task["source_files"]
        for record in source_records:
            assert Path(record["path"]).parts[0] == folder
            check_record(record)
        sources_count += len(source_records)
        upload_records = task["upload_files"]
        assert len(upload_records) == (5 if task["id"] == "63325" else 2)
        paths = [check_record(record) for record in upload_records]
        assert set(paths) == set((BASE / "para_subir" / task["id"]).iterdir())
        assert all(path.stat().st_size < MAX_FILE_BYTES for path in paths)
        largest_upload = max(largest_upload, *(p.stat().st_size for p in paths))
        reproduction = next(path for path in paths if path.suffix == ".zip")
        with zipfile.ZipFile(reproduction) as archive:
            assert archive.testzip() is None
            assert set(archive.namelist()) == {r["path"] for r in source_records}
            for record in source_records:
                assert digest(archive.read(record["path"])) == record["sha256"]
            check_inner_manifests(archive, folder)
        pdf = next(path for path in paths if path.suffix == ".pdf")
        info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
        pages = int(
            next(
                line.split(":")[1]
                for line in info.splitlines()
                if line.startswith("Pages:")
            )
        )
        assert (
            pages
            == {
                "63638": 4,
                "63320": 5,
                "63321": 4,
                "63325": 3,
                "63544": 5,
                "63386": 5,
                "63380": 5,
            }[task["id"]]
        )
        pages_count += pages
        print(task["id"], "OK:", len(source_records), "fuentes;", pages, "páginas")
    master = BASE / "Trabajos_Moodle_2026-10-05.zip"
    files = {
        str(Path("Trabajos_Moodle_2026-10-05") / p.relative_to(BASE / "para_subir")): p
        for p in (BASE / "para_subir").rglob("*")
        if p.is_file()
    }
    with zipfile.ZipFile(master) as archive:
        assert archive.testzip() is None and set(archive.namelist()) == set(files)
        for name, path in files.items():
            assert digest(archive.read(name)) == digest(path.read_bytes())
    result = {
        "passed": True,
        "tasks": 7,
        "source_files": sources_count,
        "pdf_pages": pages_count,
        "largest_upload_bytes": largest_upload,
        "max_allowed_file_bytes": MAX_FILE_BYTES,
        "zip_roundtrip_and_inner_manifests": True,
        "master_zip_bytes": master.stat().st_size,
        "master_zip_sha256": digest(master.read_bytes()),
        "submitted_to_moodle": False,
    }
    (BASE / "verificacion_paquetes.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
