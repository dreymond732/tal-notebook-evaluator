"""Envoi administratif d'un code à usage unique pour l'espace enseignant TAL.

Uniquement dans le conteneur/terminal du NAS. Aucun endpoint HTTP ne peut
déclencher cette opération. Le code et le destinataire ne sont pas imprimés.
"""
import sys

import teacher_access


def main():
    try:
        if not teacher_access.configured():
            raise ValueError(
                "Adresse TAL_TEACHER_EMAIL, SMTP, année ou clé Flask non configurés"
            )
        if not teacher_access.issue_cli_code():
            raise ValueError("Limite d'envoi CLI atteinte ; opération refusée")
    except (OSError, RuntimeError, ValueError) as exc:
        print("Envoi impossible : " + str(exc), file=sys.stderr)
        return 1
    print("Code enseignant envoyé à l'adresse autorisée dans TAL_TEACHER_EMAIL.")
    print("Valable dix minutes, utilisable une fois.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
