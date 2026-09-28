"""OAuth de lectura para los cuadernos privados enlazados desde Moodle."""

from __future__ import annotations

import argparse
import json
import os
import stat
import tempfile
from pathlib import Path

SCOPE = "https://www.googleapis.com/auth/drive.readonly"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TOKEN = Path.home() / ".local/share/aabd-moodle-sync/google-drive-token.json"


def private_path(path: Path, *, existing: bool) -> Path:
    """Mantener credenciales fuera de Git y sin acceso de otros usuarios."""
    path = path.expanduser()
    if path.is_symlink():
        raise ValueError("El archivo OAuth no puede ser un enlace simbólico")
    path = path.resolve()
    if path.is_relative_to(REPO_ROOT):
        raise ValueError("Guarda las credenciales OAuth fuera del repositorio")
    if existing or path.exists():
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid():
            raise ValueError("El archivo OAuth debe ser un archivo propio")
        if stat.S_IMODE(info.st_mode) & 0o077:
            raise ValueError("El archivo OAuth necesita permisos 600")
    return path


def token_path() -> Path:
    return Path(os.environ.get("GOOGLE_DRIVE_TOKEN_FILE", str(DEFAULT_TOKEN)))


def authenticated_session():
    """No iniciar login interactivo desde el servicio; renovar OAuth si existe."""
    path = token_path()
    if not path.exists() and "GOOGLE_DRIVE_TOKEN_FILE" not in os.environ:
        return None
    path = private_path(path, existing=True)
    from google.auth.transport.requests import AuthorizedSession, Request
    from google.oauth2.credentials import Credentials

    info = json.loads(path.read_text())
    if (
        not isinstance(info, dict)
        or info.get("token_uri") != "https://oauth2.googleapis.com/token"
    ):
        raise ValueError("El token OAuth debe usar el endpoint oficial de Google")
    if set(info.get("scopes", [])) != {SCOPE}:
        raise ValueError("Autoriza de nuevo con el único scope drive.readonly")
    credentials = Credentials.from_authorized_user_info(info, scopes=[SCOPE])
    if not credentials.valid:
        try:
            credentials.refresh(Request())
        except Exception:
            raise RuntimeError(
                "No se pudo renovar Google OAuth; vuelve a autorizar la cuenta del centro"
            ) from None
    return AuthorizedSession(credentials)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--client", required=True, type=Path, help="JSON OAuth de tipo Desktop app"
    )
    parser.add_argument(
        "--token",
        type=Path,
        default=token_path(),
        help="Archivo privado de autorización",
    )
    args = parser.parse_args()
    client = private_path(args.client, existing=True)
    target = private_path(args.token, existing=False)
    from google_auth_oauthlib.flow import InstalledAppFlow

    config = json.loads(client.read_text())
    installed = config.get("installed", {})
    if (
        installed.get("auth_uri") != "https://accounts.google.com/o/oauth2/auth"
        or installed.get("token_uri") != "https://oauth2.googleapis.com/token"
    ):
        raise ValueError(
            "Se necesita un cliente Desktop app con endpoints oficiales de Google"
        )
    flow = InstalledAppFlow.from_client_config(
        config, [SCOPE], autogenerate_code_verifier=True
    )
    try:
        credentials = flow.run_local_server(
            host="127.0.0.1",
            port=0,
            timeout_seconds=180,
            prompt="consent select_account",
            access_type="offline",
            authorization_prompt_message="Autoriza con la cuenta del centro en el navegador:\n{url}",
            success_message="Autorización recibida. Puedes cerrar esta pestaña.",
        )
    except Exception:
        raise RuntimeError(
            "No se completó la autorización de Google; comprueba la cuenta y la política del centro"
        ) from None
    if not credentials.refresh_token:
        raise ValueError("Google no entregó autorización renovable; vuelve a autorizar")
    if credentials.granted_scopes is not None and set(credentials.granted_scopes) != {
        SCOPE
    }:
        raise ValueError("Google no concedió el scope drive.readonly solicitado")
    target.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=target.parent, delete=False
        ) as output:
            temporary = Path(output.name)
            os.chmod(temporary, 0o600)
            output.write(credentials.to_json())
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f"Autorización de lectura guardada en {target}; no compartas este archivo.")


if __name__ == "__main__":
    main()
