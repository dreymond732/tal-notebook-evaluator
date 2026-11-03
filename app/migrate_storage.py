"""Migration non destructive des évaluations vers un dossier unique par correcteur.

Par défaut : simulation, sans copie ni modification. --apply opère sous le
verrou partagé avec le serveur. Aucun ancien dossier n'est supprimé.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import tempfile
from pathlib import Path

import outils
from notebook_contract import load_catalog
from progression import progression_lock, refresh_progression
from storage_layout import GRADE_COLUMNS, storage_id


def _sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalise(row, fields, origin, number, version):
    kinds = [k for k in ("Note", "Score technique provisoire") if k in fields]
    if len(kinds) != 1:
        raise ValueError("Score historique ambigu : " + origin)
    kind = kinds[0]
    nature = row.get("Nature du score", "").strip()
    if not nature:
        nature = "technique_provisoire" if kind == "Score technique provisoire" else "note"
    if nature not in ("note", "technique_provisoire"):
        raise ValueError("Nature de score incompatible : " + origin)
    out = {
        "Date": row.get("Date", ""),
        "Nom": row.get("Nom", ""),
        "Prénom": row.get("Prénom", ""),
        "Classe": row.get("Classe", ""),
        "Score": row.get(kind, ""),
        "Bonus": row.get("Bonus", ""),
        "Nature du score": nature,
        "Maximum technique": row.get("Maximum technique", ""),
        "Relecture humaine": row.get("Relecture humaine", ""),
        "Numéro étudiant": row.get("Numéro étudiant", ""),
        "Version du contrat": str(version),
        "Origine": "migration:" + origin,
        "Ligne origine": str(number),
    }
    # Neutralise les valeurs qui pourraient être interprétées comme formules
    # lors d'une ouverture directe du CSV dans un tableur.
    for key in ("Nom", "Prénom", "Classe", "Numéro étudiant"):
        value = str(out[key])
        if value.lstrip().startswith(("=", "+", "-", "@")):
            out[key] = "'" + value
    return {key: out[key] for key in GRADE_COLUMNS}


def _read_legacy(path, origin, version):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        fields = reader.fieldnames or []
        required = {"Date", "Nom", "Prénom", "Classe"}
        if not required <= set(fields) or (("Note" in fields) == ("Score technique provisoire" in fields)):
            raise ValueError("Schéma CSV inconnu dans " + origin)
        if len(fields) != len(set(fields)):
            raise ValueError("Colonnes répétées dans " + origin)
        rows = []
        for number, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError("Nombre de champs incorrect dans " + origin + ":" + str(number))
            rows.append(_normalise(row, fields, origin, number, version))
    return rows


def _read_canonical(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        if reader.fieldnames != list(GRADE_COLUMNS):
            raise ValueError("Le CSV cible utilise un autre schéma : " + str(path))
        rows = list(reader)
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise ValueError("Le CSV cible contient une ligne incorrecte : " + str(path))
    return rows


def _atomic_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                         dir=path.parent, prefix=".migration-",
                                         delete=False) as stream:
            temp = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=GRADE_COLUMNS, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp, 0o600)
        os.replace(temp, path)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def _paths(root, evaluator, canonical):
    """Retrouve les répertoires de route, indépendamment de la casse, et -vN."""
    regex = re.compile(re.escape(evaluator) + r"(?:-v([0-9]+))?", re.IGNORECASE)
    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or entry.is_symlink() or entry.name == canonical:
            continue
        match = regex.fullmatch(entry.name)
        if match:
            # Un ancien stockage sans suffixe correspond à son contrat v1.
            yield entry, int(match.group(1)) if match.group(1) else 1


def _plan_files(source, target, reserved):
    if source.is_symlink():
        raise ValueError("Lien symbolique refusé : " + str(source))
    content_hash = _sha(source)
    if target in reserved and reserved[target] == content_hash:
        return None
    if target.exists() and _sha(target) == content_hash:
        reserved[target] = content_hash
        return None
    if target in reserved or target.exists():
        suffix = hashlib.sha256(source.as_posix().encode("utf-8")).hexdigest()[:16]
        target = target.with_name(target.stem + "__source_" + suffix + target.suffix)
        if target in reserved or target.exists():
            existing = reserved.get(target, _sha(target) if target.exists() else None)
            if existing == content_hash:
                return None
            raise ValueError("Collision d'archive : " + str(target))
    reserved[target] = content_hash
    return source, target


def prepare(root):
    """Construit le plan complet en lecture seule ; bloque les sources illisibles."""
    root = Path(root)
    if not root.is_dir():
        raise ValueError("Répertoire de soumissions introuvable : " + str(root))
    actions = []
    merged = {}
    sources = 0
    catalog = [entry for entry in load_catalog()
               if entry.get("active") and entry.get("evaluator")]
    destinations = {}
    for entry in catalog:
        evaluator = entry["evaluator"]
        name = storage_id(evaluator)
        if name in destinations:
            raise ValueError("Collision de nom physique entre évaluateurs")
        destinations[name] = evaluator
        target_dir = root / name
        journal = target_dir / ("notes_" + name + ".csv")
        current_rows = _read_canonical(journal)
        by_origin = {(row["Origine"], row["Ligne origine"]): row for row in current_rows}
        reserved = {}
        # Copie des versions suffixées et des anciens dossiers de classes.
        candidates = list(_paths(root, evaluator, name))
        # Un canonique déjà déployé ne doit pas avoir de sous-dossiers de classe.
        if target_dir.is_dir():
            candidates.append((target_dir, entry["version"]))
        for directory, version in candidates:
            group_dirs = sorted(p for p in directory.iterdir()
                                if p.is_dir() and p.name not in ("nb", "rapport"))
            for group in group_dirs:
                if group.is_symlink():
                    raise ValueError("Dossier de groupe symbolique interdit : " + str(group))
                sources += 1
                for file in sorted(group.iterdir()):
                    if file.is_symlink():
                        raise ValueError("Lien symbolique refusé : " + str(file))
                    if file.is_file() and file.suffix.lower() == ".csv" and file.name.lower().startswith("notes"):
                        origin = file.relative_to(root).as_posix()
                        for row in _read_legacy(file, origin, version):
                            key = (row["Origine"], row["Ligne origine"])
                            if key in by_origin:
                                if by_origin[key] != row:
                                    raise ValueError("Journal source modifié après migration : " + origin)
                            else:
                                by_origin[key] = row
                                current_rows.append(row)
                    elif file.is_dir() and file.name in ("nb", "rapport"):
                        for artifact in sorted(file.iterdir()):
                            if not artifact.is_file() or artifact.is_symlink():
                                raise ValueError("Archive inattendue : " + str(artifact))
                            planned = _plan_files(artifact, target_dir / file.name / artifact.name, reserved)
                            if planned:
                                actions.append(planned)
                    else:
                        raise ValueError("Fichier ou sous-dossier non reconnu : " + str(file))
        # Les anciennes données d'un modèle encore en place sont lues au même
        # titre que les autres : elles ne sont pas supprimées après la copie.
        merged[journal] = (current_rows, len(current_rows) - len(_read_canonical(journal)))

    # Contrôle des destinataires planifiés, avant toute écriture.
    if len({target for _, target in actions}) != len(actions):
        raise ValueError("Plusieurs archives correspondent au même chemin")
    return {"files": actions, "journals": merged, "groups": sources}


def execute(root, apply=False):
    """Prépare puis éventuellement copie ; réexécution sans doublons."""
    root = Path(root)
    with progression_lock(root):
        plan = prepare(root)
        changed = sum(1 for rows, additional in plan["journals"].values() if additional)
        result = {"dossiers_groupes": plan["groups"],
                  "fichiers_a_copier": len(plan["files"]),
                  "nouvelles_lignes": sum(count for _, count in plan["journals"].values()),
                  "journaux_a_mettre_a_jour": changed,
                  "mode": "APPLY" if apply else "DRY_RUN"}
        if not apply:
            return result
        # Conserver les originaux. En cas d'interruption, relancer la même
        # commande : empreintes de fichiers et provenance CSV sont vérifiées.
        for src, dst in plan["files"]:
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                with src.open("rb") as inp, dst.open("xb") as out:
                    shutil.copyfileobj(inp, out)
                    out.flush()
                    os.fsync(out.fileno())
                os.chmod(dst, 0o600)
            except FileExistsError:
                if _sha(src) != _sha(dst):
                    raise ValueError("Archive cible divergente : " + str(dst))
        for journal, (rows, additional) in plan["journals"].items():
            if additional or (not journal.exists() and rows):
                _atomic_csv(journal, rows)
        result["progression"] = refresh_progression(root)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=outils.BASE_DIR)
    parser.add_argument("--apply", action="store_true", help="Copier et fusionner, sans supprimer les originaux")
    args = parser.parse_args()
    print(execute(args.root, apply=args.apply))


if __name__ == "__main__":
    main()
