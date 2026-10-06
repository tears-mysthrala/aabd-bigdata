"""Regresiones reales de Git: protección de master y trabajo local ajeno."""

import os
import subprocess
from pathlib import Path

import pytest

from moodle_publish import publish_snapshot


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


@pytest.fixture
def repositories(tmp_path):
    root = tmp_path / "checkout"
    root.mkdir()
    remote = tmp_path / "remote.git"
    git(root, "init", "-b", "master")
    git(root, "config", "user.name", "Fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    (root / "material.txt").write_text("viejo\n")
    (root / "user.txt").write_text("base\n")
    git(root, "add", "material.txt", "user.txt")
    git(root, "commit", "-m", "base")
    git(root, "init", "--bare", str(remote))
    git(root, "remote", "add", "origin", str(remote))
    git(root, "push", "origin", "master")
    # Igual que GH006: el remoto protege master, admite ramas de revisión.
    hook = remote / "hooks" / "pre-receive"
    hook.write_text(
        "#!/bin/sh\nwhile read old new ref; do\n"
        '  [ "$ref" != refs/heads/master ] || exit 1\n'
        "done\n"
        '[ ! -f "reject-review" ]\n'
    )
    hook.chmod(0o700)
    return root, remote


def test_recovers_committed_material_preserving_head_index_and_dirty_files(
    repositories,
):
    root, remote = repositories
    base = git(root, "rev-parse", "HEAD")
    # Hay un commit local que nunca debe viajar en la rama de Moodle.
    (root / "private.txt").write_text("trabajo ajeno\n")
    git(root, "add", "private.txt")
    git(root, "commit", "-m", "trabajo local ajeno")
    (root / "material.txt").write_text("nuevo\n")
    git(root, "add", "material.txt")
    git(root, "commit", "-m", "descargado, push antiguo fallido")
    # Próximo ciclo: ninguna descarga nueva, pero el material sigue pendiente.
    (root / "user.txt").write_text("staged\n")
    git(root, "add", "user.txt")
    (root / "user.txt").write_text("staged y cambio adicional\n")
    before = git(root, "status", "--porcelain=v1")
    head = git(root, "rev-parse", "HEAD")
    index = git(root, "write-tree")
    result = publish_snapshot(root, ["material.txt"], publish=True)
    assert result["status"] == "published"
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "write-tree") == index
    assert git(root, "status", "--porcelain=v1") == before
    assert git(remote, "rev-parse", "master") == base
    commit = result["commit"]
    assert git(remote, "rev-parse", f"{commit}^") == base
    assert git(remote, "show", f"{commit}:material.txt") == "nuevo"
    assert git(remote, "show", f"{commit}:user.txt") == "base"
    assert "private.txt" not in git(remote, "ls-tree", "--name-only", commit)
    # Idempotente: reutiliza el commit publicado y conserva el trabajo local.
    repeated = publish_snapshot(root, ["material.txt"], publish=True)
    assert repeated["commit"] == commit
    assert git(root, "status", "--porcelain=v1") == before


def test_failed_push_can_be_retried_without_a_new_download(repositories):
    root, remote = repositories
    (root / "material.txt").write_text("pendiente\n")
    (remote / "reject-review").write_text("fallo transitorio")
    with pytest.raises(RuntimeError, match="push falló"):
        publish_snapshot(root, ["material.txt"], publish=True)
    (remote / "reject-review").unlink()
    result = publish_snapshot(root, ["material.txt"], publish=True)
    assert result["status"] == "published"
    assert git(remote, "show", f"{result['commit']}:material.txt") == "pendiente"


def test_preparation_does_not_create_remote_branches(repositories):
    root, remote = repositories
    (root / "material.txt").write_text("nuevo\n")
    result = publish_snapshot(root, ["material.txt"])
    assert result["status"] == "prepared"
    assert (
        git(remote, "for-each-ref", "--format=%(refname)", "refs/heads/")
        == "refs/heads/master"
    )


@pytest.mark.parametrize("path", ["../private.txt", "/tmp/private.txt", ".git/config"])
def test_rejects_paths_outside_managed_tree(repositories, path):
    with pytest.raises(ValueError, match="Ruta de publicación"):
        publish_snapshot(repositories[0], [path])


def test_rejects_symlinks_and_missing_files(repositories):
    root, _ = repositories
    (root / "link.txt").symlink_to(root / "material.txt")
    with pytest.raises(ValueError, match="enlaces"):
        publish_snapshot(root, ["link.txt"])
    with pytest.raises(ValueError, match="Falta un archivo"):
        publish_snapshot(root, ["missing.txt"])


def test_already_merged_material_creates_nothing(repositories):
    root, _ = repositories
    assert publish_snapshot(root, ["material.txt"], publish=True)["status"] == "current"


def test_moodle_filenames_with_non_ascii_characters(repositories):
    root, remote = repositories
    name = "ariketa berria — ebazpena.txt"
    (root / name).write_text("enunciado verificado\n")
    result = publish_snapshot(root, [name], publish=True)
    assert result["paths"] == [name]
    assert git(remote, "show", f"{result['commit']}:{name}") == "enunciado verificado"


def test_daily_branch_is_reused_and_fast_forwards_for_same_day_updates(repositories):
    root, remote = repositories
    (root / "material.txt").write_text("primera versión\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    assert first["branch"].startswith("moodle-sync/master/")
    assert first["branch"].count("/") == 2

    (root / "material.txt").write_text("segunda versión\n")
    second = publish_snapshot(root, ["material.txt"], publish=True)
    assert second["branch"] == first["branch"]
    assert second["commit"] != first["commit"]
    assert git(remote, "show", f"{second['commit']}:material.txt") == "segunda versión"
    assert git(remote, "rev-parse", f"{second['commit']}^") == first["commit"]


def test_stale_checkout_does_not_revert_newer_published_material(
    repositories, tmp_path
):
    root, remote = repositories
    stale = tmp_path / "desfasado"
    subprocess.check_output(["git", "clone", str(remote), str(stale)], text=True)
    git(stale, "config", "user.name", "Fixture")
    git(stale, "config", "user.email", "fixture@example.invalid")
    # A publica una versión nueva del material.
    (root / "material.txt").write_text("segunda versión\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    assert first["status"] == "published"
    # B sigue con la versión de la base y publica otra novedad: el material
    # más nuevo no debe revertirse aunque el commit avance en fast-forward.
    assert (stale / "material.txt").read_text() == "viejo\n"
    (stale / "other.txt").write_text("otro\n")
    result = publish_snapshot(stale, ["material.txt", "other.txt"], publish=True)
    assert result["status"] == "published"
    assert "material.txt" in result["preserved"]
    assert "other.txt" in result["paths"]
    assert git(remote, "show", f"{result['commit']}:material.txt") == "segunda versión"
    assert git(remote, "show", f"{result['commit']}:other.txt") == "otro"
    # Reintentar con el conjunto completo tampoco revierte nada: es idempotente.
    repeated = publish_snapshot(stale, ["material.txt", "other.txt"], publish=True)
    assert repeated["paths"] == []
    assert git(remote, "show", f"{repeated['commit']}:material.txt") == (
        "segunda versión"
    )


def test_contaminated_daily_branch_is_rejected(repositories, tmp_path):
    root, remote = repositories
    (root / "material.txt").write_text("primera versión\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    branch = first["branch"]
    # Contaminación externa: un commit ajeno directo sobre la rama diaria.
    (root / "evil.txt").write_text("no verificado\n")
    env = dict(os.environ, GIT_INDEX_FILE=str(tmp_path / "evil-index"))
    subprocess.check_output(["git", "read-tree", first["commit"]], cwd=root, env=env)
    subprocess.check_output(["git", "add", "--", "evil.txt"], cwd=root, env=env)
    tree = subprocess.check_output(["git", "write-tree"], cwd=root, env=env, text=True)
    commit = subprocess.check_output(
        ["git", "commit-tree", tree.strip(), "-p", first["commit"]],
        cwd=root,
        env=env,
        text=True,
        input="Moodle: cambio ajeno\n",
    ).strip()
    subprocess.check_output(
        ["git", "push", "origin", f"{commit}:refs/heads/{branch}"], cwd=root
    )
    # Aunque este ciclo no cambie nada, heredar la rama contaminada se rechaza.
    with pytest.raises(RuntimeError, match="ajenos al material"):
        publish_snapshot(root, ["material.txt"], publish=True)
    assert git(remote, "show", f"{commit}:evil.txt") == "no verificado"
