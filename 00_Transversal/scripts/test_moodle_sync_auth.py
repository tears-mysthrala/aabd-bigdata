"""No repetir rechazos explícitos de Moodle; conservar recuperación de red."""

import json
import sys

import moodle_sync
import pytest
import requests


@pytest.mark.parametrize(
    "message",
    [
        "Your account is locked. An unlock link has been sent via email.",
        "Tu cuenta está bloqueada.",
        "Invalid login, please try again. user=fixture@example.invalid",
        "Nombre de usuario o contraseña incorrectos.",
    ],
)
def test_explicit_rejections_have_fixed_messages_without_source_text(message):
    with pytest.raises(moodle_sync.MoodleAuthenticationRejected) as caught:
        moodle_sync.check_login_rejection(message)
    assert "no se reintenta" in str(caught.value)
    assert "fixture@example.invalid" not in str(caught.value)
    assert str(caught.value) != message


def test_unknown_or_empty_messages_do_not_classify_network_failures_as_rejections():
    moodle_sync.check_login_rejection("")
    moodle_sync.check_login_rejection("Connection timed out")


def configure_main(monkeypatch):
    import moodle_publish

    monkeypatch.setattr(
        moodle_publish, "observe_publication", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(sys, "argv", ["moodle_sync.py", "--no-publish"])
    monkeypatch.setattr(moodle_sync, "log", lambda message: None)
    monkeypatch.setattr(moodle_sync, "notify", lambda title, message: None)
    monkeypatch.setattr(moodle_sync, "SYNC_REPORT", {"errors": 0, "unavailable": 0})


def test_main_makes_only_one_attempt_when_moodle_reports_locked_account(monkeypatch):
    configure_main(monkeypatch)
    attempts = []
    sleeps = []

    def blocked():
        attempts.append(True)
        moodle_sync.check_login_rejection("Your account is locked.")

    monkeypatch.setattr(moodle_sync, "sinkronizatu", blocked)
    monkeypatch.setattr(moodle_sync.time, "sleep", sleeps.append)
    with pytest.raises(SystemExit) as caught:
        moodle_sync.main()
    assert caught.value.code == 1
    assert len(attempts) == 1
    assert sleeps == []


def test_main_still_recovers_after_one_transient_failure(monkeypatch):
    configure_main(monkeypatch)
    attempts = []
    sleeps = []

    def transient():
        attempts.append(True)
        if len(attempts) == 1:
            raise TimeoutError("network timeout")
        return []

    monkeypatch.setattr(moodle_sync, "sinkronizatu", transient)
    monkeypatch.setattr(moodle_sync.time, "sleep", sleeps.append)
    moodle_sync.main()
    assert len(attempts) == 2
    assert sleeps == [moodle_sync.SAIAKERA_ATSEDENA_S]


def test_main_checks_pending_publication_with_no_new_downloads(monkeypatch):
    import moodle_publish

    configure_main(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["moodle_sync.py"])
    monkeypatch.setattr(moodle_sync, "sinkronizatu", lambda: [])
    monkeypatch.setattr(moodle_sync, "SYNC_MANAGED", ["material.txt"])
    notifications = []
    publications = []
    monkeypatch.setattr(moodle_sync, "notify", lambda *args: notifications.append(args))

    def publish(root, paths, **kwargs):
        publications.append((paths, kwargs["publish"]))
        return {
            "status": "published",
            "branch": "review/fixture",
            "commit": "123456789abc",
        }

    monkeypatch.setattr(moodle_publish, "publish_snapshot", publish)
    moodle_sync.main()
    assert publications == [(["material.txt"], True)]
    assert notifications == []


def test_automatic_cycle_observes_before_download_and_passes_observation(monkeypatch):
    import moodle_publish

    configure_main(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["moodle_sync.py"])
    observation = moodle_publish.PublicationObservation("daily", "base", "tip")
    events = []

    def observe(*args, **kwargs):
        events.append("observe")
        return observation

    def download():
        assert events == ["observe"]
        events.append("download")
        return []

    def publish(*args, **kwargs):
        assert kwargs["observation"] is observation
        assert events == ["observe", "download"]
        events.append("publish")
        return {"status": "current"}

    monkeypatch.setattr(moodle_publish, "observe_publication", observe)
    monkeypatch.setattr(moodle_sync, "sinkronizatu", download)
    monkeypatch.setattr(moodle_publish, "publish_snapshot", publish)
    moodle_sync.main()
    assert events == ["observe", "download", "publish"]


def test_retry_observes_again_before_redownloading(monkeypatch):
    import moodle_publish

    configure_main(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["moodle_sync.py"])
    events = []

    def observe(*args, **kwargs):
        events.append("observe")
        return moodle_publish.PublicationObservation("daily", "base", str(len(events)))

    def download():
        events.append("download")
        if len(events) == 2:
            raise TimeoutError("network timeout")
        return []

    def publish(*args, **kwargs):
        assert kwargs["observation"].parent == "3"
        return {"status": "current"}

    monkeypatch.setattr(moodle_publish, "observe_publication", observe)
    monkeypatch.setattr(moodle_sync, "sinkronizatu", download)
    monkeypatch.setattr(moodle_sync.time, "sleep", lambda _: None)
    monkeypatch.setattr(moodle_publish, "publish_snapshot", publish)
    moodle_sync.main()
    assert events == ["observe", "download", "observe", "download"]


def test_notebook_download_removes_personal_metadata_and_paths_idempotently(
    monkeypatch, tmp_path
):
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "colab": {"authorship_tag": "private-fixture", "name": "lesson.ipynb"}
        },
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {
                    "executionInfo": {
                        "user": {
                            "userId": "private-fixture",
                            "displayName": "private-fixture",
                        }
                    },
                    "tags": ["lesson"],
                },
                "source": ["print('fixture')\n"],
                "outputs": [
                    {
                        "output_type": "stream",
                        "name": "stdout",
                        "text": ["accuracy=0.9\n", "/tmp/fixture/run.py\n"],
                    }
                ],
            }
        ],
    }

    def response(*args, **kwargs):
        result = requests.Response()
        result.status_code = 200
        result.headers["Content-Type"] = "application/json"
        result._content = json.dumps(notebook).encode()
        result._content_consumed = True
        return result

    monkeypatch.setattr(moodle_sync, "moodle_request", response)
    target = tmp_path / "lesson.ipynb"
    assert moodle_sync.download_file(
        None, "https://fixture.invalid/lesson.ipynb", target, notebook=True
    )
    saved = target.read_bytes()
    cleaned = json.loads(saved)
    assert b"private-fixture" not in saved
    assert b"/tmp/fixture" not in saved
    assert cleaned["cells"][0]["source"] == notebook["cells"][0]["source"]
    assert cleaned["cells"][0]["metadata"] == {"tags": ["lesson"]}
    assert cleaned["cells"][0]["outputs"][0]["text"][0] == "accuracy=0.9\n"
    assert cleaned["metadata"]["colab"]["name"] == "lesson.ipynb"
    # Google puede volver a entregar otras identidades/tiempos; la copia
    # publicable es idéntica y no se anuncia como descarga nueva.
    notebook["cells"][0]["metadata"]["executionInfo"]["timestamp"] = 123
    assert not moodle_sync.download_file(
        None, "https://fixture.invalid/lesson.ipynb", target, notebook=True
    )
    assert target.read_bytes() == saved
