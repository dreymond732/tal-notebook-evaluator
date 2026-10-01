"""Régressions de résultat, type et provenance des TD S3 v2, sans exécution étudiante."""
import copy
import hashlib
import importlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
import s3_audit_linguistic as check
from s3_audit_data import TEXT0, TEXT1, TEXT2
import app_correction_TD3_S3 as td3


def validate(td, question, value, context=None):
    entry = importlib.import_module(f'app_correction_TD{td}_S3').CHECKS[question - 1]
    return entry['validate'](value, context or {}) if entry.get('contextual') else entry['validate'](value)


class FixedPipelineTests(unittest.TestCase):
    def setUp(self):
        self.ref = copy.deepcopy(check.SPACY_REFERENCE)

    def test_reference_texts_and_versions_are_fixed(self):
        provenance = self.ref['provenance']
        self.assertEqual((provenance['spacy'], provenance['model'], provenance['model_version']),
                         ('3.8.7', 'fr_core_news_sm', '3.8.0'))
        for number, text in enumerate((TEXT0, TEXT1, TEXT2)):
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), provenance['text_sha256'][str(number)])
        # Valeurs indépendamment observées : deux sauts de ligne ne sont pas des mots.
        self.assertEqual(self.ref['td1']['counts'], {'split': 47, 'tokens': 56, 'non_ponctuation': 41})
        self.assertEqual(self.ref['td2']['frequencies']['noms'], {'notice': 2, 'livre': 2, 'lecteur': 1})

    def test_td1_exact_annotations_and_not_linguistic_truth(self):
        value = {'annotations': self.ref['td1']['annotations']}
        self.assertTrue(validate(1, 1, value))
        row = next(r for r in value['annotations'] if r['forme'] == 'analysent')
        self.assertEqual(row['pos'], 'ADV')  # Le modèle est critiquable ; sa sortie ne se réécrit pas.
        row['pos'] = 'VERB'
        self.assertFalse(validate(1, 1, value))

    def test_td1_real_phrase_sizes_and_counts(self):
        value = {'phrases': self.ref['td1']['phrases']}
        self.assertTrue(validate(1, 2, value))
        value['phrases'][0]['tokens'] = 8
        self.assertFalse(validate(1, 2, value))
        counts = dict(self.ref['td1']['counts'], interpretation='Une explication personnelle.')
        self.assertTrue(validate(1, 5, counts))
        for value in (43, True, 41.0):
            self.assertFalse(validate(1, 5, dict(counts, non_ponctuation=value)))

    def test_td1_all_ordered_filters_not_any_coherent_subset(self):
        value = self.ref['td1']['filters']
        context = {1: {'annotations': self.ref['td1']['annotations']}}
        self.assertTrue(validate(1, 3, value, context))
        value['mots_pleins'].reverse()
        self.assertFalse(validate(1, 3, value, context))
        value['mots_pleins'] = ['étudiant']
        self.assertFalse(validate(1, 3, value, context))
        self.assertFalse(check.ordered_subsequence(['x', 'x'], ['x']))
        self.assertTrue(check.ordered_subsequence(['x', 'x'], ['x', 'y', 'x']))

    def test_td1_dependency_locations_are_distinct_in_first_sentence(self):
        value = {'verbe': 'analysent', 'verbe_debut': 15, 'dependant': 'étudiantes',
                 'dependant_debut': 4, 'relation': 'amod', 'interpretation': 'Divergence à analyser.'}
        self.assertTrue(validate(1, 4, value))
        self.assertTrue(validate(1, 4, dict(value, dependant='.', dependant_debut=44, relation='punct')))
        self.assertFalse(validate(1, 4, dict(value, dependant='analysent', dependant_debut=15)))
        self.assertFalse(validate(1, 4, dict(value, dependant='comparent', dependant_debut=52)))
        self.assertFalse(validate(1, 4, dict(value, relation=' ')))

    def test_closed_results_are_independent_of_missing_prior_answers(self):
        ref = self.ref['td2']
        before = ref['frequencies']['noms']
        after = {k: v for k, v in before.items() if k != 'notice'}
        self.assertTrue(validate(2, 3, {'exclusions': ['notice'], 'avant': before,
                                     'apres': after, 'justification': ''}))
        value = {key: ref['frequencies'][kind] for key, kind in
                 [('general_noms', 'noms'), ('specialise_noms', 'noms'),
                  ('general_verbes', 'verbes'), ('specialise_verbes', 'verbes')]}
        from collections import Counter
        value.update(combine=dict(Counter(before) + Counter(ref['frequencies']['verbes'])), comparaison='')
        self.assertTrue(validate(2, 7, value))
        self.assertTrue(validate(1, 3, self.ref['td1']['filters']))
        value['general_noms'] = {'livre': 1}
        self.assertFalse(validate(2, 7, value))

    def test_td2_first_ten_and_exact_summary(self):
        ref = self.ref['td2']
        value = {k: ref[k] for k in ('caracteres', 'phrases', 'tokens')}
        value['annotations'] = [{k: row[k] for k in ('forme', 'lemme', 'pos')} for row in ref['annotations'][:10]]
        self.assertTrue(validate(2, 1, value))
        value['annotations'] = ref['annotations'][1:11]
        self.assertFalse(validate(2, 1, value))
        value['annotations'] = ref['annotations'][:10]
        value['tokens'] = 19
        self.assertFalse(validate(2, 1, value))

    def test_td2_coherent_invented_frequencies_fail(self):
        value = self.ref['td2']['frequencies']
        self.assertTrue(validate(2, 2, value))
        self.assertFalse(validate(2, 2, {'noms': {'livre': 1}, 'verbes': {'lire': 1}}))
        value['verbes']['décrire'] = True
        self.assertFalse(validate(2, 2, value))

    def test_td2_pos_exact_with_free_tie_order(self):
        pos = self.ref['td2']['pos']
        value = {'pos': pos, 'top3': [['NOUN', 5], ['DET', 5], ['VERB', 2]], 'limite': ''}
        self.assertTrue(validate(2, 4, value))
        value['pos'] = {'NOUN': 5, 'DET': 5, 'VERB': 2}
        self.assertFalse(validate(2, 4, value))

    def test_td2_manual_selection_is_free_but_occurrences_not_invented(self):
        ref = self.ref['td2']
        rows = [dict(row, jugement='À discuter') for row in ref['annotations'][4:9]][::-1]
        value = {'lemmes': ref['lemmes'], 'controle': rows, 'limite_modele': 'Une limite.'}
        self.assertTrue(validate(2, 5, value))
        value['controle'] = [rows[0]] * 5
        self.assertFalse(validate(2, 5, value))
        value['controle'] = rows
        value['lemmes'] = ['notice']
        self.assertFalse(validate(2, 5, value))


    def test_td2_manual_selection_accepts_punctuation_with_real_multiplicity(self):
        ref = self.ref['td2']
        punctuation = next(row for row in ref['all_annotations'] if row['pos'] == 'PUNCT')
        def marked(rows):
            return [dict(row, jugement='Ponctuation ou mot vérifié.') for row in rows]
        value = {'lemmes': ref['lemmes'], 'controle': marked(ref['annotations'][:4] + [punctuation]),
                 'limite_modele': ''}
        self.assertTrue(validate(2, 5, value))
        value['controle'] = marked([punctuation] * 3 + ref['annotations'][:2])
        self.assertTrue(validate(2, 5, value))
        value['controle'] = marked([punctuation] * 4 + ref['annotations'][:1])
        self.assertFalse(validate(2, 5, value))


class ProvenanceAndTypeTests(unittest.TestCase):
    def test_offsets_cannot_be_boolean_or_overrun_slice(self):
        source = 'Mot'
        row = {'forme': 'Mot', 'lemme': 'mot', 'pos': 'NOUN', 'tag': '', 'debut': 0, 'fin': 3}
        self.assertTrue(check.q1_td1({'annotations': [row]}, source))
        for field, value in [('fin', 999), ('debut', False), ('fin', True), ('tag', None)]:
            self.assertFalse(check.q1_td1({'annotations': [dict(row, **{field: value})]}, source))

    def test_free_transfer_requires_prefix_including_punctuation(self):
        source = 'Un chat. Un chien dort.'
        spans = [('Un', 0, 2), ('chat', 3, 7), ('.', 7, 8), ('Un', 9, 11), ('chien', 12, 17)]
        rows = [{'forme': form, 'lemme': form.lower(), 'pos': 'PUNCT' if form == '.' else 'NOUN',
                 'debut': start, 'fin': end} for form, start, end in spans]
        value = {'texte': source, 'phrases': 2, 'annotations': rows, 'noms': [], 'verbes': [], 'question': ''}
        self.assertTrue(validate(1, 6, value))
        omitted = rows[:2] + rows[3:] + [{'forme': 'dort', 'lemme': 'dormir', 'pos': 'VERB', 'debut': 18, 'fin': 22}]
        self.assertFalse(validate(1, 6, dict(value, annotations=omitted)))

    def test_context_boolean_does_not_become_integer(self):
        context = {2: {'noms': {'notice': True, 'livre': 1}, 'verbes': {'lire': 1}}}
        exclusion = {'exclusions': ['notice'], 'avant': {'notice': 1, 'livre': 1}, 'apres': {'livre': 1}, 'justification': ''}
        self.assertFalse(check.exclusions(exclusion, context))
        value = {'general_noms': exclusion['avant'], 'specialise_noms': exclusion['avant'],
                 'general_verbes': {'lire': 1}, 'specialise_verbes': {'lire': 1},
                 'combine': {'notice': 1, 'livre': 1, 'lire': 1}, 'comparaison': ''}
        self.assertFalse(check.generalization(value, context))
        self.assertFalse(check.chart_data({'frequences': {'livre': 1}, 'hypothese': '', 'verification': ''},
                                         {3: {'apres': {'livre': True}}}))

    def test_td0_synthesis_presence_is_separate_from_technical_grade(self):
        value = {'split': ['L’analyse,', 'c’est', 'utile', '!'], 'limites': ' '}
        self.assertTrue(validate(0, 7, value))
        from app_correction_TD0_S3 import CHECKS
        self.assertEqual(CHECKS[6]['required_text_fields'], ['limites'])
        self.assertTrue(validate(0, 7, dict(value, limites='?')))

    def test_td3_search_rejects_slice_clamping(self):
        source = 'Les lecteurs lisent. Une lectrice lit.'
        start = source.index('lit')
        exact = [{'forme': 'lit', 'debut': start, 'fin': start + 3}]
        value = {'fragment': exact, 'forme': exact, 'lemme': exact, 'explication': ''}
        self.assertTrue(td3.research_modes(value))
        value['lemme'] = [{'forme': source[start:], 'debut': start, 'fin': 999}]
        self.assertFalse(td3.research_modes(value))

    def test_td3_evidence_counts_occurrences_not_windows(self):
        source, _ = td3.resources()
        matches = list(re.finditer(r'\bintelligence\b', source, re.I))[:3]
        rows = [{'debut': m.start(), 'fin': m.end(), 'passage': m.group()} for m in matches]
        value = {'affirmation': 'G1', 'preuves': rows, 'convention_proposee': '', 'limite': ''}
        self.assertTrue(td3.evidence(value))
        first = matches[0]
        value['preuves'] = [{'debut': first.start() - k, 'fin': first.end(),
                             'passage': source[first.start() - k:first.end()]} for k in (0, 1, 2)]
        self.assertFalse(td3.evidence(value))
        # Trois fenêtres répétées contenant trois vraies occurrences ne créent pas de faux compte.
        passage = source[matches[0].start():matches[-1].end()]
        value['preuves'] = [{'debut': matches[0].start(), 'fin': matches[-1].end(), 'passage': passage}] * 3
        self.assertTrue(td3.evidence(value))
        value['preuves'][0]['fin'] = len(source) + 1
        self.assertFalse(td3.evidence(value))


if __name__ == '__main__':
    unittest.main()
