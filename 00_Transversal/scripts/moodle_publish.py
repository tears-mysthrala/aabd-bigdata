"""Publicar únicamente material verificado en una rama de revisión.

Usa un índice temporal y parte de la rama remota: no cambia HEAD, el índice
del usuario ni su árbol de trabajo. Nunca fuerza un push ni escribe en master.

Garantías del snapshot diario:

- La rama diaria reutilizada se valida contra la base: si contiene rutas
  ajenas al material verificado de este ciclo, la publicación se rechaza
  en lugar de heredar contaminación.
- La fusión es por ruta y falla cerrada: una ruta se publica si la rama
  no la ha cambiado desde la base; se preserva la rama si este checkout
  conserva la versión de la base; si base, rama y checkout difieren los
  tres, la publicación se rechaza (conflicto) salvo que el llamador haya
  observado estas referencias antes de verificar otra vez las fuentes.
  Esa observación solo sirve si base y rama siguen intactas al publicar.
- Cada ciclo debe pasar el conjunto gestionado completo que quiera
  preservar en la rama (el llamador real pasa siempre ``SYNC_MANAGED``).
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class PublicationObservation:
    """Estado remoto observado antes de verificar de nuevo las fuentes."""

    branch: str
    base: str
    parent: str


def observe_publication(
    root: Path, *, remote: str = "origin", base_branch: str = "master"
) -> PublicationObservation:
    """Leer ambas referencias antes de descargar, sin modificar el remoto."""
    if not remote or remote.startswith("-"):
        raise ValueError("Remoto Git inválido")
    branch = f"moodle-sync/{base_branch}/{date.today().isoformat()}"
    for name in (base_branch, branch):
        checked = subprocess.run(
            ["git", "check-ref-format", f"refs/heads/{name}"],
            cwd=root,
            capture_output=True,
            timeout=90,
        )
        if checked.returncode:
            raise ValueError("Referencia Git inválida")
    observed = subprocess.run(
        [
            "git",
            "ls-remote",
            "--heads",
            remote,
            f"refs/heads/{base_branch}",
            f"refs/heads/{branch}",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=90,
    )
    if observed.returncode:
        raise RuntimeError("No se pudo observar el remoto antes de sincronizar")
    refs = dict(line.split()[::-1] for line in observed.stdout.splitlines())
    base = refs.get(f"refs/heads/{base_branch}")
    if base is None:
        raise RuntimeError("No existe la rama remota base")
    return PublicationObservation(branch, base, refs.get(f"refs/heads/{branch}", base))


def publish_snapshot(
    root: Path,
    paths: list[str],
    *,
    remote: str = "origin",
    base_branch: str = "master",
    publish: bool = False,
    observation: PublicationObservation | None = None,
    verified_hashes: dict[str, str] | None = None,
) -> dict:
    """Preparar o publicar un snapshot acotado, también sin descargas nuevas.

    ``observation`` debe obtenerse antes de descargar/verificar las fuentes,
    nunca como forma de saltarse un conflicto al final del ciclo.
    """
    root = root.resolve()

    def git(
        *args: str,
        env: dict | None = None,
        stdin: str | None = None,
        raw: bool = False,
    ) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            env=env,
            input=stdin,
            text=True,
            capture_output=True,
            timeout=90,
        )
        if result.returncode:
            # No incluir URLs autenticadas ni la salida arbitraria del remoto.
            raise RuntimeError(f"Git {args[0]} falló (exit {result.returncode})")
        return result.stdout if raw else result.stdout.strip()

    git("check-ref-format", f"refs/heads/{base_branch}")
    if not remote or remote.startswith("-"):
        raise ValueError("Remoto Git inválido")
    safe_paths = []
    for name in sorted(set(paths)):
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or ".git" in path.parts:
            raise ValueError("Ruta de publicación fuera del material gestionado")
        target = root / path
        if not target.resolve().is_relative_to(root) or target.is_symlink():
            raise ValueError("La publicación no admite enlaces o escapes de ruta")
        if not target.is_file():
            raise ValueError("Falta un archivo gestionado; no se publican borrados")
        safe_paths.append(name)
    if not safe_paths:
        raise ValueError("No hay material verificado para publicar")
    if verified_hashes is not None and set(verified_hashes) != set(safe_paths):
        raise ValueError("Los hashes verificados no cubren todo el material gestionado")

    # FETCH_HEAD no altera la rama actual ni el índice real.
    git("fetch", "--no-tags", remote, f"refs/heads/{base_branch}")
    base = git("rev-parse", "FETCH_HEAD")
    base_tree = git("rev-parse", f"{base}^{{tree}}")
    branch = f"moodle-sync/{base_branch}/{date.today().isoformat()}"
    git("check-ref-format", f"refs/heads/{branch}")
    existing = git("ls-remote", "--heads", remote, f"refs/heads/{branch}").split()
    parent = base
    parent_tree = base_tree
    if existing:
        git("fetch", "--no-tags", remote, f"refs/heads/{branch}")
        parent = git("rev-parse", "FETCH_HEAD")
        parent_tree = git("rev-parse", f"{parent}^{{tree}}")
    if observation is not None and observation != PublicationObservation(
        branch, base, parent
    ):
        raise RuntimeError(
            "El remoto cambió durante la sincronización; repetir un ciclo fresco"
        )

    integrated = False
    if existing:
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", parent, base],
            cwd=root,
            capture_output=True,
            timeout=90,
        )
        if ancestry.returncode not in (0, 1):
            raise RuntimeError("No se pudo verificar la integración de la rama diaria")
        integrated = ancestry.returncode == 0
        if integrated:
            # La PR ya se integró; las siguientes novedades parten de master.
            # master conserva el tip diario como ancestro: el push sigue siendo FF.
            parent, parent_tree = base, base_tree
        includes_base = subprocess.run(
            ["git", "merge-base", "--is-ancestor", base, parent],
            cwd=root,
            capture_output=True,
            timeout=90,
        )
        if includes_base.returncode:
            raise RuntimeError(
                "La rama diaria no incluye la base actual; reconciliar antes de publicar"
            )
        inherited = git(
            "diff",
            "--no-renames",
            "--name-only",
            "-z",
            base_tree,
            parent_tree,
            raw=True,
        ).split("\0")[:-1]
        outside = sorted(set(inherited) - set(safe_paths))
        if outside:
            raise RuntimeError(
                "La rama diaria contiene cambios ajenos al material "
                "verificado: " + ", ".join(outside)
            )

    if existing and inherited:
        entries = git(
            "ls-tree",
            "-z",
            parent,
            "--",
            *inherited,
            env=dict(os.environ, GIT_LITERAL_PATHSPECS="1"),
            raw=True,
        ).split("\0")
        for entry in filter(None, entries):
            mode, kind, _ = entry.split("\t", 1)[0].split()
            if mode not in {"100644", "100755"} or kind != "blob":
                raise RuntimeError(
                    "Tipo de entrada heredada no admitido en la rama diaria"
                )

    def blob(rev: str, name: str) -> str | None:
        try:
            return git("rev-parse", f"{rev}:{name}")
        except RuntimeError:
            return None

    with tempfile.TemporaryDirectory(prefix="moodle-index-") as temporary:
        env = dict(
            os.environ,
            GIT_INDEX_FILE=str(Path(temporary) / "index"),
            GIT_LITERAL_PATHSPECS="1",
        )
        git("read-tree", parent, env=env)
        git("add", "--", *safe_paths, env=env)
        preserved = []
        for name in safe_paths:
            staged = git("rev-parse", f":{name}", env=env)
            tip = blob(parent, name)
            original = blob(base, name)
            if staged == tip:
                continue
            if tip is None and original is not None:
                raise RuntimeError(
                    "La rama diaria eliminó material gestionado: " + name
                )
            if tip == original:
                continue  # La rama no tocó esta ruta; publicar el trabajo.
            if staged == original:
                # Copia desfasada: la rama avanzó y este checkout conserva
                # la versión de la base. No revertir; conservar lo publicado.
                git("restore", "--source", parent, "--staged", "--", name, env=env)
                preserved.append(name)
                continue
            if observation is not None:
                # Las fuentes se verificaron después de observar este tip y
                # el remoto no ha avanzado. Hay causalidad para este ciclo.
                continue
            # Tres versiones distintas (base, rama y checkout): el orden
            # causal no puede probarse y asumir "actualización secuencial"
            # podría revertir material más nuevo. Fallar cerrado y exigir
            # una sincronización nueva antes de reintentar.
            raise RuntimeError(
                "Conflicto de publicación en " + name + ": base, rama diaria"
                " y checkout difieren; sincroniza de nuevo y reintenta"
            )
        if verified_hashes is not None:
            for name in safe_paths:
                staged = git("rev-parse", f":{name}", env=env)
                content = subprocess.run(
                    ["git", "cat-file", "blob", staged],
                    cwd=root,
                    capture_output=True,
                    timeout=90,
                )
                if (
                    content.returncode
                    or hashlib.sha256(content.stdout).hexdigest()
                    != verified_hashes[name]
                ):
                    raise RuntimeError(
                        "El snapshot no coincide con el material verificado: " + name
                    )
        tree = git("write-tree", env=env)
    if tree == parent_tree:
        if existing and not integrated:
            return {
                "status": "published",
                "branch": branch,
                "commit": parent,
                "base": base,
                "tree": tree,
                "paths": [],
                "preserved": sorted(preserved),
            }
        return {"status": "current", "base": base, "tree": tree, "preserved": []}

    changed = git("diff", "--name-only", "-z", parent_tree, tree, raw=True).split("\0")[
        :-1
    ]
    if not set(changed).issubset(set(safe_paths)):
        raise RuntimeError("El snapshot incluye cambios ajenos al material verificado")
    if existing:
        message = (
            "Moodle: actualizar material verificado\n\n" + "\n".join(changed) + "\n"
        )
        commit = git("commit-tree", tree, "-p", parent, stdin=message)
    else:
        message = (
            "Moodle: actualizar material verificado\n\n" + "\n".join(changed) + "\n"
        )
        commit = git("commit-tree", tree, "-p", base, stdin=message)
    result = {
        "status": "prepared",
        "branch": branch,
        "commit": commit,
        "base": base,
        "tree": tree,
        "paths": changed,
        "preserved": sorted(preserved),
    }
    if publish:
        refspec = f"{commit}:refs/heads/{branch}"
        git("push", remote, refspec)
        observed = git("ls-remote", "--heads", remote, f"refs/heads/{branch}").split()
        if not observed or observed[0] != commit:
            raise RuntimeError("No se pudo verificar el commit publicado")
        result["status"] = "published"
    return result
