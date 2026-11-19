import json
import os
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evidence_map import build, locate, publication_lock, publish_pair, read_published_pair, validate_manifest
from github_provenance import verify_pull_request

class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "repository": "sample/example",
            "source_commit": "a" * 40,
            "title": "Example evidence",
            "features": [{
                "id": "export",
                "label": "Evidence export",
                "documented_in": [{"path": "README.md", "anchor": "## Export"}],
                "changed_in": [{"path": "CHANGELOG.md", "anchor": "## v1.0.0"}],
                "tested_by": [{"path": "test_export.py", "anchor": "def test_export():"}],
            }],
        }

    def test_existing_manifest_needs_no_inventory_or_implementation_links(self):
        accepted = validate_manifest(self.manifest)
        self.assertEqual(len(accepted["features"][0]["tested_by"]), 1)

    def test_inventory_and_implementation_links_are_accepted(self):
        self.manifest["source_files"] = ["export.py", "README.md"]
        self.manifest["features"][0]["implemented_in"] = [
            {"path": "export.py", "anchor": "def export():"},
        ]
        self.assertEqual(validate_manifest(self.manifest), self.manifest)

    def test_inventory_rejects_invalid_paths_and_duplicates(self):
        for paths in (["README.md", "README.md"], ["tools/../README.md"], [None], "README.md"):
            with self.subTest(paths=paths):
                self.manifest["source_files"] = paths
                with self.assertRaisesRegex(ValueError, "unique source file paths"):
                    validate_manifest(self.manifest)

    def test_implementation_anchor_connects_feature_to_inventory_file(self):
        self.manifest["source_files"] = ["export.py"]
        self.manifest["features"][0]["implemented_in"] = [
            {"path": "export.py", "anchor": "def export():"},
        ]
        lines = {
            "export.py": ["def export():"],
            "README.md": ["## Export"],
            "CHANGELOG.md": ["## v1.0.0"],
            "test_export.py": ["def test_export():"],
        }
        with (
            tempfile.TemporaryDirectory() as folder,
            patch("evidence_map.git", return_value=b"commit"),
            patch("evidence_map.source_lines", side_effect=lambda commit, path: (lines[path], path)),
        ):
            graph, receipt = build(validate_manifest(self.manifest), Path(folder))
            links = json.loads(graph.read_text(encoding="utf-8"))["links"]
        anchor = "implemented_in:export.py:L1"
        edges = {(edge["source"], edge["target"], edge["relation"]) for edge in links}
        self.assertIn(("feature:export", anchor, "implemented_in"), edges)
        self.assertIn((anchor, "file:export.py", "located_in"), edges)
        self.assertEqual(receipt["source_files"], ["export.py"])

    def test_feature_links_are_optional(self):
        self.manifest["features"] = []
        self.assertEqual(validate_manifest(self.manifest)["features"], [])

    def test_source_path_must_stay_inside_commit(self):
        test = self.manifest["features"][0]["tested_by"][0]
        for path in ("../secrets.md", "/etc/passwd", "tools/../README.md", ".git/config", "HEAD:README.md"):
            with self.subTest(path=path):
                test["path"] = path
                with self.assertRaisesRegex(ValueError, "source link"):
                    validate_manifest(self.manifest)

    def test_anchor_resolves_to_one_exact_line(self):
        self.assertEqual(locate(["paragraph", "    evidence", "last"], "evidence", "case"), 2)
        for lines in (["no match"], ["evidence", "evidence"]):
            with self.subTest(lines=lines):
                with self.assertRaisesRegex(ValueError, "exactly one match"):
                    locate(lines, "evidence", "case")


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.repo = "sample/example"
        self.source = "a" * 40
        self.head = "b" * 40
        self.expected = {"number": 3, "source_branch": "topic"}
        self.identity = {"id": 101, "full_name": self.repo}
        self.pr = {
            "number": 3, "state": "open", "draft": False, "merged": False,
            "base": {"repo": dict(self.identity)},
            "head": {"repo": dict(self.identity), "ref": "topic", "sha": self.head},
            "merge_commit_sha": None,
        }
        self.commits = [{"sha": self.source}, {"sha": self.head}]
        self.reviews = []

    def fetch(self, route):
        return {
            "": self.identity,
            "pulls/3": self.pr,
            "pulls/3/commits?per_page=100&page=1": self.commits,
            "pulls/3/reviews?per_page=100&page=1": self.reviews,
        }[route]

    def verify(self):
        return verify_pull_request(self.repo, self.source, self.expected, self.fetch)

    def test_historical_commit_requires_github_membership(self):
        self.assertEqual(self.verify()["source_relation"], "historical PR commit")
        self.commits = [{"sha": self.head}]
        with self.assertRaisesRegex(ValueError, "absent"):
            self.verify()

    def test_unrelated_repository_or_branch_is_rejected(self):
        self.pr["head"]["ref"] = "unrelated"
        with self.assertRaisesRegex(ValueError, "source repository and branch"):
            self.verify()
        self.pr["head"]["ref"] = "topic"
        self.pr["head"]["repo"]["full_name"] = "another/example"
        with self.assertRaisesRegex(ValueError, "source repository and branch"):
            self.verify()

    def test_historical_slug_resolves_to_the_current_repository(self):
        self.repo = "sample/old-name"
        outcome = self.verify()
        self.assertEqual(outcome["pull_request"], "https://github.com/sample/example/pull/3")

    def test_same_slug_with_an_unrelated_repository_id_is_rejected(self):
        self.pr["head"]["repo"]["id"] = 102
        with self.assertRaisesRegex(ValueError, "source repository and branch"):
            self.verify()

    def test_missing_repository_identity_is_rejected(self):
        self.identity.pop("id")
        with self.assertRaisesRegex(ValueError, "stable repository identity"):
            self.verify()

    def test_superseded_and_later_commit_approvals_are_excluded(self):
        self.reviews = [
            {"user": {"id": 1}, "state": "APPROVED", "commit_id": self.source},
            {"user": {"id": 1}, "state": "CHANGES_REQUESTED", "commit_id": self.head},
            {"user": {"id": 2}, "state": "APPROVED", "commit_id": self.head},
            {"user": {"id": 3}, "state": "APPROVED", "commit_id": self.source},
        ]
        self.assertEqual(self.verify()["exact_commit_approvals"], 1)

    def test_merge_sha_is_distinct_from_source_sha(self):
        self.pr.update(state="closed", merged=True, merge_commit_sha="c" * 40)
        outcome = self.verify()
        self.assertEqual(outcome["source_commit"], self.source)
        self.assertEqual(outcome["merge_commit"], "c" * 40)
        self.assertEqual(outcome["pr_state"], "merged")


class PublicationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name) / "evidence"
        self.old = {"graph.json": b"old graph", "receipt.json": b"old receipt"}
        self.new = {"graph.json": b"new graph", "receipt.json": b"new receipt"}

    def assert_pair(self, expected):
        self.assertEqual({p.name: p.read_bytes() for p in self.output.iterdir()}, expected)

    def test_success_and_repeated_publication(self):
        publish_pair(self.output, self.old)
        self.assert_pair(self.old)
        publish_pair(self.output, self.new)
        publish_pair(self.output, self.new)
        self.assert_pair(self.new)

    def test_replace_failure_restores_previous_pair(self):
        publish_pair(self.output, self.old)
        replace = os.replace

        def fail_receipt(source, target):
            if target.name == "receipt.json":
                raise OSError("simulated receipt write failure")
            replace(source, target)

        with patch("evidence_map.os.replace", side_effect=fail_receipt):
            with self.assertRaisesRegex(OSError, "simulated receipt write failure"):
                publish_pair(self.output, self.new)
        self.assert_pair(self.old)
        publish_pair(self.output, self.new)
        self.assert_pair(self.new)

    def test_first_publish_failure_does_not_leave_half_pair(self):
        replace = os.replace

        def fail_receipt(source, target):
            if target.name == "receipt.json":
                raise OSError("simulated receipt write failure")
            replace(source, target)

        with patch("evidence_map.os.replace", side_effect=fail_receipt):
            with self.assertRaisesRegex(OSError, "simulated receipt write failure"):
                publish_pair(self.output, self.new)
        self.assert_pair({})

    def test_unavailable_receipt_target_does_not_replace_graph(self):
        self.output.mkdir()
        (self.output / "graph.json").write_bytes(self.old["graph.json"])
        (self.output / "receipt.json").mkdir()
        with self.assertRaisesRegex(ValueError, "ordinary evidence file"):
            publish_pair(self.output, self.new)
        self.assertEqual((self.output / "graph.json").read_bytes(), self.old["graph.json"])

    def test_contending_publisher_cannot_modify_previous_pair(self):
        publish_pair(self.output, self.old)
        with publication_lock(self.output), self.assertRaises(BlockingIOError):
            publish_pair(self.output, self.new)
        self.assert_pair(self.old)

    def interrupt_after_replacement(self, operation, name="graph.json"):
        worker = """
import os
import signal
import sys
from pathlib import Path
from evidence_map import publish_pair, read_published_pair

replace = os.replace

def interrupt(source, target):
    replace(source, target)
    if target.name == sys.argv[3]:
        os.kill(os.getpid(), signal.SIGKILL)

os.replace = interrupt
output = Path(sys.argv[1])
if sys.argv[2] == "publish":
    publish_pair(output, {"graph.json": b"new graph", "receipt.json": b"new receipt"})
else:
    read_published_pair(output)
"""
        completed = subprocess.run(
            [sys.executable, "-c", worker, str(self.output), operation, name],
            cwd=Path(__file__).resolve().parent, capture_output=True, timeout=15, check=False,
        )
        self.assertEqual(completed.returncode, -signal.SIGKILL, completed.stderr.decode())

    def test_read_recovers_pair_after_publisher_is_killed(self):
        publish_pair(self.output, self.old)
        self.interrupt_after_replacement("publish")
        self.assertEqual((self.output / "graph.json").read_bytes(), self.new["graph.json"])
        self.assertEqual((self.output / "receipt.json").read_bytes(), self.old["receipt.json"])
        self.assertEqual(read_published_pair(self.output), self.old)
        self.assert_pair(self.old)
        publish_pair(self.output, self.new)
        self.assert_pair(self.new)

    def test_retry_recovers_after_first_publisher_is_killed(self):
        self.interrupt_after_replacement("publish")
        self.assertFalse((self.output / "receipt.json").exists())
        with self.assertRaises(FileNotFoundError):
            read_published_pair(self.output)
        self.assert_pair({})
        publish_pair(self.output, self.new)
        self.assert_pair(self.new)

    def test_retry_republishes_after_interruption(self):
        publish_pair(self.output, self.old)
        self.interrupt_after_replacement("publish")
        publish_pair(self.output, self.new)
        self.assert_pair(self.new)

    def test_interruption_before_journal_retirement_restores_previous_pair(self):
        publish_pair(self.output, self.old)
        self.interrupt_after_replacement("publish", "receipt.json")
        self.assertEqual((self.output / "receipt.json").read_bytes(), self.new["receipt.json"])
        self.assertEqual(read_published_pair(self.output), self.old)
        self.assert_pair(self.old)

    def test_recovery_can_be_interrupted_and_repeated(self):
        publish_pair(self.output, self.old)
        self.interrupt_after_replacement("publish")
        self.interrupt_after_replacement("recover")
        self.assertEqual(read_published_pair(self.output), self.old)
        self.assert_pair(self.old)


if __name__ == "__main__":
    unittest.main()
