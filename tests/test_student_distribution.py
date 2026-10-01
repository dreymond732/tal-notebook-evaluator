"""Distribution integrity, source immutability and deployment URL handling."""
import copy
import json
import os
from pathlib import Path
import sys
import subprocess
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
            original = json.loads(raw)
            if original["cells"][-1].get("id") == prep.CELL_ID:
                self.assertEqual(original["cells"].pop(), prep.submission_cell())
            self.assertEqual(nb, original)

    def test_placeholder_is_replaced_once_without_changing_sources(self):
        path = self.root / self.entries[0]["notebook"]
        source = json.loads(path.read_text())
        if source["cells"][-1].get("id") != prep.CELL_ID:
            source["cells"].append(prep.submission_cell())
        path.write_text(json.dumps(source, ensure_ascii=False))
        original = path.read_bytes()
        output = self.root / "dist"
        for _ in range(2):
            prep.render(output, self.url, self.root)
            rendered = json.loads((output / self.entries[0]["notebook"]).read_text())
            self.assertEqual(sum(c.get("id") == prep.CELL_ID for c in rendered["cells"]), 1)
            self.assertEqual(rendered["cells"][:-1], source["cells"][:-1])
            self.assertEqual(len(rendered["cells"]), len(source["cells"]))
            self.assertNotIn(prep.URL_PLACEHOLDER, json.dumps(rendered))
            self.assertEqual(path.read_bytes(), original)
            self.assertNotIn(self.url.encode(), original)

    def test_s1_sources_require_the_final_placeholder_cell(self):
        path = self.root / self.entries[0]["notebook"]
        nb = json.loads(path.read_text())
        self.assertEqual(self.entries[0]["semester"], "S1")
        self.assertEqual(nb["cells"].pop(), prep.submission_cell())
        path.write_text(json.dumps(nb))
        with self.assertRaisesRegex(ValueError, "Cellule source de restitution absente"):
            prep.check_sources(self.root)

    def test_noncanonical_source_cells_and_stray_placeholders_are_rejected(self):
        original = json.loads((self.root / self.entries[0]["notebook"]).read_text())
        if original["cells"][-1].get("id") == prep.CELL_ID:
            original["cells"].pop()
        for mutation in ("duplicate", "position", "source", "output", "execution", "metadata", "stray"):
            with self.subTest(mutation=mutation):
                nb = copy.deepcopy(original)
                nb["cells"].append(prep.submission_cell())
                if mutation == "duplicate":
                    nb["cells"].append(prep.submission_cell())
                elif mutation == "position":
                    nb["cells"][-1], nb["cells"][-2] = nb["cells"][-2], nb["cells"][-1]
                elif mutation == "source":
                    nb["cells"][-1]["source"].append("print('modified')\n")
                elif mutation == "output":
                    nb["cells"][-1]["outputs"] = [{"output_type": "stream", "name": "stdout", "text": "old"}]
                elif mutation == "execution":
                    nb["cells"][-1]["execution_count"] = 1
                elif mutation == "metadata":
                    nb["cells"][-1]["metadata"]["tal"]["role"] = "provided"
                else:
                    nb["metadata"]["stray"] = prep.URL_PLACEHOLDER
                with self.assertRaises(ValueError):
                    prep.check_source(nb)

    def test_canonical_display_escapes_url_when_rendered(self):
        # Only the trusted generator's display template is executed; no notebook code.
        captured = []
        class DisplayModule:
            display = staticmethod(captured.append)
            HTML = staticmethod(lambda value: value)
        url = "https://example.test/a&copy;"
        cell = prep.submission_cell(url)
        with patch.dict(sys.modules, {"IPython.display": DisplayModule}):
            exec("".join(cell["source"]), {})
        self.assertEqual(len(captured), 1)
        self.assertIn('href="https://example.test/a&amp;copy;/submit"', captured[0])
        self.assertIn("Restitution de votre travail", captured[0])
        self.assertIn('rel="noopener noreferrer"', captured[0])

    def test_renamed_notebook_removes_obsolete_distribution_path(self):
        output = self.root / "dist"
        prep.render(output, self.url, self.root)
        entry = self.entries[0]
        previous = entry["notebook"]
        renamed = str(Path(previous).with_name("renamed_topic.ipynb"))
        (self.root / previous).rename(self.root / renamed)
        entry["notebook"] = renamed
        prep.render(output, self.url, self.root)
        self.assertFalse((output / previous).exists())
        self.assertTrue((output / renamed).exists())
        self.assertEqual(prep.verify_rendered(output, self.url, self.root), 2)

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


class DeployCommandTests(unittest.TestCase):
    def test_checks_and_generation_precede_docker_and_failure_stops_deployment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            env_file = root / "deployment.env"
            env_file.write_text("TAL_PUBLIC_URL=https://example.test/universite/tal\n")
            log = root / "commands.log"
            for name in ("python3", "docker"):
                command = root / name
                command.write_text('#!/bin/bash\nprintf "%s\\n" "' + name + ' $*" >> "$COMMAND_LOG"\n'
                                   'if [[ "${FAIL_RENDER:-}" == "yes" && "$*" == *" render "* ]]; then exit 17; fi\n')
                command.chmod(0o755)
            environment = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"], COMMAND_LOG=str(log))
            script = str(prep.ROOT / "deploy.sh")
            subprocess.run(["bash", script, str(env_file)], env=environment, check=True)
            calls = log.read_text()
            self.assertLess(calls.index(".py check"), calls.index(".py render"))
            self.assertLess(calls.index(".py render"), calls.index(".py verify"))
            self.assertLess(calls.index(".py verify"), calls.index("docker compose"))
            self.assertIn(f"--env-file {env_file}", calls)
            log.write_text("")
            environment["FAIL_RENDER"] = "yes"
            result = subprocess.run(["bash", script, str(env_file)], env=environment)
            self.assertEqual(result.returncode, 17)
            self.assertNotIn("docker", log.read_text())


if __name__ == "__main__":
    unittest.main()
