"""No repetir rechazos explícitos de Moodle; conservar recuperación de red."""

import sys

import moodle_sync
import pytest


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
