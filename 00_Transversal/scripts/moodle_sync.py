#!/usr/bin/env python3
"""Moodle fitxategien sinkronizazio automatikoa.

Orduro exekutatzen da (systemd timer bidez):
1. Moodle-ra konektatzen da eta saioa hasten du.
2. Atal guztiak aztertzen ditu (fitxategiak, karpetak, zereginak).
3. Aldaketak edo fitxategi berriak badaude, deskargatu eta dagokion karpetan jartzen ditu.
4. .docx fitxategiak .md formatura bihurtzen ditu.
5. Git commit eta push egiten ditu GitHub-era.
6. Mahaigaineko jakinarazpena bidaltzen du (notify-send).
"""

import os
import html
import re
import sys
import time
import subprocess
import tempfile
import urllib.parse
from datetime import datetime
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


def log(msg: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] {msg}"
    print(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def notify(title: str, msg: str) -> None:
    try:
        subprocess.run(["notify-send", "-a", "Moodle Sync", title, msg], check=False)
    except Exception as e:
        log(f"Ezin izan da notify-send exekutatu: {e}")


def lortu_saioa() -> requests.Session:
    """Chromium bidez saioa hasi eta cookies-ak eskuratu."""
    if not USERNAME or not PASSWORD:
        raise SystemExit("Falta MOODLE_USER/MOODLE_PASS en el entorno (nunca en código).")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
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
        cookies = page.context.cookies()
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
        raise RuntimeError("Login Moodle fallido: sesión no autenticada (¿contraseña cambiada?).")
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
            or any(part in ("", ".", "..") for part in parts)
            or (not nested and len(parts) != 1)):
        raise ValueError(f"Moodle izen ez-segurua: {remote_name!r}")
    root = REPO_ROOT.resolve()
    base = dest_dir.resolve()
    candidate = (base / name).resolve()
    if (base != dest_dir.absolute() or candidate != base / name
            or not base.is_relative_to(root) or not candidate.is_relative_to(base)):
        raise ValueError("Moodle deskarga-bidea baimendutako direktoriotik kanpo")
    return candidate


def moodle_request(
    session: requests.Session, method: str, url: str,
    allowed_hosts: set[str] | None = None, **kwargs
) -> requests.Response:
    """Jarraitu soilik baimendutako HTTPS hostetako birbideratzeei."""
    current = urllib.parse.urljoin(BASE_URL + "/", url)
    hosts = allowed_hosts or {urllib.parse.urlparse(BASE_URL).hostname}
    for _ in range(6):
        parsed = urllib.parse.urlparse(current)
        if parsed.scheme != "https" or parsed.hostname not in hosts:
            raise ValueError("Deskarga esteka/birbideratzea baimendutako hostetik kanpo")
        response = session.request(method, current, allow_redirects=False, **kwargs)
        if response.status_code not in (301, 302, 303, 307, 308):
            return response
        location = response.headers.get("Location")
        response.close()
        if not location:
            raise ValueError("Moodle birbideratzeak ez du Location goibururik")
        current = urllib.parse.urljoin(current, location)
    raise ValueError("Moodle birbideratze gehiegi")


def download_file(
    session: requests.Session, url: str, dest_path: Path,
    *, allowed_hosts: set[str] | None = None, notebook: bool = False
) -> None:
    """Deskargatu muga batekin eta ordezkatu fitxategia deskarga osoa denean."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with moodle_request(
            session, "GET", url, allowed_hosts=allowed_hosts, stream=True, timeout=(10, 30)
        ) as response:
            response.raise_for_status()
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
            with temp_path.open("rb") as source:
                if not source.read(1024).lstrip().startswith(b"{"):
                    raise ValueError("Drive deskarga ez da notebook JSON bat")
        os.replace(temp_path, dest_path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def sinkronizatu() -> list[str]:
    """Exekutatu Moodle-ko eskaneatze eta deskarga prozesu osoa."""
    session = lortu_saioa()
    deskargatutakoak: list[str] = []
    erregistratutako_urlak: dict[str, list[tuple[str, str, str]]] = {}

    def erregistratu_url(sec_id: int, izena: str, kanpoko_url: str) -> None:
        dest_dir = helburu_direktorioa(sec_id, izena)
        erregistratutako_urlak.setdefault(str(dest_dir), []).append(
            (izena, act_url, kanpoko_url)
        )

    log("Moodle atalak aztertzen...")
    for sec_id in range(0, 13):
        url = f"{BASE_URL}/course/view.php?id={COURSE_ID}&section={sec_id}"
        resp = moodle_request(session, "GET", url, timeout=15)
        if resp.status_code != 200:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        activities = soup.select(".activity")

        for act in activities:
            link = act.select_one("a")
            if not link or not link.get("href"):
                continue

            act_url = link["href"]
            inst_el = act.select_one(".instancename") or link
            act_izena = inst_el.text.strip().split("\n")[0].strip()

            # 1. Baliabide zuzenak (mod/resource)
            if "mod/resource" in act_url:
                try:
                    head = moodle_request(session, "HEAD", act_url, timeout=10)
                    cd = head.headers.get("Content-Disposition", "")
                    fname = None
                    if "filename=" in cd:
                        fname = cd.split("filename=")[1].strip("\"' ")
                    elif "/" in head.url:
                        fname = head.url.split("/")[-1].split("?")[0]

                    if not fname:
                        head.close()
                        continue

                    remote_size = int(head.headers.get("Content-Length") or 0)
                    head.close()
                    dest_dir = helburu_direktorioa(sec_id, fname)
                    dest_path = safe_download_path(dest_dir, fname)

                    behar_da = False
                    if not dest_path.exists():
                        behar_da = True
                    elif remote_size > 0 and dest_path.stat().st_size != remote_size:
                        behar_da = True

                    if behar_da:
                        log(f"Deskargatzen: [Sec {sec_id}] {fname} ({remote_size} bytes)...")
                        download_file(session, act_url, dest_path)
                        deskargatutakoak.append(str(dest_path.relative_to(REPO_ROOT)))

                        if fname.lower().endswith(".docx"):
                            md_path = dest_path.with_suffix(".md")
                            docx_to_md(dest_path, md_path)
                            deskargatutakoak.append(str(md_path.relative_to(REPO_ROOT)))

                except Exception as e:
                    log(f"Errorea baliabidea aztertzean ({act_url}): {e}")

            # 2. Karpetak (mod/folder)
            elif "mod/folder" in act_url:
                try:
                    r_fld = moodle_request(session, "GET", act_url, timeout=15)
                    r_fld.raise_for_status()
                    f_soup = BeautifulSoup(r_fld.text, "html.parser")
                    base_dest = helburu_direktorioa(sec_id, "", karpeta_izena=act_izena)

                    for a in f_soup.find_all("a"):
                        fhref = a.get("href", "")
                        if "pluginfile.php" in fhref:
                            # Estrakzio bidea URL-tik (adib. Ariketa%203.1/ikasleak_notak_100.csv)
                            match = re.search(r"content/\d+/(.+?)\?", fhref)
                            erlatiboa = match.group(1) if match else a.text.strip()
                            dest_path = safe_download_path(base_dest, erlatiboa, nested=True)

                            head = moodle_request(session, "HEAD", fhref, timeout=10)
                            remote_size = int(head.headers.get("Content-Length") or 0)
                            head.close()

                            behar_da = False
                            if not dest_path.exists():
                                behar_da = True
                            elif remote_size > 0 and dest_path.stat().st_size != remote_size:
                                behar_da = True

                            if behar_da:
                                log(f"Deskargatzen karpetatik: {erlatiboa} ({remote_size} bytes)...")
                                download_file(session, fhref, dest_path)
                                deskargatutakoak.append(str(dest_path.relative_to(REPO_ROOT)))

                                if dest_path.name.lower().endswith(".docx"):
                                    md_path = dest_path.with_suffix(".md")
                                    docx_to_md(dest_path, md_path)
                                    deskargatutakoak.append(str(md_path.relative_to(REPO_ROOT)))

                except Exception as e:
                    log(f"Errorea karpeta aztertzean ({act_url}): {e}")

            # 3. Zereginen eranskinak (mod/assign)
            elif "mod/assign" in act_url:
                try:
                    r_asg = moodle_request(session, "GET", act_url, timeout=15)
                    r_asg.raise_for_status()
                    asg_soup = BeautifulSoup(r_asg.text, "html.parser")
                    for a in asg_soup.select("#intro a, .introattachment a, .fileuploadsubmission a"):
                        ahref = a.get("href", "")
                        if "pluginfile.php" in ahref and "forcedownload=1" in ahref:
                            fname = a.text.strip()
                            if not fname:
                                continue
                            dest_dir = helburu_direktorioa(sec_id, fname)
                            dest_path = safe_download_path(dest_dir, fname)

                            head = moodle_request(session, "HEAD", ahref, timeout=10)
                            remote_size = int(head.headers.get("Content-Length") or 0)
                            head.close()

                            behar_da = False
                            if not dest_path.exists():
                                behar_da = True
                            elif remote_size > 0 and dest_path.stat().st_size != remote_size:
                                behar_da = True

                            if behar_da:
                                log(f"Deskargatzen zereginetik: {fname} ({remote_size} bytes)...")
                                download_file(session, ahref, dest_path)
                                deskargatutakoak.append(str(dest_path.relative_to(REPO_ROOT)))

                                if fname.lower().endswith(".docx"):
                                    md_path = dest_path.with_suffix(".md")
                                    docx_to_md(dest_path, md_path)
                                    deskargatutakoak.append(str(md_path.relative_to(REPO_ROOT)))
                except Exception as e:
                    log(f"Errorea zeregina aztertzean ({act_url}): {e}")

            # 4. Kanpo-estekak (mod/url: Colab, Drive, artikuluak...)
            # Anatomia: view.php orriak kanpoko URLa erakusten du (ez du
            # birbideratzen). Erregistroan jasotzen da beti; Drive publikoa
            # bada, zuzenean deskargatzen saiatzen da.
            elif "mod/url" in act_url:
                try:
                    r_u = moodle_request(session, "GET", act_url, timeout=15)
                    r_u.raise_for_status()
                    u_soup = BeautifulSoup(r_u.text, "html.parser")
                    kanpoko = None
                    for a in u_soup.find_all("a", href=True):
                        h = a["href"]
                        if h.startswith("http") and "hezkuntza.net" not in h \
                                and "moodle.org" not in h and "moodle.com" not in h:
                            kanpoko = h
                            break
                    if not kanpoko:
                        log(f"URL jarduerak kanpoko estekarik gabe: {act_izena}")
                        continue
                    erregistratu_url(sec_id, act_izena, kanpoko)
                    drive_id = None
                    m = re.search(r"drive\.google\.com/(?:file/d/|drive/)([-\w]+)", kanpoko)
                    if m:
                        drive_id = m.group(1)
                    else:
                        m = re.search(r"colab\.research\.google\.com/drive/([-\w]+)", kanpoko)
                        if m:
                            drive_id = m.group(1)
                    if drive_id:
                        dest_dir = helburu_direktorioa(sec_id, act_izena)
                        slug = re.sub(r"[^\w\-]+", "_", act_izena).strip("_")[:60]
                        dest_path = safe_download_path(dest_dir, f"{slug}.ipynb")
                        if not dest_path.exists():
                            download_file(
                                session,
                                f"https://drive.google.com/uc?export=download&id={drive_id}",
                                dest_path,
                                allowed_hosts={"drive.google.com", "drive.usercontent.google.com"},
                                notebook=True,
                            )
                            deskargatutakoak.append(str(dest_path.relative_to(REPO_ROOT)))
                            log(f"Drive-tik deskargatuta: {act_izena} -> {dest_path.name}")
                except Exception as e:
                    log(f"Errorea URLa aztertzean ({act_url}): {e}")

    idatzi_url_erregistroak(erregistratutako_urlak)
    return deskargatutakoak


def idatzi_url_erregistroak(erregistroak: dict) -> None:
    """Idatzi MOODLE_URLs.md helburu-karpeta bakoitzean (determinista).

    Kanpo-estekak (Colab/Drive/artikuluak) ez dira `mod/resource` eta
    isilean galduko: erregistroak Moodle izena, jarduera-URL eta kanpoko
    URLa jasotzen ditu, hurrengo sync-ean berridatzita.
    """
    def cell(value: str) -> str:
        return html.escape(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")

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
        for izena, jarduera, kanpoko in sorted(zerrenda):
            if (izena, kanpoko) in ikusitakoak:
                continue
            ikusitakoak.add((izena, kanpoko))
            if "colab.research.google.com" in kanpoko or "drive.google.com" in kanpoko:
                egoera = "Google login behar du deskargatzeko"
            else:
                egoera = "erreferentzia (web)"
            lerroak.append(f"| {cell(izena)} | {cell(jarduera)} | {cell(kanpoko)} | {egoera} |")
        registry_path.write_text("\n".join(lerroak) + "\n", encoding="utf-8")


SAIAKERA_MAX = 5
SAIAKERA_ATSEDENA_S = 30


def main() -> None:
    log("=== Sinkronizazio zikloa hasita ===")
    berriak: list[str] = []
    try:
        for saiakera in range(1, SAIAKERA_MAX + 1):
            try:
                berriak = sinkronizatu()
                break
            except Exception as e:
                log(f"{saiakera}. saiakera huts: {e}")
                if saiakera >= SAIAKERA_MAX:
                    raise
                time.sleep(SAIAKERA_ATSEDENA_S)
        if berriak:
            log(f"Deskargatutako fitxategiak ({len(berriak)}): {', '.join(berriak)}")
            notify(
                "Moodle Eguneratua!",
                f"{len(berriak)} fitxategi berri deskargatu dira:\n" + "\n".join(berriak[:3]),
            )

            # Git: bidea ematen dugu deskargatutako fitxategiei soilik.
            # Ez erabili `git add -A`: lan-arloko aldaketa ajenoak ez dira
            # inoiz "Auto-sync" commit batean sartu behar.
            subprocess.run(["git", "add", "--", *berriak], cwd=REPO_ROOT, check=True)
            staged = subprocess.run(
                ["git", "diff", "--cached", "--quiet", "--", *berriak],
                cwd=REPO_ROOT,
            )
            if staged.returncode != 0:
                msg = f"Auto-sync Moodle: {len(berriak)} fitxategi deskargatuta\n\n" + "\n".join(f"- {b}" for b in berriak)
                subprocess.run(["git", "commit", "--only", "-m", msg, "--", *berriak], cwd=REPO_ROOT, check=True)
                subprocess.run(["git", "push", "origin", "master"], cwd=REPO_ROOT, check=True)
                log("Git push ondo osatu da.")
            else:
                log("Aldaketarik ez stage-an: commit/push ez da egin.")
        else:
            log("Ez dago fitxategi berririk Moodle-n.")

    except Exception as e:
        log(f"Errore orokorra sinkronizazioan: {e}")
        notify("Moodle Sync Errorea", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
