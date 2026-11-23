from tal_toolkit.audit_llm import concordances_expression


def test_retrouver_forme_sans_sous_chaines_et_conserver_les_bornes():
    source = "Adroite, elle a le DROIT. Quels droits ? Droit !"
    lignes = concordances_expression(source, "droit", largeur=3)
    assert [ligne["expression"] for ligne in lignes] == ["DROIT", "Droit"]
    for ligne in lignes:
        assert source[ligne["debut"]:ligne["fin"]] == ligne["expression"]
    assert lignes[1]["droite"] == " !"


def test_locution_et_ponctuation_litterale():
    source = "Il\nfaudrait voir M. Turgeon. Mx Turgeon et Turgeonnet."
    assert concordances_expression(source, "il faudrait")[0]["expression"] == "Il\nfaudrait"
    assert concordances_expression(source, "il faut") == []
    assert len(concordances_expression(source, "M. Turgeon")) == 1
