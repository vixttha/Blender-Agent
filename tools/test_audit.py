"""CI tests for the portable, read-only stack audit."""
import contextlib
import io
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from audit import print_report, run


class AuditTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Code Stack fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.repo / "service.py").write_text("VERSION = 1\n")
        (self.repo / "view.ts").write_text("export const version = 1\n")
        (self.repo / "component.h").write_text("/* reviewed separately */\n")
        (self.repo / "package.json").write_text("{}\n")
        self.commit()
        self.config = {
            "schema_version": 1, "project": "Synthetic multi-language project",
            "source_commit": self.git("rev-parse", "HEAD"),
            "required_paths": ["service.py", "view.ts"],
            "sources": [{"id": "S1", "url": "https://example.com/source", "claim": "Fixture source"}],
            "technologies": [
                {"name": "Python", "status": "active", "role": "service", "evidence": ["S1"],
                 "tracked_language": True},
                {"name": "TypeScript", "status": "active", "role": "client", "evidence": ["S1"],
                 "tracked_language": True},
                {"name": "Rust", "status": "conditional", "role": "native helper",
                 "evidence": ["S1"]},
            ],
            "reviewed_paths": ["component.h"],
            "source_checks": {"service.py": ["VERSION = 1"]},
        }

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Synthetic fixture")

    def test_audits_distinct_languages_and_formats(self):
        report = run(self.repo, self.config)
        self.assertEqual(report["languages"], {"Python": ["service.py"], "TypeScript": ["view.ts"]})
        self.assertEqual(report["formats"], {"JSON": ["package.json"]})
        self.assertEqual(report["review_paths"], ["component.h"])
        with contextlib.redirect_stdout(io.StringIO()) as log:
            import sys
            print_report(report, sys.stdout)
        self.assertIn("Result: PASS", log.getvalue())

    def test_rejects_a_different_checkout(self):
        self.config["source_commit"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "HEAD differs"):
            run(self.repo, self.config)

    def test_rejects_a_moving_ref(self):
        self.config["source_commit"] = "HEAD"
        with self.assertRaisesRegex(ValueError, "full Git object ID"):
            run(self.repo, self.config)

    def test_rejects_an_unregistered_language(self):
        (self.repo / "new.go").write_text("package example\n")
        self.commit()
        self.config["source_commit"] = self.git("rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "unregistered source languages: Go"):
            run(self.repo, self.config)

    def test_rejects_review_path_until_classified_or_recorded(self):
        self.config["reviewed_paths"] = []
        with self.assertRaisesRegex(ValueError, "unreviewed tracked paths"):
            run(self.repo, self.config)

    def test_rejects_a_missing_required_path(self):
        self.config["required_paths"].append("missing.py")
        with self.assertRaisesRegex(ValueError, "missing required tracked paths"):
            run(self.repo, self.config)

    def test_rejects_unsubstantiated_technology(self):
        self.config["technologies"][0]["evidence"] = ["S404"]
        with self.assertRaisesRegex(ValueError, "incomplete role or evidence"):
            run(self.repo, self.config)

    def test_rejects_source_drift(self):
        self.config["source_checks"] = {"service.py": ["VERSION = 2"]}
        with self.assertRaisesRegex(ValueError, "source check failed"):
            run(self.repo, self.config)

    def test_uncommitted_files_do_not_enter_the_inventory(self):
        (self.repo / "untracked.rs").write_text("fn main() {}\n")
        self.assertNotIn("Rust", run(self.repo, self.config)["languages"])


if __name__ == "__main__":
    unittest.main()
