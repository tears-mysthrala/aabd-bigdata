"""Publicar únicamente material verificado en una rama de revisión.

Usa un índice temporal y parte de la rama remota: no cambia HEAD, el índice
del usuario ni su árbol de trabajo. Nunca fuerza un push ni escribe en master.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from datetime import date
from pathlib import Path


def publish_snapshot(
    root: Path,
    paths: list[str],
    *,
    remote: str = "origin",
    base_branch: str = "master",
    publish: bool = False,
) -> dict:
    """Preparar o publicar un snapshot acotado, también sin descargas nuevas."""
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

    # FETCH_HEAD no altera la rama actual ni el índice real.
    git("fetch", "--no-tags", remote, f"refs/heads/{base_branch}")
    base = git("rev-parse", "FETCH_HEAD")
    branch = f"moodle-sync/{base_branch}/{date.today().isoformat()}"
    git("check-ref-format", f"refs/heads/{branch}")
    existing = git("ls-remote", "--heads", remote, f"refs/heads/{branch}").split()
    parent = base
    if existing:
        parent = existing[0]
        git("fetch", "--no-tags", remote, f"refs/heads/{branch}")
    parent_tree = git("rev-parse", f"{parent}^{{tree}}")
    with tempfile.TemporaryDirectory(prefix="moodle-index-") as temporary:
        env = dict(
            os.environ,
            GIT_INDEX_FILE=str(Path(temporary) / "index"),
            GIT_LITERAL_PATHSPECS="1",
        )
        git("read-tree", parent, env=env)
        git("add", "--", *safe_paths, env=env)
        tree = git("write-tree", env=env)
    if tree == parent_tree:
        if existing:
            return {
                "status": "published",
                "branch": branch,
                "commit": parent,
                "base": base,
                "tree": tree,
                "paths": [],
            }
        return {"status": "current", "base": base, "tree": tree}

    changed = git("diff", "--name-only", "-z", parent_tree, tree, raw=True).split("\0")[
        :-1
    ]
    if not set(changed).issubset(set(safe_paths)):
        raise RuntimeError("El snapshot incluye cambios ajenos al material verificado")
    if existing:
        message = "Moodle: actualizar material verificado\n\n" + "\n".join(changed) + "\n"
        commit = git("commit-tree", tree, "-p", parent, stdin=message)
    else:
        message = "Moodle: actualizar material verificado\n\n" + "\n".join(changed) + "\n"
        commit = git("commit-tree", tree, "-p", base, stdin=message)
    result = {
        "status": "prepared",
        "branch": branch,
        "commit": commit,
        "base": base,
        "tree": tree,
        "paths": changed,
    }
    if publish:
        refspec = f"{commit}:refs/heads/{branch}"
        git("push", remote, refspec)
        observed = git("ls-remote", "--heads", remote, f"refs/heads/{branch}").split()
        if not observed or observed[0] != commit:
            raise RuntimeError("No se pudo verificar el commit publicado")
        result["status"] = "published"
    return result
