"""Acceptance tests for generated language decisions and repeatable Git evidence."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]


class PortableStackTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.repo = self.root / "target"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Code Stack Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.kit = self.root / "copied-kit"
        shutil.copytree(KIT, self.kit)
        self.out = self.root / "review"

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def commit(self, name, files):
        for filename, body in files.items():
            path = self.repo / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", name)
        return self.git("rev-parse", "HEAD")

    def scan(self, *args, succeeds=True):
        result = subprocess.run(
            [sys.executable, str(self.kit / "tools/stack.py"), "--repo", str(self.repo),
             "--out", str(self.out), *map(str, args)],
            cwd=self.root, check=False, capture_output=True, text=True,
        )
        if not succeeds:
            self.assertNotEqual(result.returncode, 0)
            return result.stderr
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("CODE_STACK_REVIEW_RECEIPT", result.stdout)
        receipt = json.loads((self.out / "receipt.json").read_text(encoding="utf-8"))
        for filename, expected in receipt["outputs_sha256"].items():
            self.assertEqual(hashlib.sha256((self.out / filename).read_bytes()).hexdigest(), expected)
        self.assertFalse(receipt["runtime_validated"])
        return json.loads((self.out / "code-stack.json").read_text(encoding="utf-8"))

    def input(self, name, data):
        path = self.root / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_pinned_blender_role_and_no_target_execution(self):
        first = self.commit("Python package", {
            "pyproject.toml": '[project]\nrequires-python = ">=3.11"\n[project.scripts]\nexample = "host:main"\nexample-mcp = "host:mcp"\n',
            "src/worker.py": 'import bpy\nraise RuntimeError("target code must never run")\n',
            ".github/workflows/ci.yml": "jobs: {}\n",
        })
        self.commit("later unrelated runtime", {"app/thing.go": "package thing\n"})
        self.git("remote", "add", "origin", "https://example-token@github.com/example/project.git")
        registry = self.scan("--ref", first)
        self.assertEqual(registry["source_commit"], first)
        self.assertEqual(registry["source_repository"], "example/project")
        self.assertEqual(set(registry["inventory"]["languages"]), {"Python"})
        choices = {(row["role"], row["language"]): row for row in registry["recommendations"]}
        self.assertEqual(choices["blender-worker", "Python"]["verdict"], "keep")
        self.assertEqual(choices["blender-worker", "C++"]["verdict"], "drop")
        self.assertIn("src/worker.py", choices["blender-worker", "Python"]["evidence_paths"])
        self.assertEqual(choices["service", "Python"]["verdict"], "keep")
        self.assertIn(first, registry["evidence"]["src/worker.py"]["url"])
        self.assertNotIn("example-token", (self.out / "code-stack.json").read_text())

    def test_monorepo_languages_and_forward_plan(self):
        self.commit("Mixed project", {
            "client/package.json": '{"engines":{"node":">=22"},"devDependencies":{"vite":"1"}}',
            "client/src/main.ts": "export const name = 'client'\n",
            "client/vendor/legacy.py": "ignored\n",
            "backend/go.mod": "module example.org/backend\n\ngo 1.24\n",
            "backend/server.go": "package server\n",
            "unusual/sim.jl": "const x = 1\n",
            "app.vue": "<template/>\n",
        })
        context = self.input("goals.json", {"goals": [
            {"component": "future", "role": "browser", "need": "Preview a generated asset"},
            {"component": "backend", "role": "native", "need": "Find the bottleneck first"},
        ]})
        registry = self.scan("--context", context)
        choices = {(row["component"], row["role"], row["language"]): row["verdict"]
                   for row in registry["recommendations"]}
        self.assertEqual(choices["client", "browser", "TypeScript"], "keep")
        self.assertEqual(choices["backend", "go", "Go"], "keep")
        self.assertEqual(choices["backend", "native", "Rust"], "defer")
        self.assertEqual(choices["future", "browser", "TypeScript"], "adopt")
        self.assertEqual(choices[".", "unknown", "Julia"], "keep")
        self.assertIn("app.vue", registry["inventory"]["review_paths"])
        self.assertIn("client/vendor/legacy.py", registry["inventory"]["vendored"])
        self.assertNotIn("blender-worker", {row["role"] for row in registry["recommendations"]})

    def test_refresh_preserves_approvals_and_flags_evidence_changes(self):
        first = self.commit("initial Node package", {
            "package.json": '{"bin":"./src/main.js"}', "src/main.js": "console.log('first')\n",
        })
        approval = self.input("approval.json", [
            {"component": ".", "role": "cli", "language": "JavaScript", "action": "keep", "reason": "Maintain installed CLI"},
        ])
        registry = self.scan("--approve", approval)
        self.assertEqual(registry["approved_decisions"][0]["status"], "current")
        snapshot = self.out / "code-stack.json"
        self.commit("documentation only", {"README.md": "# Help\n"})
        registry = self.scan("--previous", snapshot)
        self.assertEqual(registry["refresh"]["changed_paths"], ["README.md"])
        self.assertEqual(registry["approved_decisions"][0]["status"], "current")
        self.commit("changed entrypoint", {"package.json": '{"bin":{"app":"./src/main.js"}}'})
        registry = self.scan("--previous", snapshot)
        self.assertEqual(registry["approved_decisions"][0]["approved_at_source"], first)
        self.assertEqual(registry["approved_decisions"][0]["status"], "review-needed")
        self.assertTrue(registry["refresh"]["recommendations_for_review"])
        self.git("rm", "-q", "package.json", "src/main.js")
        self.git("commit", "-qm", "retire the component")
        registry = self.scan("--previous", snapshot)
        self.assertEqual(registry["approved_decisions"][0]["status"], "component-or-candidate-missing")

    def test_bad_inputs_leave_no_report_and_unrecognized_content_is_explicit(self):
        self.commit("invalid manifest", {"package.json": '{', "README.md": "# Help\n"})
        stderr = self.scan("--ref", "--missing", succeeds=False)
        self.assertIn("expected one argument", stderr)
        self.assertFalse(self.out.exists())
        stderr = self.scan("--previous", self.input("old.json", {"schema_version": 2}), succeeds=False)
        self.assertIn("schema 3", stderr)
        registry = self.scan()
        self.assertEqual(registry["components"][0]["manifests"][0]["detail"],
                         "Manifest content unavailable or unrecognized")


if __name__ == "__main__":
    unittest.main()
