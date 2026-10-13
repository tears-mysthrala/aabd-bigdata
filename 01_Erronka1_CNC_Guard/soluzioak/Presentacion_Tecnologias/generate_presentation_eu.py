"""Euskarazko PPTX eta PDFa sortu, diseinu-sortzaile bera erabiliz."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASENAME = "CNC_Guard_Tecnologias_EU"

def main() -> None:
    source = HERE / "contenido.eu.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    if data.get("language") != "eu" or len(data.get("slides", [])) != 33:
        raise ValueError("Euskarazko 33 diapositibak behar dira")
    with tempfile.TemporaryDirectory(prefix="cnc-eu-") as tmp:
        folder = Path(tmp)
        shutil.copy2(HERE / "generate_presentation.py", folder / "generate_presentation.py")
        shutil.copy2(source, folder / "contenido.json")
        subprocess.run([sys.executable, str(folder / "generate_presentation.py")], check=True, cwd=folder)
        for ext in ("pptx", "pdf"):
            original = folder / f"CNC_Guard_Tecnologias.{ext}"
            if not original.is_file() or original.stat().st_size < 20000:
                raise RuntimeError(f"Ez da fitxategia sortu: {original}")
            shutil.copy2(original, HERE / f"{BASENAME}.{ext}")
    print("Euskarazko aurkezpena: 33 diapositiba, PPTX + PDF.")

if __name__ == "__main__":
    main()
