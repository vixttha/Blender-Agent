"""Code Stack v0.0.2 checks against synthetic Git repositories."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from audit import compact_receipt, run

KIT = Path(__file__).resolve().parents[1]
REPO_NAME = "example/portable-fixture"


class AuditTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.work = Path(directory.name)
        self.repo = self.work / "unrelated-product"
        self.repo.mkdir()
        self.git("init", "--quiet", "-b", "main")
        self.git("config", "user.name", "Code Stack fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        for path, body in {
            "src/app.py": "VALUE = 1\n",
            "web/view.ts": "export const value = 1\n",
            "vendor/lib.go": "package vendor\n",
            "generated/bindings.rs": "fn main() {}\n",
            "scripts/start": "#!/usr/bin/env -S python3 -u\nprint('fixture')\n",
            "web/Component.vue": "<script>export default {}</script>\n",
            "build.gradle": "plugins {}\n",
            "README.md": "# Portable fixture\n",
            "package.json": "{}\n",
        }.items():
            self.write(path, body)
        self.git("add", ".")
        self.git("update-index", "--chmod=+x", "scripts/start")
        self.git("commit", "--quiet", "-m", "Create unrelated fixture")
        self.pin = self.git("rev-parse", "HEAD")
        self.config = {
            "schema_version": 2,
            "project": "Portable fixture",
            "source_repository": REPO_NAME,
            "source_ref": "refs/heads/main",
            "source_commit": self.pin,
            "template_commit": "1" * 40,
            "required_paths": ["src/app.py", "web/view.ts"],
            "reviewed_paths": {
                "web/Component.vue": "Embedded script inspected in the fixture",
                "build.gradle": "Gradle script is build tooling",
            },
            "source_checks": {"src/app.py": ["VALUE = 1"]},
            "technologies": [
                self.technology("Python", "language"),
                self.technology("TypeScript", "language"),
                self.technology("JSON", "format"),
                self.technology("Vue component", "source"),
            ],
            "sources": [{
                "id": "S1", "kind": "repo-file", "review": "reviewed",
                "reviewed_on": "2026-01-01", "claim": "Fixture source",
                "commit": self.pin, "path": "src/app.py",
                "url": f"https://github.com/{REPO_NAME}/blob/{self.pin}/src/app.py",
            }],
        }

    def technology(self, name, basis):
        return {"name": name, "status": "active", "basis": basis,
                "role": "Fixture technology", "evidence": ["S1"]}

    def write(self, path, data):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(data, encoding="utf-8")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def commit(self, path, data):
        self.write(path, data)
        self.git("add", "--", path)
        self.git("commit", "--quiet", "-m", "Change fixture")
        return self.git("rev-parse", "HEAD")

    def test_inventory_reports_languages_formats_and_review_boundaries(self):
        report = run(self.repo, self.config)
        self.assertEqual(report["languages"],
                         {"Python": ["scripts/start", "src/app.py"], "TypeScript": ["web/view.ts"]})
        self.assertEqual(report["formats"], {"JSON": ["package.json"], "Markdown": ["README.md"]})
        self.assertEqual(report["review_paths"], ["build.gradle", "web/Component.vue"])
        self.assertEqual(report["vendored"], ["vendor/lib.go"])
        self.assertEqual(report["generated"], ["generated/bindings.rs"])
        self.assertFalse(report["evidence"]["claim_contents_checked"])
        self.assertEqual(report["evidence"]["reviewed_as_recorded"], 1)

    def test_discovers_and_audits_as_a_copied_kit(self):
        install = self.work / "copied-code-stack"
        shutil.copytree(KIT, install, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("README.md", "STACK.md", "STACK_MEMORY.md", "AUDIT.md",
                     "MIGRATION.md", "PROPOSAL.md", "LICENSE", "workflow.example.yml"):
            self.assertTrue((install / name).is_file(), name)
        registry = install / "code-stack.json"
        registry.write_text(json.dumps(self.config), encoding="utf-8")
        common = [sys.executable, str(install / "tools/audit.py"), "--repo", str(self.repo)]
        inventory = json.loads(subprocess.check_output(
            [*common, "--discover", self.pin], text=True, cwd=install))
        self.assertIn("web/Component.vue", inventory["review_paths"])
        summary = install / "summary.md"
        output = install / "audit.json"
        out = subprocess.check_output(
            [*common, "--config", str(registry), "--summary", str(summary),
             "--live-ref", "refs/heads/main", "--json", str(output)], text=True, cwd=install)
        receipt_line = next(line for line in out.splitlines()
                            if line.startswith("CODE_STACK_RECEIPT "))
        receipt = json.loads(receipt_line.split(" ", 1)[1])
        self.assertEqual(receipt["result"], "pass")
        self.assertEqual(receipt["source_commit"], self.pin)
        self.assertEqual(receipt["freshness"]["live"]["status"], "current")
        self.assertIn(receipt_line.split(" ", 1)[1], summary.read_text(encoding="utf-8"))
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["source_commit"], self.pin)
        fail = subprocess.run([*common, "--config", str(registry), "--live-ref", "main"],
                              capture_output=True, text=True)
        self.assertEqual(fail.returncode, 1)
        self.assertIn("fully qualified", fail.stderr)

    def test_freshness_docs_only_stack_changes_and_release(self):
        doc = self.commit("README.md", "# Updated docs\n")
        self.git("tag", "fixture-v1")
        tip = self.commit("src/app.py", "VALUE = 2\n")
        self.git("checkout", "--quiet", "--detach", self.pin)
        report = run(self.repo, self.config, "refs/heads/main", "refs/tags/fixture-v1")
        self.assertEqual(report["freshness"]["release"]["commit"], doc)
        self.assertEqual(report["freshness"]["release"]["status"], "docs-only")
        self.assertEqual(report["freshness"]["live"]["commit"], tip)
        self.assertEqual(report["freshness"]["live"]["status"], "stack-relevant")
        self.assertEqual(compact_receipt(report)["freshness"]["live"]["changed_count"], 2)

    def test_missing_comparison_is_unknown(self):
        report = run(self.repo, self.config, "refs/remotes/origin/missing")
        self.assertEqual(report["freshness"]["live"]["status"], "unknown")

    def test_divergent_comparison_is_unknown(self):
        self.git("checkout", "--quiet", "--orphan", "unrelated")
        self.commit("README.md", "# Independent root\n")
        self.git("checkout", "--quiet", "--detach", self.pin)
        self.assertEqual(run(self.repo, self.config, "refs/heads/unrelated")
                         ["freshness"]["live"]["status"], "unknown")

    def test_malformed_values_have_field_diagnostics(self):
        self.config["project"] = None
        with self.assertRaisesRegex(ValueError, "project must"):
            run(self.repo, self.config)

    def test_stale_and_missing_evidence_ids_are_rejected(self):
        self.config["technologies"][0]["evidence"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "known evidence IDs"):
            run(self.repo, self.config)

    def test_repo_evidence_links_must_match_bound_location(self):
        self.config["sources"][0]["url"] = f"https://github.com/{REPO_NAME}/blob/main/src/app.py"
        with self.assertRaisesRegex(ValueError, "declared GitHub repository"):
            run(self.repo, self.config)

    def test_repo_evidence_path_must_exist(self):
        row = self.config["sources"][0]
        row["path"] = "src/absent.py"
        row["url"] = f"https://github.com/{REPO_NAME}/blob/{self.pin}/src/absent.py"
        with self.assertRaisesRegex(ValueError, "regular tracked file"):
            run(self.repo, self.config)

    def test_repo_evidence_sha_must_match_pin(self):
        self.config["sources"][0]["commit"] = "2" * 40
        with self.assertRaisesRegex(ValueError, "match the audited source commit"):
            run(self.repo, self.config)

    def test_requires_detected_languages_and_declared_formats(self):
        self.config["technologies"][0]["status"] = "retired"
        with self.assertRaisesRegex(ValueError, "unregistered source languages: Python"):
            run(self.repo, self.config)
        self.config["technologies"][0]["status"] = "active"
        self.config["technologies"][2]["name"] = "TOML"
        with self.assertRaisesRegex(ValueError, "declared formats without files: TOML"):
            run(self.repo, self.config)

    def test_explicit_overrides_and_stale_review(self):
        self.config["overrides"] = {"build.gradle": {
            "kind": "language", "name": "Groovy", "reason": "Reviewed build script",
        }}
        self.config["technologies"].append(self.technology("Groovy", "language"))
        with self.assertRaisesRegex(ValueError, "stale reviewed paths"):
            run(self.repo, self.config)
        del self.config["reviewed_paths"]["build.gradle"]
        self.assertEqual(run(self.repo, self.config)["languages"]["Groovy"], ["build.gradle"])

    def test_dirty_work_is_excluded(self):
        self.write("untracked.rb", "puts 'fixture'\n")
        self.assertNotIn("Ruby", run(self.repo, self.config)["languages"])

    def test_wrong_checkout_and_source_fragments_are_rejected(self):
        self.config["source_checks"] = {"src/app.py": ["VALUE = 99"]}
        with self.assertRaisesRegex(ValueError, "source check failed"):
            run(self.repo, self.config)
        self.commit("README.md", "# Changed\n")
        with self.assertRaisesRegex(ValueError, "HEAD differs"):
            run(self.repo, self.config)


if __name__ == "__main__":
    unittest.main()
