"""Generate distributable TAL notebooks; never rewrite course sources."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit

from notebook_contract import load_catalog, resolve_notebook

ROOT = Path(__file__).resolve().parents[1]
CELL_ID = "tal-submission"
URL_PLACEHOLDER = "__TAL_PUBLIC_URL__"
MANIFEST = ".tal-distribution.json"
URL_RE = re.compile(r"https?://[^\s<>\"'\\]+", re.I)


def public_url(value=None, env_file=None):
    """Read only TAL_PUBLIC_URL, without executing/interpolating a dotenv file."""
    raw = value if value is not None else os.environ.get("TAL_PUBLIC_URL")
    if raw is None and env_file:
        for line in Path(env_file).read_text(encoding="utf-8-sig").splitlines():
            key, sep, candidate = line.strip().partition("=")
            if sep and key.strip() == "TAL_PUBLIC_URL":
                if raw is not None:
                    raise ValueError("TAL_PUBLIC_URL est définie plusieurs fois.")
                raw = candidate.strip()
                if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
                    raw = raw[1:-1]
    if not raw or not isinstance(raw, str):
        raise ValueError("Définissez TAL_PUBLIC_URL dans l’environnement ou le fichier .env.")
    raw = raw.strip()
    if any(c.isspace() or ord(c) < 32 for c in raw) or any(c in raw for c in '\\<>\"\'`${}'):
        raise ValueError("TAL_PUBLIC_URL contient des caractères interdits.")
    try:
        parsed = urlsplit(raw)
        parsed.port
    except ValueError as exc:
        raise ValueError("TAL_PUBLIC_URL est invalide.") from exc
    if (parsed.scheme not in {"http", "https"} or not parsed.hostname
            or parsed.username is not None or parsed.password is not None
            or parsed.query or parsed.fragment):
        raise ValueError("TAL_PUBLIC_URL doit être une URL HTTP(S), sans identifiants, paramètres ni fragment.")
    if parsed.path.rstrip("/").endswith("/submit"):
        raise ValueError("TAL_PUBLIC_URL désigne la racine de l’application, sans /submit.")
    return raw.rstrip("/")


def check_source(notebook, expected_url=None):
    """Inspect all fields, including saved HTML outputs, for a deposit address."""
    raw = json.dumps(notebook, ensure_ascii=False)
    expected_host = urlsplit(expected_url).hostname if expected_url else None
    for match in URL_RE.finditer(raw):
        parsed = urlsplit(match.group())
        if (expected_host and parsed.hostname == expected_host) or re.search(
                r"/(?:universite/tal|submit|eval)(?:/|$)", parsed.path, re.I):
            raise ValueError("Une adresse de dépôt est présente dans un notebook source.")
    cells = notebook.get("cells", [])
    candidates = [i for i, cell in enumerate(cells)
                  if cell.get("id") == CELL_ID
                  or cell.get("metadata", {}).get("tal", {}).get("role") == "submission"
                  or cell.get("metadata", {}).get("tal", {}).get("question") == "submission"]
    if candidates:
        if candidates != [len(cells) - 1] or cells[-1] != submission_cell():
            raise ValueError("La cellule source de restitution doit être unique, finale et canonique, sans sortie.")
    # A placeholder elsewhere must never silently survive into the student copy.
    remaining = copy.deepcopy(notebook)
    if candidates:
        remaining["cells"].pop()
    if URL_PLACEHOLDER in json.dumps(remaining, ensure_ascii=False):
        raise ValueError("Le marqueur URL est réservé à la cellule finale de restitution.")


def submission_cell(base_url=URL_PLACEHOLDER):
    """Canonical source cell, or the same cell with a validated deployment URL."""
    if base_url != URL_PLACEHOLDER:
        base_url = public_url(base_url)
    code = ('# Restitution — (URL injectée lors du déploiement)\n'
            'from IPython.display import display, HTML\n'
            'from html import escape\n'
            f'URL_SOUMISSION = {json.dumps(base_url, ensure_ascii=False)}.rstrip("/") + "/submit"\n\n'
            'display(HTML(f"""\n'
            '<div style="padding:20px;border:2px solid #005a9c;border-radius:8px;background:#f8f9fa">\n'
            '<h3>Restitution de votre travail</h3>\n'
            '<ol>\n'
            '<li>Vérifiez que toutes les cellules ont été exécutées.</li>\n'
            '<li>Téléchargez votre notebook au format <code>.ipynb</code> (menu Fichier).</li>\n'
            '<li>Déposez ce fichier sur le serveur.</li>\n'
            '</ol>\n'
            '<p style="text-align:center"><a href="{escape(URL_SOUMISSION, quote=True)}" target="_blank" rel="noopener noreferrer"><strong>Accéder au serveur de dépôt</strong></a></p>\n'
            '</div>\n'
            '"""))\n')
    return {"cell_type": "code", "id": CELL_ID,
            "metadata": {"tal": {"question": "submission", "role": "submission"}},
            "source": code.splitlines(keepends=True), "execution_count": None, "outputs": []}


def distributable(notebook, base_url):
    """Replace a canonical source placeholder, or append a cell for older sources."""
    check_source(notebook, base_url)
    rendered = copy.deepcopy(notebook)
    if rendered["cells"] and rendered["cells"][-1].get("id") == CELL_ID:
        rendered["cells"][-1] = submission_cell(base_url)
    else:
        rendered["cells"].append(submission_cell(base_url))
    return rendered


def active_sources(root=ROOT):
    for entry in load_catalog():
        if entry["active"]:
            yield entry, root / entry["notebook"]


def check_sources(root=ROOT, expected_url=None):
    count = 0
    for entry, source in active_sources(root):
        nb = json.loads(source.read_text(encoding="utf-8"))
        resolved = resolve_notebook(nb)
        if resolved["id"] != entry["id"]:
            raise ValueError(f"Identité incohérente : {entry['notebook']}")
        check_source(nb, expected_url)
        if entry["semester"] in {"S1", "S3"} and entry["mode"] == "td":
            if not nb["cells"] or nb["cells"][-1] != submission_cell():
                raise ValueError(f"Cellule source de restitution absente : {entry['notebook']}")
        count += 1
    return count


def verify_rendered(output, base_url, root=ROOT):
    base_url = public_url(base_url)
    count = 0
    for entry, source in active_sources(root):
        original = json.loads(source.read_text(encoding="utf-8"))
        rendered = json.loads((output / entry["notebook"]).read_text(encoding="utf-8"))
        expected = distributable(original, base_url)
        if rendered != expected:
            raise ValueError(f"Copie distribuable incohérente : {entry['notebook']}")
        count += 1
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*.ipynb")}
    allowed = {entry["notebook"] for entry, _ in active_sources(root)}
    if actual != allowed:
        raise ValueError("La distribution contient des notebooks manquants ou non autorisés.")
    return count


def render(output, base_url, root=ROOT):
    """Validate a complete temporary distribution before replacing the previous one."""
    base_url = public_url(base_url)
    if output.is_symlink():
        raise ValueError("Le répertoire de distribution ne doit pas être un lien symbolique.")
    output = output.resolve()
    root = root.resolve()
    if output == root or output in root.parents:
        raise ValueError("Le répertoire de distribution ne doit pas remplacer le projet.")
    if output.is_relative_to(root) and not output.is_relative_to(root / "dist"):
        raise ValueError("Dans le projet, la distribution doit rester sous dist/.")
    if output.exists():
        if not output.is_dir():
            raise ValueError("La destination existe et n’est pas un répertoire.")
        marker = output / MANIFEST
        try:
            previous = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raise ValueError("La destination existe mais n’est pas une distribution TAL reconnue.") from None
        if (not isinstance(previous, dict) or previous.get("format") != "tal-distribution-v1"
                or not isinstance(previous.get("notebooks"), list)
                or not all(isinstance(p, str) and p.endswith(".ipynb") and not Path(p).is_absolute()
                           and ".." not in Path(p).parts for p in previous["notebooks"])):
            raise ValueError("Le manifeste de distribution existant est invalide.")
        contents = list(output.rglob("*"))
        if any(p.is_symlink() for p in contents):
            raise ValueError("La distribution existante contient un lien symbolique.")
        allowed = set(previous["notebooks"]) | {MANIFEST}
        if any(p.relative_to(output).as_posix() not in allowed for p in contents if p.is_file()):
            raise ValueError("La distribution contient des fichiers étrangers : remplacement refusé.")
    check_sources(root, base_url)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".tal-dist-", dir=output.parent))
    backup = None
    try:
        for entry, source in active_sources(root):
            nb = json.loads(source.read_text(encoding="utf-8"))
            nb = distributable(nb, base_url)
            target = temporary / entry["notebook"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        count = verify_rendered(temporary, base_url, root)
        (temporary / MANIFEST).write_text(json.dumps({
            "format": "tal-distribution-v1",
            "notebooks": [entry["notebook"] for entry, _ in active_sources(root)],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if output.exists():
            backup = Path(tempfile.mkdtemp(prefix=".tal-previous-", dir=output.parent))
            backup.rmdir()
            output.rename(backup)
        try:
            temporary.rename(output)
        except OSError:
            if backup:
                backup.rename(output)
            raise
        if backup:
            shutil.rmtree(backup)
        return count
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "render", "verify"))
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check":
            count = check_sources()
        else:
            url = public_url(env_file=args.env_file)
            count = (render(args.output_dir, url) if args.command == "render"
                     else verify_rendered(args.output_dir, url))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Préparation refusée : {exc}\n")
    print(f"{count} notebooks : {args.command} OK")


if __name__ == "__main__":
    main()
