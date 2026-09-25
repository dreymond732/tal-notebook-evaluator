"""Integration checks against synthetic local repositories; never remote production."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "app" / "prepare_history_cleanup.py"
spec = importlib.util.spec_from_file_location("history_cleanup", MODULE_PATH)
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)


def command(*args, cwd=None, env=None):
    return subprocess.check_output(args, cwd=cwd, env=env, stderr=subprocess.PIPE).decode().strip()


@unittest.skipUnless(importlib.util.find_spec("git_filter_repo"), "optional git-filter-repo unavailable")
class HistoryCleanupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / "source"
        command("git", "init", "-b", "main", str(self.source))
        command("git", "config", "user.name", "Synthetic teacher", cwd=self.source)
        command("git", "config", "user.email", "teacher@example.invalid", cwd=self.source)
        self.environment = dict(os.environ, GIT_AUTHOR_DATE="2020-01-02T03:04:05+0200",
                                GIT_COMMITTER_DATE="2020-01-03T04:05:06+0200")
        resources = self.source / cleanup.RESOURCE_PATH
        resources.mkdir(parents=True)
        (resources / "corpus.txt").write_bytes(b"A corpus.\r\nExact bytes preserved.\r\n")
        (self.source / "old.md").write_text("https://subdomain.private.example/submit\n")
        self.commit("Resources and old link")
        self.resource = command("git", "rev-parse", "HEAD", cwd=self.source)
        command("git", "checkout", "-b", "side", cwd=self.source)
        (self.source / "side.txt").write_text("independent content\n")
        self.commit("side")
        command("git", "checkout", "main", cwd=self.source)
        (self.source / "notebook.ipynb").write_text(json.dumps({"cells": [{"cell_type": "markdown",
            "source": ["https://subdomain.private.example/submit", self.resource]}]}))
        self.commit("notebook")
        command("git", "merge", "--no-ff", "side", "-m", "merge preserving parents", cwd=self.source, env=self.environment)
        command("git", "tag", "release", cwd=self.source)
        self.output = self.root / "prepared"
        self.original = cleanup.local_refs(self.source)

    def commit(self, message):
        command("git", "add", ".", cwd=self.source)
        command("git", "commit", "-m", message, cwd=self.source, env=self.environment)

    def prepare(self):
        return cleanup.prepare(str(self.source), self.output, ["subdomain.private.example"], self.resource)

    def test_preserves_graph_metadata_resources_pin_and_source(self):
        report = self.prepare()
        self.assertEqual(cleanup.local_refs(self.source), self.original)
        self.assertEqual(report["commits"], 4)
        self.assertNotEqual(report["resource_commit"], self.resource)
        target = self.output / "rewritten.git"
        content = cleanup.git(target, "show", "refs/heads/main:notebook.ipynb")
        self.assertNotIn(b"subdomain.private.example", content)
        self.assertIn(report["resource_commit"].encode(), content)
        self.assertNotIn(self.resource.encode(), content)
        raw = cleanup.git(target, "cat-file", "commit", "refs/heads/main")
        self.assertEqual(sum(line.startswith(b"parent ") for line in raw.splitlines()), 2)
        self.assertIn(b"1578017106 +0200", raw)  # Original committer date/timezone.
        self.assertEqual(cleanup.git(target, "show", "refs/heads/main:" + cleanup.RESOURCE_PATH + "corpus.txt"),
                         b"A corpus.\r\nExact bytes preserved.\r\n")
        self.assertTrue((self.output / "original.bundle").is_file())
        self.assertTrue((self.output / "cleaned.bundle").is_file())

    def test_publish_is_explicit_atomic_and_keeps_all_refs(self):
        self.prepare()
        remote = self.root / "remote.git"
        command("git", "clone", "--bare", str(self.source), str(remote))
        self.assertEqual(cleanup.refs_at(remote), self.original)
        result = cleanup.publish(self.output, str(remote))
        manifest = json.loads((self.output / "manifest.json").read_text())
        self.assertEqual(result["published_refs"], 3)
        self.assertEqual(cleanup.refs_at(remote), manifest["new_refs"])

    def test_refuses_advanced_remote_without_changing_any_ref(self):
        self.prepare()
        (self.source / "new.txt").write_text("new work after preparation")
        self.commit("new work")
        before = cleanup.local_refs(self.source)
        with self.assertRaisesRegex(RuntimeError, "distants ont changé"):
            cleanup.publish(self.output, str(self.source))
        self.assertEqual(cleanup.local_refs(self.source), before)

    def test_refuses_bundle_tampering_and_output_in_repository(self):
        self.prepare()
        with (self.output / "cleaned.bundle").open("ab") as stream:
            stream.write(b"tampered")
        with self.assertRaisesRegex(RuntimeError, "bundle a changé"):
            cleanup.publish(self.output, str(self.source))
        with self.assertRaisesRegex(ValueError, "hors de tout dépôt"):
            cleanup.prepare(str(self.source), self.source / "private", ["subdomain.private.example"], self.resource)

    def test_discovery_ignores_other_urls_and_non_markdown(self):
        subject = self.source / "Notebooks contrôles finaux" / "DevoirS1.ipynb"
        subject.parent.mkdir()
        subject.write_text(json.dumps({"cells": [
            {"cell_type": "markdown", "source": ["Dépôt : https://subdomain.private.example/controleur/", " https://github.com/controleur/", " https://external.example/reference"]},
            {"cell_type": "code", "source": ["# Dépôt https://not-target.example/controleur/"]}]}))
        self.commit("instruction")
        cleanup.prepare(str(self.source), self.output, [], self.resource, discover=True)
        cleaned = cleanup.git(self.output / "rewritten.git", "show", "main:" + subject.relative_to(self.source).as_posix())
        self.assertNotIn(b"subdomain.private.example", cleaned)
        self.assertIn(b"https://github.com/controleur/", cleaned)
        self.assertIn(b"https://not-target.example/controleur/", cleaned)

    def test_annotated_tag_is_refused_without_changing_source(self):
        command("git", "tag", "-a", "annotated", "-m", "Requires separate audit", cwd=self.source,
                env=self.environment)
        before = cleanup.local_refs(self.source)
        with self.assertRaisesRegex(ValueError, "tags annotés"):
            self.prepare()
        self.assertEqual(cleanup.local_refs(self.source), before)
        self.assertFalse((self.output / "manifest.json").exists())

    def test_private_hosts_json_and_text(self):
        path = self.root / "private-hosts.json"
        path.write_text('["SUBDOMAIN.PRIVATE.EXAMPLE"]')
        self.assertEqual(cleanup.private_hosts(path), ["subdomain.private.example"])
        path.write_text("subdomain.private.example\nother.private.example\n")
        self.assertEqual(len(cleanup.private_hosts(path)), 2)


if __name__ == "__main__":
    unittest.main()
