#!/usr/bin/env python3
"""Prepare official MinIO sidecar outside Git; never starts Docker or NiFi."""
from __future__ import annotations

import argparse
import hashlib
import os
import secrets
import urllib.request
from pathlib import Path

RELEASE = "RELEASE.2025-09-07T16-13-09Z"
SOURCE = f"https://github.com/minio/minio/releases/download/{RELEASE}/minio.linux-amd64.{RELEASE}"
SHA256 = "7c5bd8512c6e966455b1d198209358b2d191c77a83ab377c4073281065fb855f"
TEMPLATES = Path(__file__).resolve().parent
PROJECT_ROOT = TEMPLATES.parents[3]


def prepare(runtime_dir: Path) -> None:
    runtime_dir = runtime_dir.expanduser().resolve()
    if runtime_dir.is_relative_to(PROJECT_ROOT):
        raise ValueError("Runtime credentials and binary must be outside the repository")
    runtime_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(runtime_dir, 0o700)
    build_dir = runtime_dir / "minio-build"
    build_dir.mkdir(mode=0o700, exist_ok=True)
    binary = build_dir / "minio"
    if not binary.exists():
        # Download data over verified HTTPS, then verify before execution/build.
        urllib.request.urlretrieve(SOURCE, binary)
    actual = hashlib.sha256(binary.read_bytes()).hexdigest()
    if actual != SHA256:
        raise ValueError("Official MinIO artifact SHA-256 mismatch; do not build or execute")
    binary.chmod(0o755)
    credentials = runtime_dir / "minio.env"
    if credentials.exists():
        if credentials.stat().st_mode & 0o077:
            raise ValueError("Existing minio.env permissions must be private (600)")
        names = {line.split("=", 1)[0] for line in credentials.read_text().splitlines()}
        if not {"MINIO_ROOT_USER", "MINIO_ROOT_PASSWORD"}.issubset(names):
            raise ValueError("Existing minio.env does not contain required LAB credential fields")
    else:
        fd = os.open(credentials, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as handle:
            handle.write("MINIO_ROOT_USER=lab7-" + secrets.token_hex(6) + "\n")
            handle.write("MINIO_ROOT_PASSWORD=" + secrets.token_urlsafe(32) + "\n")
    (runtime_dir / "minio-data").mkdir(mode=0o700, exist_ok=True)
    (build_dir / "Dockerfile.minio").write_text((TEMPLATES / "Dockerfile.minio").read_text())
    compose = runtime_dir / "compose-minio-generated.yml"
    compose.write_text((TEMPLATES / "compose.minio.yml").read_text())
    print(f"Verified official MinIO {RELEASE}; SHA-256 {actual}")
    print(f"Private LAB credentials: {credentials} (not displayed)")
    print(f"Sidecar recipe prepared: {compose}; Docker and NiFi have not been started")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-dir", type=Path,
                        default=Path("/tmp/bigdata-nifi-lab-20261002"))
    args = parser.parse_args()
    prepare(args.runtime_dir)
