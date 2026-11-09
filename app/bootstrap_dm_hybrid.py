"""Indexation optionnelle des anciens DM S1 dans la nouvelle file hybride.

Simulation sans écriture par défaut, application après sauvegarde. Les CSV,
rapports, scores originaux et copies archivées restent strictement intacts.
Les calculs sont inertes (AST/JSON), sans exécution de code étudiant.
"""
import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

import outils
import dm_hybrid
from app_correction_DM_intermediaire_S1 import check_notebook, MAX_SCORE_TOTAL
from progression import _academic_start, _date, progression_lock
from storage_layout import storage_id


def candidates(root):
    name = storage_id("dm-intermediaire-s1")
    journal = Path(root) / name / ("notes_" + name + ".csv")
    if not journal.is_file() or journal.is_symlink():
        return []
    year = _academic_start(dm_hybrid._year())
    latest = {}
    with journal.open(encoding="utf-8-sig", newline="") as stream:
        for index, row in enumerate(csv.DictReader(stream, delimiter=";")):
            number = (row.get("Numéro étudiant") or "").strip()
            origin = (row.get("Origine") or "").strip()
            date = _date(row.get("Date", ""))
            if (not dm_hybrid.NUMBER_RE.fullmatch(number)
                    or not dm_hybrid.RECEIPT_RE.fullmatch(origin.removeprefix("direct:"))
                    or not origin.startswith("direct:")
                    or date is None
                    or not datetime(year,9,1) <= date < datetime(year+1,9,1)):
                continue
            if number not in latest or (date,index) > latest[number][0]:
                latest[number] = ((date,index), number, origin.removeprefix("direct:"))
    return [row[1:] for row in latest.values()]


def inspect(root):
    result = []
    for number,receipt in candidates(root):
        try:
            file = dm_hybrid._notebook_path(receipt)
            blob = file.read_bytes()
            score,details,maximum,info,error = check_notebook(blob.decode("utf-8-sig"),file.name)
            if error or maximum != MAX_SCORE_TOTAL or info.get("numero_etudiant") != number:
                raise ValueError("Copie ou contrat inexploitables")
            result.append((number,receipt,blob,score))
        except (OSError,ValueError,UnicodeError):
            result.append((number,receipt,None,None))
    return result


def run(apply=False, backup_confirmed=False):
    if apply and not backup_confirmed:
        raise ValueError("Sauvegarde indépendante obligatoire (--backup-confirmed)")
    root = Path(outils.BASE_DIR)
    with progression_lock(root) if apply else _null_context():
        examined = inspect(root)
        stats = {
            "candidats":len(examined),
            "copies_exploitables":sum(blob is not None for _,_,blob,_ in examined),
            "copies_inexploitables":sum(blob is None for _,_,blob,_ in examined),
            "ajoutes":0,
            "deja_indexees":0,
            "mode":"APPLICATION" if apply else "SIMULATION",
        }
        if not apply:
            return stats
        conn = dm_hybrid._db()
        try:
            conn.execute("BEGIN IMMEDIATE")
            for number,receipt,blob,score in examined:
                if blob is None:
                    continue
                if dm_hybrid._latest(conn,number):
                    stats["deja_indexees"] += 1
                    continue
                if conn.execute("SELECT 1 FROM submissions WHERE submission_id=?",
                                (receipt,)).fetchone():
                    stats["deja_indexees"] += 1
                    continue
                conn.execute(
                    """INSERT INTO submissions
                    (submission_id,student_number,academic_year,received_at,
                     auto_score,auto_version,notebook_sha256,state)
                    VALUES(?,?,?,datetime('now'),?,?,?,'pending')""",
                    (receipt,number,dm_hybrid._year(),score,
                     dm_hybrid.GRADING_VERSION,hashlib.sha256(blob).hexdigest())
                )
                stats["ajoutes"] += 1
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        return stats


class _null_context:
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-confirmed", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(run(args.apply,args.backup_confirmed),
                         ensure_ascii=False,sort_keys=True))
    except (OSError,ValueError) as exc:
        parser.exit(1, "Reprise DM interrompue : " + str(exc) + "\n")


if __name__ == "__main__":
    main()
