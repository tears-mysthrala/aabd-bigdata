"""Regressions for owner-only lab files and truthful NotebookLM uploads.

Use synthetic credentials in temporary directories and a fake CLI. These
tests never read existing credentials or contact NotebookLM.
"""

import contextlib
import importlib.util
import io
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
PREPARE = ROOT / "07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/preparar_lab.py"
UPLOAD = ROOT / "00_Transversal/notebooklm/SUBIR_NOVEDADES_2026-09-30.sh"
SPEC = importlib.util.spec_from_file_location("lab_prepare", PREPARE)
LAB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAB)


class LabCredentialTests(unittest.TestCase):
    def test_files_are_private_at_creation_with_permissive_umask(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            previous_mask = os.umask(0)
            try:
                with (
                    patch.object(LAB.os, "getuid", return_value=1000),
                    patch.object(LAB.secrets, "token_hex", return_value="synthetic"),
                    contextlib.redirect_stdout(io.StringIO()) as output,
                ):
                    LAB.prepare_credentials(root)
                    for file in (root / ".env", root / "private/mysql.properties"):
                        self.assertEqual(stat.S_IMODE(file.stat().st_mode), 0o600)
                    self.assertEqual(
                        stat.S_IMODE((root / "private").stat().st_mode), 0o700
                    )
                    self.assertNotIn("synthetic", output.getvalue())
                    with patch.object(LAB.secrets, "token_hex") as generate:
                        LAB.prepare_credentials(root)
                        generate.assert_not_called()
            finally:
                os.umask(previous_mask)

    def test_exclusive_creation_preserves_existing_files_and_symlink_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.write_text("synthetic fixture")
            link = root / "link"
            link.symlink_to(target)
            dangling = root / "dangling"
            dangling.symlink_to(root / "missing")
            for path in (target, link, dangling):
                with self.subTest(path=path.name), self.assertRaises(FileExistsError):
                    LAB.write_private_file(path, "replacement fixture")
            self.assertEqual(target.read_text(), "synthetic fixture")
            self.assertFalse((root / "missing").exists())


class NotebookUploadTests(unittest.TestCase):
    def test_dry_run_publish_and_first_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / "calls"
            cli = root / "notebooklm"
            cli.write_text(
                '#!/bin/sh\nprintf "%s\\n" "$*" >> "$NOTEBOOK_TEST_LOG"\n'
                '[ "${NOTEBOOK_TEST_FAIL:-0}" = 0 ] || exit 9\n'
            )
            cli.chmod(0o700)
            env = dict(
                os.environ,
                PATH=f"{root}:/usr/bin:/bin",
                NOTEBOOK_TEST_LOG=str(log),
            )
            dry = subprocess.run(
                ["bash", str(UPLOAD)], env=env, capture_output=True, text=True
            )
            self.assertEqual(dry.returncode, 0)
            self.assertIn("DRY RUN", dry.stdout)
            self.assertFalse(log.exists())
            publish = subprocess.run(
                ["bash", str(UPLOAD), "--publish"],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(publish.returncode, 0)
            calls = log.read_text().splitlines()
            self.assertEqual(len(calls), 10)
            self.assertTrue(all(call.startswith("source add -n ") for call in calls))
            self.assertIn("10 operaciones de subida completadas", publish.stdout)
            failed = subprocess.run(
                ["bash", str(UPLOAD), "--publish"],
                env=dict(env, NOTEBOOK_TEST_FAIL="1"),
                capture_output=True,
                text=True,
            )
            self.assertEqual(failed.returncode, 9)
            self.assertEqual(len(log.read_text().splitlines()), 11)
            self.assertNotIn("OK:", failed.stdout)


if __name__ == "__main__":
    unittest.main()
