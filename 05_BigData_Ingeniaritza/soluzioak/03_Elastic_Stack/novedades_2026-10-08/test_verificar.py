"""La validación de eventos debe seguir rechazando errores con python -O."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def test_optimized_python_rejects_invalid_status(tmp_path):
    shutil.copy(ROOT / "verificar.py", tmp_path)
    shutil.copytree(ROOT / "evidencias", tmp_path / "evidencias")
    path = tmp_path / "evidencias" / "p20.stdout.log"
    lines = path.read_text().splitlines()
    for i, line in enumerate(lines):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and "status_code" in event:
            event["status_code"] = 999
            lines[i] = json.dumps(event)
            break
    else:
        raise AssertionError("Fixture sin evento HTTP")
    path.write_text("\n".join(lines) + "\n")
    result = subprocess.run(
        [sys.executable, "-O", str(tmp_path / "verificar.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "ValueError" in result.stderr and "status_code" in result.stderr
