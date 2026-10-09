"""Cobertura de páginas: contenido docente, sin envoltorio de sesión."""

import sys
from types import SimpleNamespace

import moodle_sync as sync
import pytest
import requests

URL = sync.BASE_URL + "/mod/page/view.php?id=64153"


def test_page_preserves_text_and_links_but_not_session_wrapper():
    source = """<nav>Persona privada</nav><input id='username'>
    <main id='region-main'><div class='generalbox'><div class='no-overflow'>
    <h2>Guía</h2><p>Teoría: <strong>3 puntos</strong>.</p>
    <a href='https://example.org/reference?sesskey=private'>Referencia</a>
    </div></div></main>"""
    # Un login detectado en cualquier parte invalida la respuesta.
    with pytest.raises(ValueError, match="autenticación"):
        sync.page_document(source, URL, "Guía")
    payload = sync.page_document(
        source.replace("<input id='username'>", ""), URL, "Guía"
    )
    assert "Teoría:" in payload and "3 puntos" in payload
    assert "https://example.org/reference" in payload
    assert "Persona privada" not in payload and "private" not in payload
    assert (
        sync.page_document(source.replace("<input id='username'>", ""), URL, "Guía")
        == payload
    )


@pytest.mark.parametrize(
    "body", ["", "<nav>Sin contenido</nav>", "<div class='generalbox'> </div>"]
)
def test_empty_or_unrecognized_page_is_not_verified(body):
    with pytest.raises(ValueError):
        sync.page_document(body, URL, "Guía")


@pytest.mark.parametrize(
    "asset",
    [
        "<img src='/x.png'>",
        "<iframe src='/x'>",
        "<video></video>",
        "<a href='/pluginfile.php/1/example.pdf'>PDF</a>",
    ],
)
def test_non_text_material_remains_pending(asset):
    source = f"<main id='region-main'><div class='generalbox'>Texto{asset}</div></main>"
    with pytest.raises(sync.ManualPageRequired):
        sync.page_document(source, URL, "Guía")


def test_multiple_content_boxes_are_ambiguous():
    with pytest.raises(ValueError, match="ambiguo"):
        sync.page_document(
            "<main id='region-main'><div class='generalbox'>A</div><div class='generalbox'>B</div></main>",
            URL,
            "Guía",
        )


def test_page_table_is_not_flattened_without_column_boundaries():
    with pytest.raises(sync.ManualPageRequired):
        sync.page_document(
            "<main id='region-main'><div class='generalbox'><table><tr><td>A</td><td>B</td></tr></table></div></main>",
            URL,
            "Guía",
        )


def test_public_video_and_anchor_survive_but_credentials_do_not():
    url = "https://private@example.org/watch?v=lesson&t=30&sesskey=hidden#section-2"
    clean = sync.public_url(url)
    assert clean == "https://example.org/watch?v=lesson&t=30#section-2"
    assert (
        sync.public_url("https://example.org/#access_token=hidden")
        == "https://example.org/"
    )
    page = f'<main id="region-main"><div class="generalbox"><a href="{url}">Vídeo</a></div></main>'
    saved = sync.page_document(page, URL, "Guía")
    assert clean in saved and "hidden" not in saved and "private@" not in saved


def test_atomic_write_failure_preserves_existing_page(monkeypatch, tmp_path):
    target = tmp_path / "page.md"
    target.write_text("previous", encoding="utf-8")

    def fail_replace(self, destination):
        raise OSError("simulated replacement failure")

    monkeypatch.setattr(type(target), "replace", fail_replace)
    with pytest.raises(OSError):
        sync.write_page_atomic(target, "new text")
    assert target.read_text() == "previous"
    assert list(tmp_path.iterdir()) == [target]


def test_atomic_write_success_is_idempotent(tmp_path):
    target = tmp_path / "page.md"
    assert sync.write_page_atomic(target, "new text")
    assert not sync.write_page_atomic(target, "new text")
    assert target.read_text() == "new text"


@pytest.mark.parametrize("media", [False, True])
def test_full_cycle_tracks_page_hash_or_keeps_coverage_pending(
    monkeypatch, tmp_path, media
):
    monkeypatch.setattr(sync, "REPO_ROOT", tmp_path)
    (tmp_path / "00_Transversal").mkdir()
    monkeypatch.setattr(sync, "log", lambda *args: None)
    monkeypatch.setattr(sync, "lortu_saioa", requests.Session)
    monkeypatch.setitem(
        sys.modules,
        "google_drive_auth",
        SimpleNamespace(authenticated_session=lambda: None),
    )
    resource_url = sync.BASE_URL + "/mod/resource/view.php?id=1"
    course_html = f"""<div class='activity'><a class='aalink' href='{URL}'>Guía</a></div>
    <div class='activity'><a class='aalink' href='{resource_url}'>example.csv</a></div>"""

    def request(session, method, url, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.url = url
        response._content_consumed = True
        if method == "HEAD":
            response.url = sync.BASE_URL + "/pluginfile.php/1/example.csv"
            response.headers["Content-Disposition"] = (
                'attachment; filename="example.csv"'
            )
            response._content = b""
        elif "/mod/page/" in url:
            body = "Texto docente" + ("<img src='/x.png'>" if media else "")
            response._content = f"<main id='region-main'><div class='generalbox'>{body}</div></main>".encode()
        else:
            response._content = course_html.encode()
        return response

    def fetch(session, url, target, **kwargs):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("value\n1\n")
        return True

    monkeypatch.setattr(sync, "moodle_request", request)
    monkeypatch.setattr(sync, "fetch_file", fetch)
    sync.sinkronizatu()
    assert sync.SYNC_REPORT["errors"] == 0
    page = next(e for e in sync.SYNC_REPORT["entries"] if e["kind"] == "page")
    if media:
        assert sync.SYNC_REPORT["unavailable"] == 1
        assert page["status"] == "manual review required"
        assert "path" not in page
    else:
        assert sync.SYNC_REPORT["unavailable"] == 0
        assert page["status"] == "verified"
        assert sync.file_hash(tmp_path / page["path"]) == page["sha256"]
        assert page["path"] in sync.SYNC_MANAGED
        assert page["path"] not in sync.sinkronizatu()
        assert sync.file_hash(tmp_path / page["path"]) == page["sha256"]
