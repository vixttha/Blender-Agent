import tempfile
import unittest
from pathlib import Path

from scripts.verify_release_approval import read_release_notes, validate_ci, validate_dispatch


class ReleaseApprovalTests(unittest.TestCase):
    def setUp(self):
        self.sha = "a" * 40
        self.event = {
            "repository": {"owner": {"id": 123, "login": "owner"}, "default_branch": "main"},
            "inputs": {"release_tag": "v0.0.3", "release_sha": self.sha, "ci_run_id": "456"},
        }
        self.env = {
            "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_TRIGGERING_ACTOR": "owner",
            "GITHUB_ACTOR_ID": "123", "GITHUB_REF": "refs/heads/main", "GITHUB_SHA": self.sha,
            "RELEASE_TAG": "v0.0.3", "RELEASE_SHA": self.sha, "RELEASE_CI_RUN_ID": "456",
        }
        self.run_info = {
            "id": 456, "workflow_id": 789, "head_sha": self.sha, "head_branch": "main",
            "event": "push", "status": "completed", "conclusion": "success",
        }
        self.run_jobs = {"total_count": 2, "jobs": [{"conclusion": "success"}, {"conclusion": "success"}]}

    def test_owner_approved_exact_target_and_ci(self):
        self.assertEqual(validate_dispatch(self.event, self.env, "0.0.3"), ("v0.0.3", self.sha, 456, "main"))
        self.validate_run(self.run_info, self.run_jobs)

    def test_unapproved_dispatches_are_rejected(self):
        for change, message in (
            ({"GITHUB_EVENT_NAME": "push"}, "manual workflow dispatch"),
            ({"GITHUB_ACTOR_ID": "1"}, "repository owner"),
            ({"GITHUB_TRIGGERING_ACTOR": "other"}, "repository owner"),
            ({"RELEASE_SHA": "b" * 40}, "differ from"),
            ({"GITHUB_SHA": "c" * 40}, "exact approved commit"),
            ({"GITHUB_REF": "refs/heads/topic"}, "default branch"),
        ):
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, message):
                validate_dispatch(self.event, self.env | change, "0.0.3")
        with self.assertRaisesRegex(ValueError, "package version"):
            validate_dispatch(self.event, self.env, "0.0.2.17")

    def test_requires_original_application_workflow_and_all_jobs(self):
        for change in ({"workflow_id": 0}, {"head_sha": "b" * 40}, {"event": "pull_request"}):
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "exact approved"):
                self.validate_run(self.run_info | change, self.run_jobs)
        for jobs in (
            {"total_count": 2, "jobs": [{"conclusion": "success"}]},
            {"total_count": 1, "jobs": [{"conclusion": "failure"}]},
        ):
            with self.subTest(jobs=jobs), self.assertRaisesRegex(ValueError, "Every application CI job"):
                self.validate_run(self.run_info, jobs)

    def test_reviewed_notes_load_only_for_the_requested_final_tag(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            content = "## Release notes\n\nA reviewed change.\n"
            (directory / "v0.0.3.md").write_bytes(content.encode("utf-8"))
            self.assertEqual(read_release_notes("v0.0.3", directory), content)
            with self.assertRaisesRegex(ValueError, "notes are missing"):
                read_release_notes("v0.0.4", directory)
            with self.assertRaisesRegex(ValueError, "final vMAJOR"):
                read_release_notes("v0.0.3.1", directory)

    def test_blank_or_invalid_notes_are_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            path = directory / "v0.0.3.md"
            for content, message in ((b"  \n", "notes are empty"), (b"\xff", "must be UTF-8")):
                with self.subTest(content=content), self.assertRaisesRegex(ValueError, message):
                    path.write_bytes(content)
                    read_release_notes("v0.0.3", directory)

    def validate_run(self, run, jobs):
        validate_ci(run, jobs, sha=self.sha, default_branch="main", expected_run=456, expected_workflow=789)


if __name__ == "__main__":
    unittest.main()
