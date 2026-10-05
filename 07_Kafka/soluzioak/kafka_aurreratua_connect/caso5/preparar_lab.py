#!/usr/bin/env python3
"""Prepare fresh lab-only credentials; preserve existing credentials and volumes."""

import os
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent
env_path = ROOT / ".env"
private_dir = ROOT / "private"
credential_path = private_dir / "mysql.properties"
if os.getuid() != 1000:
    raise SystemExit(
        "This bind-mount recipe expects host UID 1000 (image appuser UID). Adapt ownership before using it on another host."
    )
if env_path.exists() or credential_path.exists():
    if not (env_path.is_file() and credential_path.is_file()):
        raise SystemExit(
            "Partial credentials exist: inspect them locally; nothing overwritten."
        )
    print("Existing lab credentials preserved. No data or volumes changed.")
else:
    private_dir.mkdir(mode=0o700, exist_ok=True)
    password = secrets.token_hex(20)
    root_password = secrets.token_hex(20)
    # Host UID 1000 equals the image appuser UID; no broad host read permissions.
    # Values never enter the build context.
    os.chmod(private_dir, 0o700)
    env_path.write_text(
        f"MYSQL_ROOT_PASSWORD={root_password}\nMYSQL_PASSWORD={password}\n"
    )
    os.chmod(env_path, 0o600)
    credential_path.write_text(f"password={password}\n")
    os.chmod(credential_path, 0o600)
    print("Local lab credentials created in ignored files. Values not printed.")
