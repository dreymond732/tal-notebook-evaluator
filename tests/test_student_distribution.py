"""Distribution integrity, source immutability and deployment URL handling."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
import prepare_student_notebooks as prep


class DistributionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.entries = [e for e in prep.load_catalog() if e["active"]][:2]
        for entry in self.entries:
            target = self.root / entry["notebook"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((prep.ROOT / entry["notebook"]).read_bytes())
        mock = patch.object(prep, "load_catalog", return_value=self.entries)
        mock.start()
        self.addCleanup(mock.stop)
        self.url = "https://example.test/universite/tal"

    def test_render_preserves_every_source_field_and_is_repeatable(self):
        originals = {p: p.read_bytes() for _, p in prep.active_sources(self.root)}
        output = self.root / "dist"
        for _ in range(2):
            self.assertEqual(prep.render(output, self.url, self.root), 2)
            self.assertEqual(prep.verify_rendered(output, self.url, self.root), 2)
        for path, raw in originals.items():
            self.assertEqual(path.read_bytes(), raw)
            nb = json.loads((output / path.relative_to(self.root)).read_text())
            self.assertEqual(nb["cells"].pop(), prep.submission_cell(self.url))
            self.assertEqual(nb, json.loads(raw))

    def test_saved_output_url_rejected_without_replacing_previous_distribution(self):
        output = self.root / "dist"
        prep.render(output, self.url, self.root)
        source = self.root / self.entries[0]["notebook"]
        old_render = (output / self.entries[0]["notebook"]).read_bytes()
        nb = json.loads(source.read_text())
        nb["metadata"]["leaked_output"] = {"text/html": f'<a href="{self.url}/submit">Déposer</a>'}
        source.write_text(json.dumps(nb))
        with self.assertRaises(ValueError):
            prep.render(output, self.url, self.root)
        self.assertEqual((output / self.entries[0]["notebook"]).read_bytes(), old_render)

    def test_verify_rejects_content_mutation_or_extra_teacher_copy(self):
        output = self.root / "dist"
        prep.render(output, self.url, self.root)
        extra = output / "corrige.ipynb"
        extra.write_text("{}")
        with self.assertRaises(ValueError):
            prep.verify_rendered(output, self.url, self.root)
        extra.unlink()
        target = output / self.entries[0]["notebook"]
        nb = json.loads(target.read_text())
        nb["cells"][1]["source"] = ["contenu modifié"]
        target.write_text(json.dumps(nb))
        with self.assertRaises(ValueError):
            prep.verify_rendered(output, self.url, self.root)

    def test_refuse_source_destinations_and_symlinks(self):
        for target in [self.root, self.root / "Notebooks TD"]:
            with self.assertRaises(ValueError):
                prep.render(target, self.url, self.root)
        link = self.root / "dist"
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            prep.render(link, self.url, self.root)

    def test_existing_foreign_directory_is_never_replaced(self):
        output = self.root / "dist"
        output.mkdir()
        foreign = output / "travail-important.txt"
        foreign.write_text("à conserver")
        with self.assertRaises(ValueError):
            prep.render(output, self.url, self.root)
        self.assertEqual(foreign.read_text(), "à conserver")
        foreign.unlink()
        output.rmdir()
        prep.render(output, self.url, self.root)
        foreign.write_text("à conserver aussi")
        with self.assertRaises(ValueError):
            prep.render(output, self.url, self.root)
        self.assertEqual(foreign.read_text(), "à conserver aussi")

    def test_url_validation_and_dotenv_not_executed(self):
        for value in ["", "file:///tmp/test", "https://u:p@example.test", "https://example.test/?x=1",
                      "https://example.test/#x", "https://example.test/submit", "https://example.test/\nfoo",
                      'https://example.test/$(touch file)', 'https://example.test/"']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                prep.public_url(value)
        env = self.root / ".env"
        env.write_text('OTHER_SECRET=$(exit 1)\nTAL_PUBLIC_URL="https://example.test/universite/tal/"\n')
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(prep.public_url(env_file=env), self.url)
        env.write_text("TAL_PUBLIC_URL=https://example.test\nTAL_PUBLIC_URL=https://other.test\n")
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(ValueError):
            prep.public_url(env_file=env)


if __name__ == "__main__":
    unittest.main()
