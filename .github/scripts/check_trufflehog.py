"""Accept only four reviewed false positives from two immutable commits.

The Box match is base64 PNG data in the COMPAS notebook. Both JDBC matches
are Docker lab URLs without passwords; credentials come from private files.
The fourth occurrence is the same password-free URL in the regression fixture.
Exceptions bind the detector, decoder, path, commit, line and raw-value hash.
Verified findings, unexpected verification errors and changed occurrences fail.
Never print raw findings: scanner reports may contain credentials.
"""

import hashlib
import json
import sys
from pathlib import Path

REVIEWED_COMMIT = "ddcf210c80073bd84e4a9cf266624db4913065a9"
REVIEWED = {
    (
        REVIEWED_COMMIT,
        "Box",
        "02_AA_Ereduak_5071/soluzioak/COMPAS/COMPAS_reconciliado.ipynb",
        792,
        "c399bd9e311dd3d84f2846b51c224f8d5518c7a4a075a924f89d42e98bb14b67",
    ),
    (
        REVIEWED_COMMIT,
        "JDBC",
        "06_NiFi/soluzioak/scripts/nifi_lab_verificar.py",
        126,
        "043c0a46083815638940040f372a20ea8db3f232d459a27c7216de3096a4773c",
    ),
    (
        REVIEWED_COMMIT,
        "JDBC",
        "07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/config/mysql-source.properties",
        4,
        "4561e769512448225d1975cd8d09f9fb32fa92fc368b3a284ec64177b2419867",
    ),
    (
        "be33a08ead48786ae376f505dc6dd1660b6eab2f",
        "JDBC",
        ".github/scripts/test_check_trufflehog.py",
        19,
        "043c0a46083815638940040f372a20ea8db3f232d459a27c7216de3096a4773c",
    ),
}


def reviewed_false_positive(finding: dict) -> bool:
    source = finding["SourceMetadata"]["Data"]["Git"]
    fingerprint = (
        source["commit"],
        finding["DetectorName"],
        source["file"],
        source["line"],
        hashlib.sha256(finding["Raw"].encode()).hexdigest(),
    )
    return (
        finding["Verified"] is False
        and (
            not finding.get("VerificationError")
            or (
                finding["DetectorName"] == "JDBC"
                and finding.get("VerificationError")
                == "missing host or password in connection string"
            )
        )
        and not finding.get("RawV2")
        and finding["DecoderName"] == "PLAIN"
        and fingerprint in REVIEWED
    )


def check_report(report: Path, scan_exit: int) -> int:
    if scan_exit not in (0, 183):
        print(f"TruffleHog scan failed (exit {scan_exit}).")
        return 1
    accepted = blocked = 0
    try:
        for line in report.read_text().splitlines():
            if not line.strip():
                continue
            if reviewed_false_positive(json.loads(line)):
                accepted += 1
            else:
                blocked += 1
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        print("Invalid or incomplete TruffleHog report.")
        return 1
    if scan_exit == 183 and accepted + blocked == 0:
        print("TruffleHog reported findings but the report is empty.")
        return 1
    print(
        f"TruffleHog: {accepted} reviewed false positives; {blocked} blocked findings."
    )
    return int(blocked > 0)


if __name__ == "__main__":
    raise SystemExit(check_report(Path(sys.argv[1]), int(sys.argv[2])))
