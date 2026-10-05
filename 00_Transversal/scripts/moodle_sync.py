#!/usr/bin/env python3
"""Moodle fitxategien sinkronizazio automatikoa.

Orduro exekutatzen da (systemd timer bidez):
1. Moodle-ra konektatzen da eta saioa hasten du.
2. Atal guztiak aztertzen ditu (fitxategiak, karpetak, zereginak).
3. Aldaketak edo fitxategi berriak badaude, deskargatu eta dagokion karpetan jartzen ditu.
4. .docx fitxategiak .md formatura bihurtzen ditu.
5. Material egiaztatua berrikuspen-adar batean argitaratzen du.
6. Mahaigaineko jakinarazpena bidaltzen du (notify-send).
"""

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
from collections import Counter
from datetime import datetime
from email.message import Message
from pathlib import Path
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

REPO_ROOT = Path("/home/tears/bigdata")
LOG_FILE = REPO_ROOT / "moodle_sync.log"

USERNAME = os.environ.get("MOODLE_USER", "")
PASSWORD = os.environ.get("MOODLE_PASS", "")
BASE_URL = "https://elearning20.hezkuntza.net/012053"
COURSE_ID = "535"
MAX_DOWNLOAD_BYTES = 100 * 1024 * 1024


def redact_sensitive(text: str) -> str:
    for value in (USERNAME, PASSWORD):
        if value:
            text = text.replace(value, "[redacted]")
    return text


def log(msg: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] {redact_sensitive(msg)}"
    print(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def notify(title: str, msg: str) -> None:
    try:
        subprocess.run(["notify-send", "-a", "Moodle Sync", title, redact_sensitive(msg)], check=False)
    except Exception as e:
        log(f"Ezin izan da notify-send exekutatu: {e}")


class MoodleAuthenticationRejected(RuntimeError):
    """El servidor rechaza la autenticación; repetir puede bloquear la cuenta."""


def check_login_rejection(message: str) -> None:
    """Clasificar mensajes conocidos sin escribir el texto recibido ni secretos."""
    normalized = " ".join(message.casefold().split())
    if any(text in normalized for text in (
        "account is locked", "cuenta está bloqueada", "kontua blokeatuta",
    )):
        raise MoodleAuthenticationRejected(
            "Cuenta Moodle bloqueada: requiere desbloqueo humano; no se reintenta"
        )
    if any(text in normalized for text in (
        "invalid login", "nombre de usuario o contraseña incorrectos",
    )):
        raise MoodleAuthenticationRejected(
            "Moodle rechaza el login: comprobar acceso configurado; no se reintenta"
        )


def lortu_saioa() -> requests.Session:
    """Chromium bidez saioa hasi eta cookies-ak eskuratu."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        cdp_port = os.environ.get("MOODLE_BROWSER_CDP_PORT")
        if cdp_port:
            port = int(cdp_port)
            if not 1 <= port <= 65535:
                raise ValueError("Puerto CDP local inválido")
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
            # Uso manual autorizado de la sesión existente. Solo cookies de
            # Moodle, en memoria: no se exportan ni se cierra su navegador.
            cookies = browser.contexts[0].cookies(BASE_URL)
        else:
            if not USERNAME or not PASSWORD:
                raise SystemExit("Falta MOODLE_USER/MOODLE_PASS en el entorno (nunca en código).")
            browser = p.chromium.launch(
                executable_path="/usr/bin/chromium",
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            page = browser.new_page()
            page.goto(f"{BASE_URL}/login/index.php")
            page.fill("#username", USERNAME)
            page.fill("#password", PASSWORD)
            page.click("#loginbtn")
            page.wait_for_load_state("networkidle")
            try:
                message = " ".join(page.locator(
                    ".loginerrors, .alert-danger, #loginerrormessage"
                ).all_text_contents())
                check_login_rejection(message)
                cookies = page.context.cookies(BASE_URL)
            finally:
                browser.close()

    session = requests.Session()
    for c in cookies:
        session.cookies.set(c["name"], c["value"], domain=c["domain"], path=c["path"])

    # Verificar autenticación real: sin sesión válida Moodle devuelve el
    # formulario de login (HTTP 200) y el escaneo vería 0 actividades,
    # informando "sin novedades" en falso. Fallar ruidoso en ese caso.
    probe = moodle_request(session, "GET", f"{BASE_URL}/course/view.php?id={COURSE_ID}", timeout=15)
    probe.raise_for_status()
    if 'id="username"' in probe.text or "login/index.php" in probe.url:
        raise RuntimeError("Login Moodle fallido: sesión autenticada no confirmada")
    return session


def docx_to_md(docx_path: Path, md_path: Path) -> None:
    """Bihurtu docx testu aberatsa markdown garbi batera."""
    temp_path = None
    try:
        md_path = safe_download_path(md_path.parent, md_path.name)
        import docx

        with ZipFile(docx_path) as archive:
            if sum(part.file_size for part in archive.infolist()) > MAX_DOWNLOAD_BYTES:
                raise ValueError("DOCX deskonprimatuak tamaina-muga gainditzen du")
        doc = docx.Document(docx_path)
        lines = []
        for p in doc.paragraphs:
            txt = p.text.strip()
            if not txt:
                continue
            if p.style.name.startswith("Heading 1"):
                lines.append(f"# {txt}\n")
            elif p.style.name.startswith("Heading 2"):
                lines.append(f"## {txt}\n")
            elif p.style.name.startswith("Heading 3"):
                lines.append(f"### {txt}\n")
            else:
                lines.append(f"{txt}\n")
        for t in doc.tables:
            for row in t.rows:
                row_txt = [c.text.strip().replace("\n", " ") for c in row.cells]
                lines.append("| " + " | ".join(row_txt) + " |\n")
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=md_path.parent, delete=False
        ) as output:
            temp_path = Path(output.name)
            output.write("\n".join(lines))
        os.replace(temp_path, md_path)
        log(f"Bihurtuta: {docx_path.name} -> {md_path.name}")
    except Exception as e:
        log(f"Errorea docx bihurtzean ({docx_path}): {e}")
        raise
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def helburu_direktorioa(sec_id: int, izena: str, karpeta_izena: str = "") -> Path:
    """Zehaztu fitxategiaren helburu-karpeta atal eta fitxategi-izenaren arabera."""
    izena_lower = izena.lower()
    
    # 1. Karpeta espezifikoak
    if "mock datuak" in karpeta_izena.lower():
        return REPO_ROOT / "04_Programazioa_5073" / "data" / "mock_datuak"
    if "alborapenak" in karpeta_izena.lower():
        return REPO_ROOT / "02_AA_Ereduak_5071" / "materialak" / "Alborapenak"

    # 2. Atalen araberako sailkapena
    if sec_id in (0, 1):
        return REPO_ROOT / "00_Transversal" / "materialak_00_Orokorra"
    elif sec_id in (2, 3):
        return REPO_ROOT / "01_Erronka1_CNC_Guard" / "materialak"
    elif sec_id == 4:
        return REPO_ROOT / "02_AA_Ereduak_5071" / "materialak"
    elif sec_id == 5:
        return REPO_ROOT / "03_ML_5072" / "materialak"
    elif sec_id == 6:
        return REPO_ROOT / "04_Programazioa_5073" / "materialak"
    elif sec_id == 7:
        return REPO_ROOT / "05_BigData_Ingeniaritza" / "materialak"
    elif sec_id == 8:
        if "kafka" in izena_lower or "01_03" in izena_lower:
            return REPO_ROOT / "07_Kafka" / "materialak"
        return REPO_ROOT / "06_NiFi" / "materialak"
    elif sec_id == 9:
        return REPO_ROOT / "08_Erronka2_RetailEUS" / "materialak"
    elif sec_id == 10:
        return REPO_ROOT / "00_Transversal" / "azterketak"
    else:
        return REPO_ROOT / "materialak"


def safe_download_path(dest_dir: Path, remote_name: str, *, nested: bool = False) -> Path:
    """Baliozkotu urruneko izena idatzi aurretik, baita symlinkak ere."""
    name = urllib.parse.unquote(remote_name).replace("\\", "/")
    parts = name.split("/")
    if (not name or name.startswith("/") or re.match(r"^[A-Za-z]:", name)
            or any(part in ("", ".", "..", ".git") for part in parts)
            or (not nested and len(parts) != 1)):
        raise ValueError(f"Moodle izen ez-segurua: {remote_name!r}")
    root = REPO_ROOT.resolve()
    base = dest_dir.resolve()
    candidate = (base / name).resolve()
    if (not base.is_relative_to(root) or not candidate.is_relative_to(root)
            or ".git" in candidate.relative_to(root).parts):
        raise ValueError("Moodle deskarga-bidea baimendutako direktoriotik kanpo")
    return candidate


def moodle_request(
    session: requests.Session, method: str, url: str,
    allowed_hosts: set[str] | None = None, *, stop_at_external: bool = False, **kwargs
) -> requests.Response:
    """Jarraitu soilik baimendutako HTTPS hostetako birbideratzeei."""
    current = urllib.parse.urljoin(BASE_URL + "/", url)
    hosts = allowed_hosts or {urllib.parse.urlparse(BASE_URL).hostname}
    for _ in range(6):
        parsed = urllib.parse.urlparse(current)
        if parsed.scheme != "https" or parsed.hostname not in hosts or parsed.username or parsed.password:
            raise ValueError("Deskarga esteka/birbideratzea baimendutako hostetik kanpo")
        for attempt in range(3):
            try:
                response = session.request(method, current, allow_redirects=False, **kwargs)
                break
            except (requests.ConnectionError, requests.Timeout):
                if attempt == 2:
                    raise
                time.sleep(attempt + 1)
        if response.status_code not in (301, 302, 303, 307, 308):
            return response
        location = response.headers.get("Location")
        if not location:
            response.close()
            raise ValueError("Moodle birbideratzeak ez du Location goibururik")
        target = urllib.parse.urljoin(current, location)
        parsed_target = urllib.parse.urlparse(target)
        if stop_at_external and (parsed_target.scheme != "https" or parsed_target.hostname not in hosts):
            return response
        response.close()
        current = target
    raise ValueError("Moodle birbideratze gehiegi")


def download_file(
    session: requests.Session, url: str, dest_path: Path,
    *, allowed_hosts: set[str] | None = None, notebook: bool = False
) -> bool:
    """Deskargatu muga batekin eta ordezkatu fitxategia deskarga osoa denean."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with moodle_request(
            session, "GET", url, allowed_hosts=allowed_hosts, stream=True, timeout=(10, 30)
        ) as response:
            response.raise_for_status()
            html_content = "text/html" in response.headers.get("Content-Type", "")
            if html_content and (dest_path.suffix.lower() not in (".html", ".htm")
                                 or "pluginfile.php" not in urllib.parse.urlparse(response.url).path):
                raise ValueError("Moodle HTML orria ez da deskargatzeko fitxategia")
            if notebook and "text/html" in response.headers.get("Content-Type", ""):
                raise ValueError("Drive-k HTML/login orria itzuli du, ez notebook bat")
            if int(response.headers.get("Content-Length") or 0) > MAX_DOWNLOAD_BYTES:
                raise ValueError("Moodle fitxategiak tamaina-muga gainditzen du")
            with tempfile.NamedTemporaryFile(dir=dest_path.parent, delete=False) as output:
                temp_path = Path(output.name)
                total = 0
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    total += len(chunk)
                    if total > MAX_DOWNLOAD_BYTES:
                        raise ValueError("Moodle fitxategiak tamaina-muga gainditzen du")
                    output.write(chunk)
        if notebook:
            data = json.loads(temp_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("cells"), list) or not data.get("nbformat"):
                raise ValueError("Drive deskarga ez da notebook JSON bat")
        with temp_path.open("rb") as source:
            prefix = source.read(512).lstrip().lower()
        if dest_path.suffix.lower() not in (".html", ".htm") and prefix.startswith((b"<!doctype html", b"<html")):
            raise ValueError("HTML/login orria ezin da material gisa gorde")
        if dest_path.suffix.lower() in (".html", ".htm") and b"sesskey" in temp_path.read_bytes().lower():
            raise ValueError("HTMLak Moodle saio-datuak ditu")
        if dest_path.suffix.lower() == ".pdf" and not prefix.startswith(b"%pdf-"):
            raise ValueError("PDF fitxategiak ez du PDF goibururik")
        if dest_path.is_file() and file_hash(dest_path) == file_hash(temp_path):
            return False
        os.replace(temp_path, dest_path)
        return True
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


SYNC_REPORT: dict = {}


def file_hash(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def response_filename(response: requests.Response) -> str:
    header = Message()
    header["Content-Disposition"] = response.headers.get("Content-Disposition", "")
    return header.get_filename() or urllib.parse.urlparse(response.url).path.rsplit("/", 1)[-1]


def fetch_file(*args, **kwargs) -> bool:
    """Berriro saiatu sare-etenetan; ez ezkutatu formatu edo baimen akatsak."""
    for attempt in range(3):
        try:
            return download_file(*args, **kwargs)
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.ChunkedEncodingError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def public_url(url: str) -> str:
    """Gorde erreferentzia publikoa, saio-parametrorik eta userinfo gabe."""
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.urlencode([(key, value) for key, value in urllib.parse.parse_qsl(parsed.query)
                                   if key in {"id", "section", "forcedownload", "export", "usp", "chapterid"}])
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc.rsplit("@", 1)[-1], parsed.path, query, ""))


def sinkronizatu() -> list[str]:
    """Egiaztatu Moodle materiala; erroreak eta kanpo-mugak esplizituak dira."""
    global SYNC_REPORT, SYNC_MANAGED
    session = lortu_saioa()
    # Google tiene su propia autorización; nunca reutilizar cookies de Moodle.
    from google_drive_auth import authenticated_session
    google_auth_error = None
    try:
        google_session = authenticated_session()
    except Exception as exc:
        # No publicar el contenido de excepciones de credenciales.
        google_session = None
        google_auth_error = f"Google OAuth initialization failed ({type(exc).__name__}); reauthorize the account"
        log(google_auth_error)
    downloaded: list[str] = []
    entries: list[dict] = []
    registries: dict[str, list[tuple[str, str, str, str]]] = {}
    seen_activities: set[str] = set()
    seen_files: set[tuple[str, str]] = set()
    activity_types: Counter = Counter()
    assignments: list[dict] = []

    def error(kind: str, url: str, exc: Exception) -> None:
        # Ez idatzi HTML, cookies edo autentifikazio-erantzunen edukia.
        detail = re.sub(r"""https?://[^\s'"]+""", lambda match: public_url(match.group()), str(exc))[:400]
        reason = redact_sensitive(f"{type(exc).__name__}: {detail}")
        entries.append({"kind": kind, "source": public_url(url), "status": "error", "reason": reason})
        log(f"Sinkronizazio errorea ({kind}): {reason}")

    def sync_file(sec: int, url: str, folder: str = "", relative: str | None = None) -> None:
        with moodle_request(session, "HEAD", url, timeout=20) as head:
            head.raise_for_status()
            name = relative or response_filename(head)
        if Path(urllib.parse.unquote(name)).suffix.lower() in (".php", ""):
            raise ValueError("Ez dago benetako fitxategi-izenik")
        dest = helburu_direktorioa(sec, name, karpeta_izena=folder)
        target = safe_download_path(dest, name, nested=bool(relative))
        key = (url, str(target))
        if key in seen_files:
            return
        seen_files.add(key)
        changed = fetch_file(session, url, target, notebook=target.suffix.lower() == ".ipynb")
        if changed:
            downloaded.append(str(target.relative_to(REPO_ROOT.resolve())))
        entries.append({"kind": "file", "source": public_url(url),
                        "path": str(target.relative_to(REPO_ROOT.resolve())),
                        "status": "verified", "sha256": file_hash(target)})
        if target.suffix.lower() == ".docx" and (changed or not target.with_suffix(".md").is_file()):
            md = target.with_suffix(".md")
            previous = file_hash(md) if md.is_file() else None
            docx_to_md(target, md)
            if previous != file_hash(md):
                downloaded.append(str(md.relative_to(REPO_ROOT.resolve())))

    index_url = f"{BASE_URL}/course/view.php?id={COURSE_ID}"
    with moodle_request(session, "GET", index_url, timeout=25) as response:
        response.raise_for_status()
        course = BeautifulSoup(response.text, "html.parser")
    sections = set(range(13))
    for element in course.select('[id^="section-"]'):
        value = element.get("id", "").removeprefix("section-")
        if value.isdigit():
            sections.add(int(value))
    for link in course.select('a[href*="section="]'):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(link["href"]).query)
        for value in query.get("section", []):
            if value.isdigit():
                sections.add(int(value))
    log(f"Moodle atalak egiaztatzen: {len(sections)}")
    for sec in sorted(sections):
        section_url = f"{index_url}&section={sec}"
        try:
            with moodle_request(session, "GET", section_url, timeout=25) as response:
                response.raise_for_status()
                if 'id="username"' in response.text:
                    raise ValueError("Moodle saioa galdu da")
                soup = BeautifulSoup(response.text, "html.parser")
        except Exception as exc:
            error("section", section_url, exc)
            continue
        for activity in soup.select(".activity"):
            link = activity.select_one('a.aalink[href], .activityname a[href]') or activity.select_one('a[href]')
            if link is None:
                continue
            url = urllib.parse.urljoin(BASE_URL + "/", link["href"])
            if url in seen_activities:
                continue
            seen_activities.add(url)
            title = (activity.select_one(".instancename") or link).get_text(" ", strip=True)
            kind_match = re.search(r"/mod/([^/]+)/", urllib.parse.urlparse(url).path)
            if not kind_match:
                continue
            kind = kind_match.group(1)
            activity_types[kind] += 1
            try:
                if kind == "resource":
                    with moodle_request(session, "HEAD", url, timeout=20) as head:
                        head.raise_for_status()
                        direct = "pluginfile.php" in urllib.parse.urlparse(head.url).path
                        filename = response_filename(head)
                    if direct and Path(urllib.parse.unquote(filename)).suffix.lower() != ".php":
                        sync_file(sec, url)
                    else:
                        with moodle_request(session, "GET", url, timeout=25) as response:
                            response.raise_for_status()
                            page = BeautifulSoup(response.text, "html.parser")
                        main = page.select_one("#region-main") or page
                        links = [a["href"] for a in main.select('a[href*="pluginfile.php"]')]
                        links += [tag.get("src") or tag.get("data") for tag in main.select('iframe[src*="pluginfile.php"], object[data*="pluginfile.php"], embed[src*="pluginfile.php"], img[src*="pluginfile.php"]')]
                        if not links:
                            raise ValueError("Baliabidearen HTML orrian ez da eranskinik aurkitu")
                        for attachment in dict.fromkeys(links):
                            sync_file(sec, urllib.parse.urljoin(url, attachment))
                elif kind in ("folder", "assign"):
                    with moodle_request(session, "GET", url, timeout=25) as response:
                        response.raise_for_status()
                        page = BeautifulSoup(response.text, "html.parser")
                    if kind == "assign":
                        intro = page.select_one("#intro")
                        dates = page.select_one(".activity-dates")
                        # Solo enunciado y fechas generales: nunca entregas,
                        # calificaciones ni la tabla personal del alumnado.
                        assignments.append({
                            "title": title, "section": sec, "source": public_url(url),
                            "statement": intro.get_text(" ", strip=True) if intro else "",
                            "dates": dates.get_text(" ", strip=True) if dates else "",
                        })
                    selector = '#region-main a[href*="pluginfile.php"]' if kind == "folder" else '#intro a[href*="pluginfile.php"], .introattachment a[href*="pluginfile.php"]'
                    for attachment in page.select(selector):
                        href = urllib.parse.urljoin(url, attachment["href"])
                        relative = None
                        if kind == "folder":
                            match = re.search(r"/content/\d+/(.+)$", urllib.parse.urlparse(href).path)
                            relative = match.group(1) if match else urllib.parse.urlparse(href).path.rsplit("/", 1)[-1]
                        try:
                            sync_file(sec, href, title if kind == "folder" else "", relative)
                        except Exception as exc:
                            error(kind, href, exc)
                elif kind == "url":
                    with moodle_request(session, "GET", url, stop_at_external=True, timeout=25) as response:
                        external = urllib.parse.urljoin(response.url, response.headers["Location"]) if response.is_redirect else None
                        if not external:
                            response.raise_for_status()
                            page = BeautifulSoup(response.text, "html.parser")
                            main = page.select_one("#region-main") or page
                            for candidate in main.select('a[href]'):
                                href = candidate["href"]
                                host = urllib.parse.urlparse(href).hostname
                                if href.startswith("https://") and host and host not in {urllib.parse.urlparse(BASE_URL).hostname, "moodle.org", "moodle.com"}:
                                    external = href
                                    break
                    if not external:
                        raise ValueError("URL jarduerak ez du kanpoko estekarik")
                    external_parts = urllib.parse.urlsplit(external)
                    if (external_parts.scheme != "https" or not external_parts.hostname
                            or external_parts.username or external_parts.password):
                        raise ValueError("Kanpo-estekak HTTPS eta userinfo gabe izan behar du")
                    status = "web reference"
                    google_reason = None
                    google_api_reason = None
                    match = None
                    if external_parts.hostname in {"drive.google.com", "colab.research.google.com"}:
                        match = re.search(r"/(?:file/d/|drive/)([A-Za-z0-9_-]+)", external_parts.path)
                    if match:
                        slug = re.sub(r"[^\w\-]+", "_", title).strip("_")[:60]
                        target = safe_download_path(helburu_direktorioa(sec, title), f"{slug}.ipynb")
                        try:
                            if google_session is not None:
                                google_url = (
                                    f"https://www.googleapis.com/drive/v3/files/{match.group(1)}"
                                    "?alt=media&supportsAllDrives=true"
                                )
                                try:
                                    changed = fetch_file(google_session, google_url, target,
                                        allowed_hosts={"www.googleapis.com"}, notebook=True)
                                except (requests.RequestException, ValueError) as api_exc:
                                    if isinstance(api_exc, requests.HTTPError) and api_exc.response is not None:
                                        google_api_reason = f"Google Drive API HTTP {api_exc.response.status_code}"
                                    else:
                                        google_api_reason = f"Google API download failed ({type(api_exc).__name__})"
                                    # Una autorización no elimina el acceso público original.
                                    with requests.Session() as public_session:
                                        changed = fetch_file(public_session, f"https://drive.google.com/uc?export=download&id={match.group(1)}", target,
                                            allowed_hosts={"drive.google.com", "drive.usercontent.google.com"}, notebook=True)
                            else:
                                # Ez bidali Moodle cookies-ak Google-ra.
                                with requests.Session() as public_session:
                                    changed = fetch_file(public_session, f"https://drive.google.com/uc?export=download&id={match.group(1)}", target,
                                        allowed_hosts={"drive.google.com", "drive.usercontent.google.com"}, notebook=True)
                            if changed:
                                downloaded.append(str(target.relative_to(REPO_ROOT.resolve())))
                            entries.append({"kind": "external notebook", "source": public_url(external), "path": str(target.relative_to(REPO_ROOT.resolve())), "status": "verified", "sha256": file_hash(target)})
                            status = "downloaded and verified"
                        except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
                            status = "not downloaded: Google access or download unavailable"
                            if google_session is None:
                                google_reason = (google_auth_error or "Google OAuth is not configured for the synchronizer") + "; public download unavailable"
                            elif google_api_reason:
                                google_reason = google_api_reason + f"; public download unavailable ({type(exc).__name__})"
                            elif isinstance(exc, requests.HTTPError) and exc.response is not None:
                                google_reason = f"Google Drive API HTTP {exc.response.status_code}; check account access, API activation and download permission"
                            else:
                                google_reason = f"Google download or notebook validation failed ({type(exc).__name__})"
                    dest = helburu_direktorioa(sec, title)
                    registries.setdefault(str(dest), []).append((title, public_url(url), public_url(external), status))
                    entry = {"kind": "external link", "source": public_url(external), "activity": public_url(url), "status": status}
                    if google_reason:
                        entry["reason"] = google_reason
                    if match and google_auth_error:
                        entry["oauth_warning"] = google_auth_error
                    entries.append(entry)
                elif kind in ("page", "book", "lesson", "scorm", "wiki"):
                    # Hauek ez dira fitxategiak. Ez aldarrikatu deskarga osoa.
                    entries.append({"kind": kind, "source": public_url(url), "status": "manual review required"})
                else:
                    entries.append({"kind": kind, "source": public_url(url), "status": "interactive activity (not mirrored)"})
            except Exception as exc:
                error(kind, url, exc)
    for name in idatzi_url_erregistroak(registries):
        downloaded.append(name)
    if not seen_activities or not seen_files:
        error("course", index_url, ValueError("Ez da jarduera edo fitxategirik aurkitu; ezin da arrakasta aldarrikatu"))
    for entry in entries:
        if entry.get("status") == "verified" and entry.get("path"):
            target = REPO_ROOT / entry["path"]
            if not target.is_file() or file_hash(target) != entry["sha256"]:
                entry["status"] = "error"
                entry["reason"] = "Saved hash mismatch: possible filename collision or concurrent edit"
    errors = sum(entry["status"] == "error" for entry in entries)
    unavailable = sum(entry["status"].startswith("not downloaded") or entry["status"] == "manual review required" for entry in entries)
    SYNC_REPORT = {"verified_on": datetime.now().date().isoformat(),
                   "scope": "Moodle resources, folders and assignment statements; external/interactive limitations explicit",
                   "sections": sorted(sections), "activities": len(seen_activities),
                   "activity_types": dict(sorted(activity_types.items())),
                   "assignments": assignments,
                   "errors": errors, "unavailable": unavailable, "entries": entries}
    report_path = REPO_ROOT / "00_Transversal" / "MOODLE_SYNC_ESTADO.json"
    payload = json.dumps(SYNC_REPORT, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if not report_path.exists() or report_path.read_text() != payload:
        report_path.write_text(payload)
        downloaded.append(str(report_path.relative_to(REPO_ROOT)))
    # El publicador recupera por separado el material gestionado pendiente,
    # sin incluir cambios ajenos en scripts o soluciones.
    managed = {entry["path"] for entry in entries if entry.get("status") == "verified" and entry.get("path")}
    managed.update(str(safe_download_path(Path(dest), "MOODLE_URLs.md").relative_to(REPO_ROOT.resolve())) for dest in registries)
    managed.add(str(report_path.relative_to(REPO_ROOT)))
    managed.update(str(Path(name).with_suffix(".md")) for name in list(managed)
                   if Path(name).suffix.lower() == ".docx" and (REPO_ROOT / Path(name).with_suffix(".md")).is_file())
    SYNC_MANAGED = sorted(managed)
    # Solo cambios reales de este ciclo. Cambios pendientes en HEAD no son
    # nuevas descargas ni deben repetir la notificación cada hora.
    log(f"Cobertura: {len(sections)} atal, {len(seen_activities)} jarduera, {errors} errore, {unavailable} kanpo/manual muga")
    session.close()
    if google_session is not None:
        google_session.close()
    return sorted(set(downloaded))


def idatzi_url_erregistroak(erregistroak: dict) -> list[str]:
    """Idatzi MOODLE_URLs.md helburu-karpeta bakoitzean (determinista).

    Kanpo-estekak (Colab/Drive/artikuluak) ez dira `mod/resource` eta
    isilean galduko: erregistroak Moodle izena, jarduera-URL eta kanpoko
    URLa jasotzen ditu, hurrengo sync-ean berridatzita.
    """
    def cell(value: str) -> str:
        return html.escape(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")

    changed = []
    for dest_s, zerrenda in sorted(erregistroak.items()):
        dest_dir = Path(dest_s)
        registry_path = safe_download_path(dest_dir, "MOODLE_URLs.md")
        dest_dir.mkdir(parents=True, exist_ok=True)
        lerroak = [
            "# Moodle kanpo-estekak (AUTO-GENERATED — ez editatu)",
            "",
            f"Atalaren `{dest_dir.name}` karpetako `mod/url` jarduerak. Sync bakoitzean berridazten da.",
            "",
            "| Moodle izena | Jarduera | Kanpoko URLa | Egoera |",
            "|---|---|---|---|",
        ]
        ikusitakoak = set()
        for izena, jarduera, kanpoko, egoera in sorted(zerrenda):
            if (izena, kanpoko) in ikusitakoak:
                continue
            ikusitakoak.add((izena, kanpoko))
            lerroak.append(f"| {cell(izena)} | {cell(jarduera)} | {cell(kanpoko)} | {egoera} |")
        payload = "\n".join(lerroak) + "\n"
        if not registry_path.exists() or registry_path.read_text() != payload:
            registry_path.write_text(payload, encoding="utf-8")
            changed.append(str(registry_path.relative_to(REPO_ROOT.resolve())))
    return changed


SAIAKERA_MAX = 5
SAIAKERA_ATSEDENA_S = 30
SYNC_MANAGED: list[str] = []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-publish", action="store_true", help="Deskargatu/egiaztatu soilik; Git commit/push gabe")
    parser.add_argument("--prepare-review", action="store_true", help="Preparar snapshot local para revisión, sin push")
    parser.add_argument("--browser-cdp", type=int, help="Puerto CDP loopback de Chromium ya autenticado (uso manual)")
    args = parser.parse_args()
    if args.browser_cdp is not None:
        if not 1 <= args.browser_cdp <= 65535:
            parser.error("--browser-cdp debe ser un puerto entre 1 y 65535")
        os.environ["MOODLE_BROWSER_CDP_PORT"] = str(args.browser_cdp)
    log("=== Sinkronizazio zikloa hasita ===")
    berriak: list[str] = []
    try:
        for saiakera in range(1, SAIAKERA_MAX + 1):
            try:
                berriak = sinkronizatu()
                break
            except MoodleAuthenticationRejected:
                # No repetir un rechazo explícito del servidor. Los fallos
                # de red/transitorios conservan sus reintentos anteriores.
                raise
            except Exception as e:
                log(f"{saiakera}. saiakera huts: {e}")
                if saiakera >= SAIAKERA_MAX:
                    raise
                time.sleep(SAIAKERA_ATSEDENA_S)
        if SYNC_REPORT.get("errors"):
            raise RuntimeError(f"Moodle sinkronizazioa osatu gabe: {SYNC_REPORT['errors']} errore; ez da argitaratu")
        if SYNC_REPORT.get("unavailable"):
            log(f"Moodle fitxategiak egiaztatuta; {SYNC_REPORT['unavailable']} kanpo/manual jarduera ez da deskargatu")
        if args.no_publish and not args.prepare_review:
            log(f"Egiaztapena amaituta: {len(berriak)} fitxategi aldatu; commit/push gabe")
            return
        if SYNC_REPORT.get("unavailable"):
            pending = SYNC_REPORT["unavailable"]
            log(f"Publicación pendiente: {pending} fuentes externas/manuales sin descargar; ciclo terminado sin commit/push")
            notify(
                "Moodle Sync: material pendiente",
                f"Descarga de Moodle verificada. Faltan {pending} fuentes externas/manuales. "
                "Publicación automática bloqueada; consulta MOODLE_SYNC_ESTADO.json.",
            )
            return
        if berriak:
            log(f"Deskargatutako fitxategiak ({len(berriak)}): {', '.join(berriak)}")
            notify(
                "Moodle Eguneratua!",
                f"{len(berriak)} fitxategi berri deskargatu dira:\n" + "\n".join(berriak[:3]),
            )

        else:
            log("Ez dago fitxategi berririk Moodle-n.")
        # Comprobar siempre el material contra el remoto. Un push fallido
        # sigue pendiente aunque Moodle no cambie en el siguiente ciclo.
        from moodle_publish import publish_snapshot
        result = publish_snapshot(
            REPO_ROOT, SYNC_MANAGED,
            remote=os.environ.get("MOODLE_GIT_REMOTE", "origin"),
            base_branch=os.environ.get("MOODLE_BASE_BRANCH", "master"),
            publish=not args.prepare_review and not args.no_publish,
        )
        if result["status"] == "current":
            log("Material verificado ya presente en la rama remota base.")
        else:
            log(f"Snapshot {result['status']}: {result['branch']} {result['commit'][:12]}; integración mediante PR pendiente")

    except Exception as e:
        log(f"Errore orokorra sinkronizazioan: {e}")
        notify("Moodle Sync Errorea", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
