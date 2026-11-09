"""Gestion CLI du code enseignant (à usage unique ou personnel réutilisable).

Uniquement dans le conteneur/terminal du NAS. Aucun endpoint HTTP ne peut
déclencher cette opération. Le code et le destinataire ne sont pas imprimés.
"""
import sys

import teacher_access


def main():
    if "--revoke" in sys.argv[1:]:
        if len(sys.argv) != 2:
            print("Usage : python send_teacher_code.py --revoke", file=sys.stderr)
            return 2
        try:
            was_active = teacher_access.revoke_reusable_code()
        except (OSError, RuntimeError, ValueError) as exc:
            print("Révocation impossible : " + str(exc), file=sys.stderr)
            return 1
        print("Code personnel révoqué." if was_active else "Aucun code personnel actif.")
        return 0
    if len(sys.argv) > 1:
        print("Usage : python send_teacher_code.py [--revoke]", file=sys.stderr)
        return 2
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
    if teacher_access.reusable_mode():
        print("Code personnel réutilisable jusqu'à révocation ou remplacement.")
        print("Un nouvel envoi remplace immédiatement le code précédent.")
    else:
        print("Valable dix minutes, utilisable une fois.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
