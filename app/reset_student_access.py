"""Réinitialisation contrôlée d'une association email/numéro étudiant.

Commande locale réservée à l'enseignant, jamais exposée sur le Web.
"""
import argparse

import student_access


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--numero", required=True, help="Numéro étudiant exact")
    parser.add_argument("--confirmer", action="store_true",
                        help="Autoriser explicitement la révocation du code et de l'email")
    args = parser.parse_args()
    number = args.numero.strip()
    if not student_access.NUMBER_RE.fullmatch(number):
        parser.error("Numéro étudiant invalide")
    if not args.confirmer:
        parser.error("Mode prudent : ajouter --confirmer pour révoquer l'accès")
    conn = student_access._db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("DELETE FROM pending WHERE number=?", (number,))
        cursor = conn.execute("DELETE FROM accounts WHERE number=?", (number,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("Association réinitialisée" if cursor.rowcount else
          "Aucune association active pour ce numéro")


if __name__ == "__main__":
    main()
