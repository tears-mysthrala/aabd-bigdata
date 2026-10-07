"""Regresiones reales de Git: protección de master y trabajo local ajeno."""

import hashlib
import os
import subprocess
from datetime import date, timedelta
from pathlib import Path

import moodle_publish
import pytest
from moodle_publish import observe_publication, publish_snapshot


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
    git(root, "init", "--bare", "-b", "master", str(remote))
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


def test_edit_after_source_verification_cannot_be_published(repositories):
    root, remote = repositories
    observation = observe_publication(root)
    (root / "material.txt").write_bytes(b"verified source\n")
    hashes = {
        "material.txt": hashlib.sha256((root / "material.txt").read_bytes()).hexdigest()
    }
    (root / "material.txt").write_bytes(b"unverified local edit\n")
    with pytest.raises(RuntimeError, match="no coincide con el material verificado"):
        publish_snapshot(
            root,
            ["material.txt"],
            publish=True,
            observation=observation,
            verified_hashes=hashes,
        )
    assert (
        git(remote, "for-each-ref", "--format=%(refname)", "refs/heads/")
        == "refs/heads/master"
    )


def test_verified_hashes_cover_binary_material_and_reject_incomplete_sets(repositories):
    root, remote = repositories
    (root / "material.txt").write_bytes(b"\x00\xff\x80\n")
    with pytest.raises(ValueError, match="no cubren todo"):
        publish_snapshot(root, ["material.txt"], publish=True, verified_hashes={})
    hashes = {
        "material.txt": hashlib.sha256((root / "material.txt").read_bytes()).hexdigest()
    }
    result = publish_snapshot(
        root, ["material.txt"], publish=True, verified_hashes=hashes
    )
    assert (
        subprocess.check_output(
            ["git", "show", f"{result['commit']}:material.txt"], cwd=remote
        )
        == b"\x00\xff\x80\n"
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


def test_observed_source_can_revert_to_the_base_without_preserving_stale_tip(
    repositories,
):
    root, remote = repositories
    original = (root / "material.txt").read_bytes()
    (root / "material.txt").write_text("updated source\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    observation = observe_publication(root)
    (root / "material.txt").write_bytes(original)
    result = publish_snapshot(
        root,
        ["material.txt"],
        publish=True,
        observation=observation,
        verified_hashes={"material.txt": hashlib.sha256(original).hexdigest()},
    )
    assert (
        subprocess.check_output(
            ["git", "show", f"{result['commit']}:material.txt"], cwd=remote
        )
        == original
    )
    assert result["preserved"] == []
    assert git(remote, "rev-parse", f"{result['commit']}^") == first["commit"]


def test_observed_cycle_reconciles_independent_upstream_changes(repositories):
    root, remote = repositories
    (root / "material.txt").write_text("daily source\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    (root / "user.txt").write_text("upstream code/documentation\n")
    git(root, "add", "user.txt")
    git(root, "commit", "-m", "independent upstream change")
    base = git(root, "rev-parse", "HEAD")
    git(root, "push", "origin", f"{base}:refs/heads/upstream-fixture")
    git(remote, "update-ref", "refs/heads/master", base)
    observation = observe_publication(root)
    (root / "material.txt").write_text("fresh source after upstream change\n")
    result = publish_snapshot(
        root, ["material.txt"], publish=True, observation=observation
    )
    assert (
        git(remote, "show", f"{result['commit']}:user.txt")
        == "upstream code/documentation"
    )
    assert (
        git(remote, "show", f"{result['commit']}:material.txt")
        == "fresh source after upstream change"
    )
    assert git(remote, "rev-parse", f"{result['commit']}^1") == first["commit"]
    assert git(remote, "rev-parse", f"{result['commit']}^2") == base
    assert result["paths"] == ["material.txt"]
    repeated = publish_snapshot(
        root, ["material.txt"], publish=True, observation=observe_publication(root)
    )
    assert repeated["commit"] == result["commit"]


def test_daily_merge_and_new_upstream_files_allow_noop_and_further_updates(
    repositories, tmp_path
):
    root, remote = repositories
    (root / "material.txt").write_text("first download\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    # Merge por PR más un cambio ajeno legítimo en master.
    (root / "user.txt").write_text("new upstream content\n")
    env = dict(os.environ, GIT_INDEX_FILE=str(tmp_path / "merge-index"))
    subprocess.check_output(["git", "read-tree", first["commit"]], cwd=root, env=env)
    subprocess.check_output(["git", "add", "user.txt"], cwd=root, env=env)
    tree = subprocess.check_output(
        ["git", "write-tree"], cwd=root, env=env, text=True
    ).strip()
    merged = subprocess.check_output(
        ["git", "commit-tree", tree, "-p", first["base"], "-p", first["commit"]],
        cwd=root,
        text=True,
        input="merge daily PR\n",
    ).strip()
    git(root, "push", "origin", f"{merged}:refs/heads/upstream-fixture")
    git(remote, "update-ref", "refs/heads/master", merged)
    result = publish_snapshot(
        root, ["material.txt"], publish=True, observation=observe_publication(root)
    )
    assert result["status"] == "current"
    assert git(remote, "rev-parse", first["branch"]) == first["commit"]
    observation = observe_publication(root)
    (root / "material.txt").write_text("second download after merge\n")
    second = publish_snapshot(
        root, ["material.txt"], publish=True, observation=observation
    )
    assert second["branch"] == first["branch"]
    assert git(remote, "rev-parse", f"{second['commit']}^") == merged
    assert git(remote, "show", f"{second['commit']}:user.txt") == "new upstream content"
    assert second["paths"] == ["material.txt"]
    assert git(remote, "rev-parse", "master") == merged


def test_moodle_filenames_with_non_ascii_characters(repositories):
    root, remote = repositories
    name = "ariketa berria — ebazpena.txt"
    (root / name).write_text("enunciado verificado\n")
    result = publish_snapshot(root, [name], publish=True)
    assert result["paths"] == [name]
    assert git(remote, "show", f"{result['commit']}:{name}") == "enunciado verificado"


def test_same_day_reupdate_without_fresh_sync_fails_closed(repositories):
    root, remote = repositories
    (root / "material.txt").write_text("primera versión\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    assert first["branch"].startswith("moodle-sync/master/")
    assert first["branch"].count("/") == 2

    # Tres versiones distintas sin causalidad probada: se rechaza en vez
    # de asumir una actualización secuencial legítima.
    (root / "material.txt").write_text("segunda versión\n")
    with pytest.raises(RuntimeError, match="Conflicto de publicación"):
        publish_snapshot(root, ["material.txt"], publish=True)
    assert git(remote, "show", f"{first['commit']}:material.txt") == "primera versión"
    # Tras sincronizar de nuevo (el material coincide con la rama), el
    # reintento converge de forma idempotente sin revertir nada.
    (root / "material.txt").write_text("primera versión\n")
    repeated = publish_snapshot(root, ["material.txt"], publish=True)
    assert repeated["commit"] == first["commit"]
    assert repeated["paths"] == []


def test_fresh_cycles_update_manifest_and_material_on_the_same_daily_branch(
    repositories,
):
    root, remote = repositories
    paths = ["material.txt", "MOODLE_SYNC_ESTADO.json"]
    master = git(remote, "rev-parse", "master")
    before = git(root, "status", "--porcelain=v1")
    previous = None
    for cycle in range(3):
        observation = observe_publication(root)
        # La descarga y su manifiesto cambian DESPUÉS de la observación.
        (root / "material.txt").write_text(f"descarga {cycle}\n")
        (root / "MOODLE_SYNC_ESTADO.json").write_text(f'{{"cycle": {cycle}}}\n')
        local_state = git(root, "status", "--porcelain=v1")
        result = publish_snapshot(root, paths, publish=True, observation=observation)
        assert (
            git(remote, "show", f"{result['commit']}:material.txt")
            == f"descarga {cycle}"
        )
        assert (
            git(remote, "show", f"{result['commit']}:MOODLE_SYNC_ESTADO.json")
            == f'{{"cycle": {cycle}}}'
        )
        assert git(root, "status", "--porcelain=v1") == local_state
        assert git(root, "rev-parse", "HEAD") == master
        if previous:
            assert result["branch"] == previous["branch"]
            assert (
                git(remote, "rev-parse", f"{result['commit']}^") == previous["commit"]
            )
        previous = result
    assert git(remote, "rev-parse", "master") == master
    assert before == ""
    assert (
        publish_snapshot(
            root, paths, publish=True, observation=observe_publication(root)
        )["commit"]
        == previous["commit"]
    )


@pytest.mark.parametrize("existing_branch", [False, True])
def test_remote_advance_after_observation_rejects_an_independent_checkout(
    repositories, tmp_path, existing_branch
):
    root, remote = repositories
    if existing_branch:
        (root / "material.txt").write_text("primera descarga\n")
        publish_snapshot(root, ["material.txt"], publish=True)
    other = tmp_path / "independent"
    subprocess.check_output(["git", "clone", str(remote), str(other)], text=True)
    git(other, "config", "user.name", "Fixture")
    git(other, "config", "user.email", "fixture@example.invalid")
    observation = observe_publication(other)
    # A publica mientras B está leyendo las fuentes.
    a_observation = observe_publication(root)
    (root / "material.txt").write_text("descarga A\n")
    published = publish_snapshot(
        root, ["material.txt"], publish=True, observation=a_observation
    )
    (other / "material.txt").write_text("descarga B\n")
    with pytest.raises(RuntimeError, match="remoto cambió"):
        publish_snapshot(other, ["material.txt"], publish=True, observation=observation)
    assert git(remote, "rev-parse", published["branch"]) == published["commit"]
    assert git(remote, "show", f"{published['commit']}:material.txt") == "descarga A"
    # Un nuevo ciclo obtiene una observación nueva antes de descargar.
    retry_observation = observe_publication(other)
    (other / "material.txt").write_text("descarga B fresca\n")
    retried = publish_snapshot(
        other, ["material.txt"], publish=True, observation=retry_observation
    )
    assert (
        git(remote, "show", f"{retried['commit']}:material.txt") == "descarga B fresca"
    )


def test_cycle_crossing_midnight_requires_a_fresh_observation(
    repositories, monkeypatch
):
    root, remote = repositories
    observation = observe_publication(root)

    class NextDay:
        @staticmethod
        def today():
            return date.today() + timedelta(days=1)

    monkeypatch.setattr(moodle_publish, "date", NextDay)
    (root / "material.txt").write_text("download crossing midnight\n")
    with pytest.raises(RuntimeError, match="remoto cambió"):
        publish_snapshot(root, ["material.txt"], publish=True, observation=observation)
    assert (
        git(remote, "for-each-ref", "--format=%(refname)", "refs/heads/")
        == "refs/heads/master"
    )


def test_base_advance_during_download_requires_a_fresh_observation(repositories):
    root, remote = repositories
    observation = observe_publication(root)
    (root / "user.txt").write_text("new upstream base\n")
    git(root, "add", "user.txt")
    git(root, "commit", "-m", "upstream base moved")
    new_base = git(root, "rev-parse", "HEAD")
    git(root, "push", "origin", f"{new_base}:refs/heads/upstream-fixture")
    git(remote, "update-ref", "refs/heads/master", new_base)
    (root / "material.txt").write_text("fresh material\n")
    with pytest.raises(RuntimeError, match="remoto cambió"):
        publish_snapshot(root, ["material.txt"], publish=True, observation=observation)
    assert git(remote, "rev-parse", "master") == new_base


def test_concurrent_push_after_validation_is_rejected_without_force(
    repositories, tmp_path, monkeypatch
):
    root, remote = repositories
    (root / "material.txt").write_text("first\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    other = tmp_path / "concurrent"
    subprocess.check_output(["git", "clone", str(remote), str(other)], text=True)
    git(other, "config", "user.name", "Fixture")
    git(other, "config", "user.email", "fixture@example.invalid")
    observation = observe_publication(root)
    (root / "material.txt").write_text("outer download\n")
    original_run = subprocess.run
    concurrent = []

    def run(command, *args, **kwargs):
        if command[:2] == ["git", "push"] and not concurrent:
            assert not any("force" in arg for arg in command)
            concurrent.append(True)
            other_observation = observe_publication(other)
            (other / "material.txt").write_text("concurrent download\n")
            concurrent.append(
                publish_snapshot(
                    other, ["material.txt"], publish=True, observation=other_observation
                )
            )
        return original_run(command, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(RuntimeError, match="push falló"):
        publish_snapshot(root, ["material.txt"], publish=True, observation=observation)
    assert git(remote, "rev-parse", first["branch"]) == concurrent[1]["commit"]
    assert (
        git(remote, "show", f"{first['branch']}:material.txt") == "concurrent download"
    )


def test_concurrent_same_file_updates_fail_closed(repositories, tmp_path):
    root, remote = repositories
    other = tmp_path / "checkout-b"
    subprocess.check_output(["git", "clone", str(remote), str(other)], text=True)
    git(other, "config", "user.name", "Fixture")
    git(other, "config", "user.email", "fixture@example.invalid")
    # A publica primero; B, sincronizado antes pero con otro contenido
    # distinto de la base y de la rama, debe chocar en cerrado.
    (root / "material.txt").write_text("versión A\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    (other / "material.txt").write_text("versión B\n")
    with pytest.raises(RuntimeError, match="Conflicto de publicación"):
        publish_snapshot(other, ["material.txt"], publish=True)
    assert git(remote, "show", f"{first['commit']}:material.txt") == "versión A"


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
    with pytest.raises(RuntimeError, match="ajenos al material"):
        publish_snapshot(
            root, ["material.txt"], publish=True, observation=observe_publication(root)
        )
    assert git(remote, "show", f"{commit}:evil.txt") == "no verificado"


def test_unmanaged_rename_source_cannot_hide_in_a_managed_destination(
    repositories, tmp_path
):
    root, remote = repositories
    (root / "material.txt").write_text("first publication\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    (root / "renamed.txt").write_text("base\n")
    env = dict(os.environ, GIT_INDEX_FILE=str(tmp_path / "rename-index"))
    subprocess.check_output(["git", "read-tree", first["commit"]], cwd=root, env=env)
    subprocess.check_output(["git", "rm", "--cached", "user.txt"], cwd=root, env=env)
    subprocess.check_output(["git", "add", "renamed.txt"], cwd=root, env=env)
    tree = subprocess.check_output(
        ["git", "write-tree"], cwd=root, env=env, text=True
    ).strip()
    commit = subprocess.check_output(
        ["git", "commit-tree", tree, "-p", first["commit"]],
        cwd=root,
        text=True,
        input="external rename\n",
    ).strip()
    git(root, "push", "origin", f"{commit}:refs/heads/{first['branch']}")
    with pytest.raises(RuntimeError, match="ajenos al material"):
        publish_snapshot(root, ["material.txt", "renamed.txt"], publish=True)
    assert git(remote, "rev-parse", first["branch"]) == commit


@pytest.mark.parametrize("mode", ["120000", "160000"])
def test_inherited_symlinks_and_gitlinks_are_rejected(repositories, tmp_path, mode):
    root, remote = repositories
    (root / "material.txt").write_text("first\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    env = dict(os.environ, GIT_INDEX_FILE=str(tmp_path / "entry-index"))
    subprocess.check_output(["git", "read-tree", first["commit"]], cwd=root, env=env)
    oid = (
        first["commit"]
        if mode == "160000"
        else subprocess.check_output(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=root,
            text=True,
            input="../outside\n",
        ).strip()
    )
    subprocess.check_output(
        ["git", "update-index", "--cacheinfo", f"{mode},{oid},material.txt"],
        cwd=root,
        env=env,
    )
    tree = subprocess.check_output(
        ["git", "write-tree"], cwd=root, env=env, text=True
    ).strip()
    commit = subprocess.check_output(
        ["git", "commit-tree", tree, "-p", first["commit"]],
        cwd=root,
        text=True,
        input="unsupported entry\n",
    ).strip()
    git(root, "push", "origin", f"{commit}:refs/heads/{first['branch']}")
    (root / "material.txt").write_text("viejo\n")
    with pytest.raises(RuntimeError, match="Tipo de entrada heredada"):
        publish_snapshot(root, ["material.txt"], publish=True)
    assert git(remote, "rev-parse", first["branch"]) == commit


def test_unmerged_daily_branch_on_old_base_is_rejected(repositories):
    root, remote = repositories
    (root / "material.txt").write_text("daily version\n")
    first = publish_snapshot(root, ["material.txt"], publish=True)
    (root / "material.txt").write_text("new master version\n")
    git(root, "add", "material.txt")
    git(root, "commit", "-m", "base advanced independently")
    base = git(root, "rev-parse", "HEAD")
    git(root, "push", "origin", f"{base}:refs/heads/upstream-fixture")
    git(remote, "update-ref", "refs/heads/master", base)
    with pytest.raises(RuntimeError, match="no incluye la base actual"):
        publish_snapshot(root, ["material.txt"], publish=True)
    assert git(remote, "show", f"{first['branch']}:material.txt") == "daily version"
