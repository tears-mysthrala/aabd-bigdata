#!/usr/bin/env python3
"""Prepare fresh lab-only credentials; preserve existing credentials and volumes."""

import os
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def write_private_file(path: Path, content: str) -> None:
    """Create owner-only runtime input without overwriting files or symlinks."""
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as output:
        output.write(content)


def prepare_credentials(root: Path = ROOT) -> None:
    env_path = root / ".env"
    private_dir = root / "private"
    credential_path = private_dir / "mysql.properties"
    if os.getuid() != 1000:
        raise SystemExit(
            "This bind-mount recipe expects host UID 1000 (image appuser UID). Adapt ownership before using it on another host."
        )
    if env_path.exists() or credential_path.exists():
        if not (
            env_path.is_file()
            and credential_path.is_file()
            and not env_path.is_symlink()
            and not credential_path.is_symlink()
        ):
            raise SystemExit(
                "Partial or symlinked credentials exist: inspect locally; nothing overwritten."
            )
        print("Existing lab credentials preserved. No data or volumes changed.")
        return
    if private_dir.is_symlink():
        raise SystemExit("Private credential directory must not be a symlink.")
    private_dir.mkdir(mode=0o700, exist_ok=True)
    password = secrets.token_hex(20)
    root_password = secrets.token_hex(20)
    # Host UID 1000 equals the image appuser UID; no broad host read permissions.
    # Values never enter the build context.
    os.chmod(private_dir, 0o700)
    write_private_file(
        env_path, f"MYSQL_ROOT_PASSWORD={root_password}\nMYSQL_PASSWORD={password}\n"
    )
    write_private_file(credential_path, f"password={password}\n")
    print("Local lab credentials created in ignored files. Values not printed.")


if __name__ == "__main__":
    prepare_credentials()
