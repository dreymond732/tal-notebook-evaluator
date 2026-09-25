"""Prepare a private, audited history rewrite; publish only on explicit request."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

RESOURCE_COMMIT = "7b34850800a5310b42a00590fefac2c54d2a1395"
RESOURCE_PATH = "Notebooks TD/S3/ressources/"
PLACEHOLDER = b"example.invalid"


def run(*args, cwd=None, data=None):
    result = subprocess.run(args, cwd=cwd, input=data, capture_output=True)
    if result.returncode:
        # Commands and stderr can contain private addresses or authenticated URLs.
        operation = "git " + (args[3] if len(args) > 3 and args[1] == "-C" else args[1]) if args[0] == "git" else "filtrage Git"
        raise RuntimeError(f"Échec de {operation} ; vérifier accès, protections et dépendances. Aucune adresse affichée.")
    return result.stdout


def git(repo, *args, data=None):
    return run("git", "-C", str(repo), *args, data=data)


def refs_at(source):
    output = run("git", "ls-remote", "--heads", "--tags", str(source))
    return {ref: oid for oid, ref in (line.split() for line in output.decode().splitlines())
            if not ref.endswith("^{}")}


def local_refs(repo):
    output = git(repo, "for-each-ref", "--format=%(objectname) %(refname)", "refs/heads", "refs/tags")
    return dict((ref, oid) for oid, ref in (line.split() for line in output.decode().splitlines()))


def private_hosts(path):
    raw = Path(path).read_text(encoding="utf-8") if path else os.environ.get("TAL_PRIVATE_HOSTS", "")
    items = json.loads(raw) if raw.lstrip().startswith("[") else re.split(r"[\s,]+", raw)
    hosts = [item.strip().lower() for item in items if item.strip()]
    if not hosts or any(not re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", host) for host in hosts):
        raise ValueError("Fournir uniquement des noms de domaine via --hosts-file ou TAL_PRIVATE_HOSTS.")
    if "example.invalid" in hosts:
        raise ValueError("Le domaine de remplacement ne peut pas être une cible.")
    return sorted(set(hosts))


def transform(data, hosts, pin=None):
    for host in hosts:
        data = re.sub(re.escape(host.encode()), PLACEHOLDER, data, flags=re.I)
    if pin:
        data = data.replace(pin[0].encode(), pin[1].encode())
    return data


def tree_entries(repo, commit):
    entries = {}
    for line in git(repo, "ls-tree", "-rz", commit).split(b"\0"):
        if not line:
            continue
        header, path = line.split(b"\t", 1)
        mode, kind, oid = header.decode().split()
        entries[path] = (mode, kind, oid)
    return entries


def unsigned_commit(raw):
    header, sep, message = raw.partition(b"\n\n")
    lines = []
    skipping = False
    for line in header.splitlines():
        if not line.startswith(b" "):
            skipping = line.startswith((b"gpgsig ", b"gpgsig-sha256 ", b"mergetag "))
        if not skipping:
            lines.append(line)
    return b"\n".join(lines) + sep + message


def snapshot(repo, hosts):
    commits = git(repo, "rev-list", "--all").decode().splitlines()
    records, blobs = {}, {}
    for oid in commits:
        raw = git(repo, "cat-file", "commit", oid)
        entries = tree_entries(repo, oid)
        records[oid] = (raw, entries)
        for _, kind, blob in entries.values():
            if kind == "blob" and blob not in blobs:
                blobs[blob] = git(repo, "cat-file", "blob", blob)
    return records, blobs


def filter_pass(repo, replacements):
    with tempfile.NamedTemporaryFile(delete=False) as stream:
        filename = Path(stream.name)
        stream.write(replacements)
    try:
        run(sys.executable, "-m", "git_filter_repo", "--force", "--replace-text", str(filename),
            "--replace-message", str(filename), "--preserve-commit-hashes", "--prune-empty", "never",
            "--prune-degenerate", "never", cwd=repo)
    finally:
        filename.unlink(missing_ok=True)
    mapping_file = Path(repo) / "filter-repo" / "commit-map"
    return dict(line.split() for line in mapping_file.read_text().splitlines()[1:])


def audit(repo, records, blobs, mapping, hosts, pin, resource_commit):
    actual = set(git(repo, "rev-list", "--all").decode().splitlines())
    if actual != set(mapping.values()) or len(actual) != len(records):
        raise RuntimeError("Le nombre ou l'identité des commits accessibles a changé de façon inattendue.")
    expected_blobs = {}
    for oid, content in blobs.items():
        expected_blobs[oid] = run("git", "hash-object", "--stdin", data=transform(content, hosts, pin)).decode().strip()
    signatures = 0
    for old, (raw, entries) in records.items():
        new = mapping[old]
        new_raw = git(repo, "cat-file", "commit", new)
        old_header, _, old_message = unsigned_commit(raw).partition(b"\n\n")
        new_header, _, new_message = unsigned_commit(new_raw).partition(b"\n\n")
        expected_header = []
        for line in old_header.splitlines():
            if line.startswith(b"tree "):
                continue
            if line.startswith(b"parent "):
                line = b"parent " + mapping[line[7:].decode()].encode()
            expected_header.append(line)
        comparable = [line for line in new_header.splitlines() if not line.startswith(b"tree ")]
        if expected_header != comparable or new_message != transform(old_message, hosts, pin):
            raise RuntimeError("Métadonnées, parents ou message de commit non conformes.")
        signatures += int(b"\ngpgsig " in raw or b"\ngpgsig-sha256 " in raw)
        new_entries = tree_entries(repo, new)
        expected = {path: (mode, kind, expected_blobs[oid] if kind == "blob" else oid)
                    for path, (mode, kind, oid) in entries.items()}
        if new_entries != expected:
            raise RuntimeError("Une arborescence ou un contenu a changé hors des substitutions autorisées.")
        for path, item in entries.items():
            if path.startswith(RESOURCE_PATH.encode()) and new_entries[path] != item:
                raise RuntimeError("Une ressource pédagogique a été modifiée.")
    objects = git(repo, "rev-list", "--objects", "--all").splitlines()
    for entry in objects:
        oid = entry.split(b" ", 1)[0].decode()
        kind = git(repo, "cat-file", "-t", oid).decode().strip()
        data = git(repo, "cat-file", kind, oid)
        if any(host.encode() in data.lower() for host in hosts):
            raise RuntimeError("Une adresse ciblée subsiste dans un objet accessible.")
    git(repo, "fsck", "--no-reflogs", "--full")
    return {"commits": len(records), "blob_versions": len(blobs), "signatures_removed": signatures,
            "resource_commit": mapping[resource_commit]}


def discover_hosts(records, blobs):
    """Discover only deposit instructions in two known historical subjects."""
    allowed = {b"Notebooks contr\xc3\xb4les finaux/DevoirS1.ipynb",
               b"Notebooks TD/S3/TD0_S3_diagnostic_texte.ipynb"}
    candidates = set()
    visited = set()
    for _, entries in records.values():
        for path, (_, kind, oid) in entries.items():
            if path not in allowed or kind != "blob" or oid in visited:
                continue
            visited.add(oid)
            notebook = json.loads(blobs[oid])
            for cell in notebook.get("cells", []):
                source = cell.get("source", [])
                text = source if isinstance(source, str) else "".join(source)
                if cell.get("cell_type") != "markdown" or not re.search(
                        r"dép[oô]t|dépos|auto.?évaluation|auto.?evaluation", text, re.I):
                    continue
                for url in re.findall(r'https?://[^\s<>"\)]+', text):
                    parsed = urlsplit(url)
                    host = parsed.hostname or ""
                    if parsed.path not in {"/controleur/", "/universite/tal/"}:
                        continue
                    if host in {"localhost", "github.com", "raw.githubusercontent.com"}:
                        continue
                    if re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", host) and host != "example.invalid":
                        candidates.add(host)
    if not candidates:
        raise ValueError("Aucun domaine de dépôt découvert ; utiliser --hosts-file.")
    return sorted(candidates)


def prepare(source, output, hosts, resource_commit=RESOURCE_COMMIT, discover=False):
    output = Path(output).resolve()
    if output.exists():
        raise ValueError("Le dossier de sortie doit être nouveau.")
    # Refuse a private backup inside any existing working tree.
    for parent in output.parents:
        if (parent / ".git").exists():
            raise ValueError("Choisir un dossier de sortie hors de tout dépôt Git.")
    old_refs = refs_at(source)
    if not old_refs or not any(ref.startswith("refs/heads/") for ref in old_refs):
        raise ValueError("Aucune branche source disponible.")
    output.mkdir(parents=True, mode=0o700)
    repo = output / "rewritten.git"
    run("git", "init", "--bare", str(repo))
    git(repo, "fetch", "--no-tags", str(source), "+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*")
    if local_refs(repo) != old_refs:
        raise RuntimeError("La source a changé pendant sa copie ; recommencer dans un nouveau dossier.")
    # Annotated tags require their own metadata/signature audit, deliberately unsupported.
    if any(git(repo, "cat-file", "-t", oid).strip() == b"tag" for oid in old_refs.values()):
        raise ValueError("Les tags annotés nécessitent une revue dédiée ; aucune réécriture effectuée.")
    git(repo, "bundle", "create", str(output / "original.bundle"), "--all")
    (output / "original-refs.json").write_text(json.dumps(old_refs, indent=2) + "\n")
    records, blobs = snapshot(repo, hosts)
    if discover:
        hosts = sorted(set(hosts) | set(discover_hosts(records, blobs)))
    if not hosts:
        raise ValueError("Aucun domaine cible fourni.")
    if resource_commit not in records:
        raise ValueError("Commit des ressources introuvable dans les branches/tags copiés.")
    rules = b"".join(b"regex:(?i)" + re.escape(host.encode()) + b"==>" + PLACEHOLDER + b"\n" for host in hosts)
    first = filter_pass(repo, rules)
    new_resource = first[resource_commit]
    # Run 2 separately: filter-repo otherwise composes commit-map across successive invocations.
    prior_filter = repo / "filter-repo"
    prior_filter.rename(output / "first-pass-mapping")
    second = filter_pass(repo, resource_commit.encode() + b"==>" + new_resource.encode() + b"\n")
    if second[new_resource] != new_resource:
        raise RuntimeError("La seconde passe change le commit des ressources : référence circulaire.")
    mapping = {old: second[new] for old, new in first.items()}
    report = audit(repo, records, blobs, mapping, hosts, (resource_commit, new_resource), resource_commit)
    new_refs = local_refs(repo)
    if set(new_refs) != set(old_refs):
        raise RuntimeError("Des références ont été créées ou supprimées.")
    for ref, old in old_refs.items():
        if new_refs[ref] != mapping[old]:
            raise RuntimeError("Référence remappée incorrectement.")
    bundle = output / "cleaned.bundle"
    git(repo, "bundle", "create", str(bundle), "--all")
    manifest = {"format": 1, "old_refs": old_refs, "new_refs": new_refs,
                "bundle_sha256": hashlib.sha256(bundle.read_bytes()).hexdigest(), "audit": report}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (output / "commit-map.json").write_text(json.dumps(mapping, indent=2) + "\n")
    return report


def publish(output, remote):
    output = Path(output).resolve()
    manifest = json.loads((output / "manifest.json").read_text())
    bundle = output / "cleaned.bundle"
    if hashlib.sha256(bundle.read_bytes()).hexdigest() != manifest["bundle_sha256"]:
        raise RuntimeError("Le bundle a changé depuis son audit.")
    if refs_at(remote) != manifest["old_refs"]:
        raise RuntimeError("Les branches/tags distants ont changé : préparer de nouveau, sans forcer.")
    with tempfile.TemporaryDirectory(prefix="tal-publish-") as directory:
        repo = Path(directory) / "publish.git"
        run("git", "clone", "--mirror", str(bundle), str(repo))
        if local_refs(repo) != manifest["new_refs"]:
            raise RuntimeError("Les références du bundle ne correspondent pas à l'audit.")
        refs = sorted(manifest["old_refs"])
        leases = ["--force-with-lease=" + ref + ":" + manifest["old_refs"][ref] for ref in refs]
        git(repo, "push", "--atomic", *leases, remote, *(ref + ":" + ref for ref in refs))
    if refs_at(remote) != manifest["new_refs"]:
        raise RuntimeError("Publication effectuée, mais références distantes à vérifier.")
    return {"published_refs": len(manifest["new_refs"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    preparation = commands.add_parser("prepare")
    preparation.add_argument("--source", required=True)
    preparation.add_argument("--output", required=True)
    preparation.add_argument("--hosts-file")
    preparation.add_argument("--discover-deposit-hosts", action="store_true")
    preparation.add_argument("--resource-commit", default=RESOURCE_COMMIT)
    publication = commands.add_parser("publish")
    publication.add_argument("--output", required=True)
    publication.add_argument("--remote", required=True)
    args = parser.parse_args()
    try:
        result = (prepare(args.source, args.output, [] if args.discover_deposit_hosts and not args.hosts_file else private_hosts(args.hosts_file), args.resource_commit, args.discover_deposit_hosts)
                  if args.command == "prepare" else publish(args.output, args.remote))
    except (RuntimeError, ValueError, OSError, KeyError) as exc:
        parser.exit(1, str(exc) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
