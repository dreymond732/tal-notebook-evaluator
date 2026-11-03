"""Migration S1 du stockage #35 vers S1_TDn[_A/B/C], sans suppression.

Simulation par défaut. --apply exige un engagement explicite de sauvegarde.
Les sources et les preuves de chaque tentative demeurent intactes ; les
lignes copiées reçoivent un marqueur de provenance stable pour l'idempotence.
Ne pas exécuter en parallèle de travailleurs de correction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path

import outils
from notebook_contract import load_catalog
from progression import progression_lock, refresh_progression
from storage_layout import GRADE_COLUMNS, legacy_storage_id, storage_id

PREFIX = "migration-s1-v2:"
SUBDIRS = ("nb", "rapport")
YEAR = "2026-2027"


def _hash(path):
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(piece)
    return sha.hexdigest()


def _regular(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("Fichier non régulier ou lien symbolique : " + str(path))


def _directory(path):
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise ValueError("Dossier inattendu ou lien symbolique : " + str(path))


def _csv_rows(path):
    if not path.exists():
        return []
    _regular(path)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        if reader.fieldnames != list(GRADE_COLUMNS):
            raise ValueError("CSV incompatible avec le schéma consolidé : " + str(path))
        records = list(reader)
    if any(None in row or len(row) != len(GRADE_COLUMNS)
           or any(type(v) is not str for v in row.values()) for row in records):
        raise ValueError("CSV avec ligne incomplète : " + str(path))
    return records


def _identity(row):
    return tuple(row[field] for field in GRADE_COLUMNS)


def _marker(source, index, row):
    # L'ancien marqueur direct:uuid ou migration:... est conservé en suffixe.
    # Index et chemin du dossier (constant) rendent chaque essai distinct,
    # même si plusieurs lignes ont des scores et dates identiques.
    return PREFIX + source.name + ":" + str(index) + ":" + row["Origine"]


def _stamped(row, source, index):
    stamped = dict(row)
    stamped["Origine"] = _marker(source, index, row)
    return stamped


def _files(source, target):
    """Planifier un rapprochement sans écraser deux archives différentes."""
    planned = []
    seen = {}
    for sub in SUBDIRS:
        old = source / sub
        dest = target / sub
        _directory(old)
        _directory(dest)
        if dest.exists():
            for existing in dest.iterdir():
                _regular(existing)
        if not old.exists():
            continue
        for artifact in sorted(old.iterdir()):
            _regular(artifact)
            if artifact.suffix.lower() not in ((".ipynb",) if sub == "nb" else (".html",)):
                raise ValueError("Extension d'archive inattendue : " + str(artifact))
            digest = _hash(artifact)
            proposed = dest / artifact.name
            if proposed.exists():
                _regular(proposed)
                if _hash(proposed) == digest:
                    continue
                # Nom stable y compris à la deuxième exécution.
                salt = hashlib.sha256(
                    (source.name + "/" + sub + "/" + artifact.name).encode()
                ).hexdigest()[:16]
                proposed = dest / (artifact.stem + "__s1_source_" + salt + artifact.suffix)
            if proposed in seen:
                if seen[proposed] == digest:
                    continue
                raise ValueError("Collision d'archives multiples : " + str(proposed))
            if proposed.exists():
                _regular(proposed)
                if _hash(proposed) == digest:
                    continue
                raise ValueError("Collision d'archives non résolue : " + str(proposed))
            seen[proposed] = digest
            planned.append((artifact, proposed, digest))
    return planned


def _entry_plan(root, evaluator):
    old_name = legacy_storage_id(evaluator)
    new_name = storage_id(evaluator)
    if old_name == new_name:
        raise ValueError("Migration non applicable à " + evaluator)
    source = root / old_name
    target = root / new_name
    _directory(source)
    _directory(target)
    for folder, expected in ((source, "notes_" + old_name + ".csv"),
                             (target, "notes_" + new_name + ".csv")):
        if folder.exists():
            allowed = set(SUBDIRS) | {expected}
            for entry in folder.iterdir():
                if entry.is_symlink() or entry.name not in allowed:
                    raise ValueError("Contenu imprévu dans " + str(folder) + " : " + entry.name)
                if entry.name in SUBDIRS:
                    _directory(entry)
                else:
                    _regular(entry)
    old_csv = source / ("notes_" + old_name + ".csv")
    new_csv = target / ("notes_" + new_name + ".csv")
    source_rows = _csv_rows(old_csv)
    existing_rows = _csv_rows(new_csv)
    imported = {}
    for row in existing_rows:
        marker = row["Origine"]
        if marker.startswith(PREFIX):
            if marker in imported:
                raise ValueError("Marqueur de migration dupliqué : " + marker)
            imported[marker] = row

    additions = []
    matched = 0
    seen = set()
    for i, row in enumerate(source_rows, 2):
        new_row = _stamped(row, source, i)
        marker = new_row["Origine"]
        if marker in seen:
            raise ValueError("Marqueur source répété : " + marker)
        seen.add(marker)
        if marker in imported:
            if imported[marker] != new_row:
                raise ValueError("Journal source modifié depuis la migration : " + old_name)
            matched += 1
        else:
            if any(existing == row for existing in existing_rows):
                # Même enregistrement déjà présent sans marqueur : impossible
                # de savoir si indépendant ou copié manuellement.
                raise ValueError("Copie sans provenance détectée : " + old_name)
            additions.append(new_row)
    # Les marqueurs déjà importés de ce dossier doivent toujours avoir une
    # origine correspondante : une source disparue n'est pas oubliée.
    old_prefix = PREFIX + old_name + ":"
    orphan_markers = [p for p in imported if p.startswith(old_prefix) and p not in seen]
    if orphan_markers:
        raise ValueError("Tentatives sources disparues : " + old_name)

    files = _files(source, target)
    return {
        "evaluator": evaluator, "source": source, "target": target,
        "old_csv": old_csv, "new_csv": new_csv,
        "source_rows": len(source_rows), "existing": existing_rows,
        "additions": additions, "matched": matched,
        "files": files,
    }


def prepare(root):
    root = Path(root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Volume soumissions absent : " + str(root))
    _directory(root / "suivi")
    entries = [x["evaluator"] for x in load_catalog()
               if x["active"] and x["evaluator"]
               and x["semester"] == "S1"
               and x["notebook"].startswith("Notebooks TD/S1/")]
    if len(entries) != 19 or len(set(entries)) != 19:
        raise ValueError("Le catalogue ne contient plus exactement les 19 TD du S1")
    plans = [_entry_plan(root, name) for name in entries]
    old_names = [p["source"].name for p in plans]
    new_names = [p["target"].name for p in plans]
    if len(set(old_names)) != 19 or len(set(new_names)) != 19:
        raise ValueError("Collision de noms physiques")
    return plans


def _atomic_csv(path, rows):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent,
            prefix=".migration-s1-", delete=False
        ) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=GRADE_COLUMNS, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _copy(src, dst, expected):
    """Publication atomique et sans écrasement ; résiste à une interruption."""
    dst.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=dst.parent, prefix=".copie-s1-",
                                         delete=False) as output:
            temporary = Path(output.name)
            with src.open("rb") as inp:
                shutil.copyfileobj(inp, output)
            output.flush()
            os.fsync(output.fileno())
        if _hash(temporary) != expected:
            raise ValueError("Copie interrompue ou altérée : " + str(src))
        os.chmod(temporary, 0o600)
        try:
            os.link(temporary, dst)  # exclusivité, pas de remplacement
        except FileExistsError:
            if _hash(dst) != expected:
                raise ValueError("Destination différente : " + str(dst))
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _summary(plans):
    return {
        "evaluations_s1": len(plans),
        "dossiers_sources_presents": sum(p["source"].exists() for p in plans),
        "lignes_sources": sum(p["source_rows"] for p in plans),
        "lignes_deja_importees": sum(p["matched"] for p in plans),
        "nouvelles_lignes": sum(len(p["additions"]) for p in plans),
        "fichiers_a_copier": sum(len(p["files"]) for p in plans),
        "journaux_a_actualiser": sum(bool(p["additions"]) for p in plans),
    }


def execute(root=None, apply=False, backup_confirmed=False, year=None):
    root = Path(root if root is not None else outils.BASE_DIR)
    if not apply:
        # Préparation pure : aucun verrou ou fichier ajouté dans soumissions/.
        result = _summary(prepare(root))
        result["mode"] = "SIMULATION"
        return result
    if not backup_confirmed:
        raise ValueError("Effectuer une sauvegarde indépendante, puis fournir --backup-confirmed")
    with progression_lock(root):
        plans = prepare(root)  # relecture sous verrou
        result = _summary(plans)
        result["mode"] = "APPLICATION"
        for entry in plans:
            for source, target, digest in entry["files"]:
                _copy(source, target, digest)
            if entry["additions"]:
                rows = entry["existing"] + entry["additions"]
                _atomic_csv(entry["new_csv"], rows)
                if Counter(_identity(r) for r in _csv_rows(entry["new_csv"])) != Counter(
                    _identity(r) for r in rows
                ):
                    raise ValueError("Contrôle CSV après fusion incorrect : " + entry["evaluator"])
            for source, target, digest in entry["files"]:
                if _hash(source) != digest or _hash(target) != digest:
                    raise ValueError("Empreinte d'archive incohérente : " + entry["evaluator"])
            if entry["source_rows"]:
                new_rows = _csv_rows(entry["new_csv"])
                markers = {row["Origine"]: row for row in new_rows}
                for i, source_row in enumerate(_csv_rows(entry["old_csv"]), 2):
                    translated = _stamped(source_row, entry["source"], i)
                    if markers.get(translated["Origine"]) != translated:
                        raise ValueError("Essai manquant après migration : " + entry["evaluator"])

        result["progression"] = refresh_progression(root, year)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=outils.BASE_DIR)
    parser.add_argument("--apply", action="store_true",
                        help="Copier et fusionner, sans effacer les sources")
    parser.add_argument("--backup-confirmed", action="store_true",
                        help="Attester d'une sauvegarde externe du volume")
    parser.add_argument("--annee", default=None, help="Filtrer le suivi : 2026-2027")
    args = parser.parse_args()
    try:
        report = execute(args.root, args.apply, args.backup_confirmed, args.annee)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, "Migration interrompue : " + str(exc) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
