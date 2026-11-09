"""Migration complémentaire TD3 : S1_TD3_one/bis/ter -> S1_TD3_A/B/C.

Simulation par défaut. Copie non destructive et idempotente après sauvegarde,
avec le même contrat d'intégrité que migrate_storage_s1.py. Aucune suppression.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import outils
from progression import progression_lock, refresh_progression
from migrate_storage_s1 import (
    _entry_plan, _summary, _copy, _csv_rows, _atomic_csv, _hash,
    _identity, _stamped,
)

TD3_PARTS = ("one", "bis", "ter")


def prepare(root):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Volume soumissions manquant ou non régulier")
    return [
        _entry_plan(root, f"td3-{part}-s1", source_name=f"S1_TD3_{part}")
        for part in TD3_PARTS
    ]


def execute(root=None, apply=False, backup_confirmed=False, year=None):
    root = Path(root if root is not None else outils.BASE_DIR)
    if not apply:
        summary = _summary(prepare(root))
        summary["mode"] = "SIMULATION"
        return summary
    if not backup_confirmed:
        raise ValueError("Sauvegarde indépendante exigée (--backup-confirmed)")
    with progression_lock(root):
        plans = prepare(root)
        summary = _summary(plans)
        summary["mode"] = "APPLICATION"
        for entry in plans:
            for source, target, digest in entry["files"]:
                _copy(source, target, digest)
            if entry["additions"]:
                merged = entry["existing"] + entry["additions"]
                _atomic_csv(entry["new_csv"], merged)
                if Counter(_identity(r) for r in _csv_rows(entry["new_csv"])) != Counter(
                    _identity(r) for r in merged
                ):
                    raise ValueError("Fusion TD3 incohérente : " + entry["evaluator"])
            for source, target, digest in entry["files"]:
                if _hash(source) != digest or _hash(target) != digest:
                    raise ValueError("Archive TD3 altérée : " + entry["evaluator"])
            if entry["source_rows"]:
                current = {row["Origine"]: row for row in _csv_rows(entry["new_csv"])}
                for index, original in enumerate(_csv_rows(entry["old_csv"]), 2):
                    copied = _stamped(original, entry["source"], index)
                    if current.get(copied["Origine"]) != copied:
                        raise ValueError("Essai TD3 manquant après copie")
        summary["progression"] = refresh_progression(root, year)
        return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=outils.BASE_DIR)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-confirmed", action="store_true")
    parser.add_argument("--annee", default=None)
    args = parser.parse_args()
    try:
        result = execute(args.root, args.apply, args.backup_confirmed, args.annee)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, "Migration TD3 interrompue : " + str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
