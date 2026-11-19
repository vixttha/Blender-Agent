import unittest

from github_provenance import verify_pull_request
from traceability import resolve_features, validate_features
from version_maps import REPOSITORY


class PullRequestEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.source = "b" * 40
        self.head = "c" * 40
        self.candidate = {
            "version": "v1.0.0", "source_pr": 4,
            "source_commit": self.source, "source_branch": "feature/public",
        }
        self.pr = {
            "number": 4, "state": "open", "draft": False, "merged": False,
            "merge_commit_sha": "d" * 40, "base": {"repo": {"full_name": REPOSITORY}},
            "head": {"repo": {"full_name": REPOSITORY}, "ref": "feature/public", "sha": self.head},
        }
        self.commits = [{"sha": self.source}, {"sha": self.head}]
        self.reviews = []

    def fetch(self, route):
        return {
            "pulls/4": self.pr,
            "pulls/4/commits?per_page=100&page=1": self.commits,
            "pulls/4/reviews?per_page=100&page=1": self.reviews,
        }[route]

    def test_historical_pr_commit(self):
        result = verify_pull_request(self.candidate, self.fetch)
        self.assertEqual(result["source_relation"], "historical PR commit")
        self.assertEqual(result["pr_state"], "open")
        self.assertIsNone(result["merge_commit"])

    def test_commit_outside_pull_request_is_rejected(self):
        self.commits = [{"sha": self.head}]
        with self.assertRaisesRegex(ValueError, "absent"):
            verify_pull_request(self.candidate, self.fetch)

    def test_wrong_head_repository_is_rejected(self):
        self.pr["head"]["repo"]["full_name"] = "another/Blender-Agent"
        with self.assertRaisesRegex(ValueError, "GitHub source"):
            verify_pull_request(self.candidate, self.fetch)

    def test_reviews_are_scoped_to_commit_and_keep_latest_decision(self):
        def review(user_id, state, sha):
            return {"user": {"id": user_id}, "state": state, "commit_id": sha}

        self.reviews = [
            review(1, "APPROVED", self.source),
            review(1, "CHANGES_REQUESTED", self.head),
            review(2, "APPROVED", self.head),
            review(3, "APPROVED", self.source),
            review(3, "COMMENTED", self.head),
            review(4, "DISMISSED", self.source),
        ]
        result = verify_pull_request(self.candidate, self.fetch)
        self.assertEqual(result["exact_commit_approvals"], 1)

    def test_github_merge_commit_is_reported_separately(self):
        self.pr.update(state="closed", merged=True)
        self.candidate["source_commit"] = self.head
        result = verify_pull_request(self.candidate, self.fetch)
        self.assertEqual(result["source_relation"], "current head")
        self.assertEqual(result["pr_state"], "merged")
        self.assertEqual(result["merge_commit"], "d" * 40)


class TraceabilityTests(unittest.TestCase):
    def setUp(self):
        self.features = [{
            "id": "inspect-mesh", "label": "Inspect mesh", "document": "README.md",
            "change": "- Verify mesh structure.",
            "tests": [{"path": "tests/test_mesh.py", "line": "def test_mesh(self):"}],
        }]
        self.files = {
            "CHANGELOG.md": "# Changes\n\n- Verify mesh structure.\n",
            "tests/test_mesh.py": "class MeshTests:\n    def test_mesh(self):\n        pass\n",
        }

    def test_trace_citations_resolve_to_pinned_lines(self):
        validate_features(self.features, ["CHANGELOG.md", "README.md"])
        feature, = resolve_features(self.features, self.files.__getitem__)
        self.assertEqual(feature["change"]["line"], 3)
        self.assertEqual(feature["tests"][0]["line"], 2)

    def test_stale_or_ambiguous_test_declaration_fails(self):
        for source in ("", "    def test_mesh(self):\n    def test_mesh(self):\n"):
            with self.subTest(source=source):
                self.files["tests/test_mesh.py"] = source
                with self.assertRaisesRegex(ValueError, "one pinned source match"):
                    resolve_features(self.features, self.files.__getitem__)

    def test_path_outside_test_suite_is_rejected(self):
        self.features[0]["tests"][0]["path"] = "tests/../test_mesh.py"
        with self.assertRaisesRegex(ValueError, "tests/test_"):
            validate_features(self.features, ["CHANGELOG.md", "README.md"])
