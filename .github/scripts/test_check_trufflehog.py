"""Negative regression checks for the narrowly scoped secret-scan exceptions."""

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

from check_trufflehog import REVIEWED_COMMIT, check_report, reviewed_false_positive


def fixture():
    return {
        "DetectorName": "JDBC",
        "DecoderName": "PLAIN",
        "Verified": False,
        "Raw": "jdbc:mysql://mysql:3306/retail_db",
        "SourceMetadata": {
            "Data": {
                "Git": {
                    "commit": REVIEWED_COMMIT,
                    "file": "06_NiFi/soluzioak/scripts/nifi_lab_verificar.py",
                    "line": 126,
                }
            }
        },
    }


class SecretScanGateTests(unittest.TestCase):
    def test_reviewed_jdbc_url_without_password_is_accepted(self):
        self.assertTrue(reviewed_false_positive(fixture()))
        finding = fixture()
        finding["VerificationError"] = "missing host or password in connection string"
        self.assertTrue(reviewed_false_positive(finding))

    def test_changes_and_verified_credentials_are_never_accepted(self):
        original = fixture()
        for key, value in (
            ("Verified", True),
            ("VerificationError", "timeout"),
            ("Raw", original["Raw"] + "?password=synthetic-test-password"),
            ("RawV2", "synthetic-test-password"),
            ("DetectorName", "Box"),
            ("DecoderName", "BASE64"),
        ):
            with self.subTest(field=key):
                finding = copy.deepcopy(original)
                finding[key] = value
                self.assertFalse(reviewed_false_positive(finding))
        for key, value in (
            ("commit", "a" * 40),
            ("file", "unreviewed.py"),
            ("line", 127),
        ):
            with self.subTest(source_field=key):
                finding = copy.deepcopy(original)
                finding["SourceMetadata"]["Data"]["Git"][key] = value
                self.assertFalse(reviewed_false_positive(finding))

    def test_reports_fail_closed_without_printing_raw_values(self):
        blocked = fixture()
        blocked["Raw"] = "synthetic-private-value"
        cases = [
            (json.dumps(fixture()), 183, 0),
            (json.dumps(blocked), 183, 1),
            (json.dumps(fixture()) + "\n" + json.dumps(blocked), 183, 1),
            ("", 0, 0),
            ("", 183, 1),
            ("", 1, 1),
            ("not JSON", 0, 1),
            ("{}", 0, 1),
        ]
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.jsonl"
            for content, exit_code, expected in cases:
                with self.subTest(exit_code=exit_code, expected=expected):
                    report.write_text(content)
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        self.assertEqual(check_report(report, exit_code), expected)
                    self.assertNotIn("synthetic-private-value", output.getvalue())


if __name__ == "__main__":
    unittest.main()
