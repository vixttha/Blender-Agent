import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from verify_archive import execution_mode, export_candidate, source_repository


class ExecutionModeTests(unittest.TestCase):
    def github_mode(self, repository):
        with tempfile.TemporaryDirectory() as directory:
            event_path = Path(directory) / "event.json"
            event_path.write_text(json.dumps({"repository": repository}), encoding="utf-8")
            return execution_mode({"GITHUB_ACTIONS": "true", "GITHUB_EVENT_PATH": str(event_path)})

    def test_local_checkout_ignores_generic_ci_and_repository_variables(self):
        self.assertEqual(execution_mode({"CI": "true", "GITHUB_REPOSITORY": "example/name"}), "local")

    def test_public_visibility(self):
        self.assertEqual(self.github_mode({"private": False, "visibility": "public"}), "github-public")
        self.assertEqual(self.github_mode({"private": False}), "github-public")

    def test_private_and_internal_visibility(self):
        for repository in ({"private": True}, {"visibility": "private"}, {"visibility": "internal"}):
            with self.subTest(repository=repository):
                self.assertEqual(self.github_mode(repository), "github-private")

    def test_unknown_visibility_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "event payload"):
            execution_mode({"GITHUB_ACTIONS": "true"})
        with self.assertRaisesRegex(ValueError, "identify repository visibility"):
            self.github_mode({})

    def test_historical_repository_identity_survives_rename(self):
        entry = {"source_commit": "a" * 40, "source_repository": "example/old"}
        self.assertEqual(source_repository(entry, "example/new"), "example/old")
        self.assertEqual(source_repository(entry, None), "example/old")
        self.assertEqual(source_repository({"source_commit": None}, "example/new"), "example/new")

    def test_nonpublic_modes_do_not_export_evidence_payloads(self):
        for mode in ("github-private", "local"):
            with self.subTest(mode=mode), redirect_stdout(StringIO()) as stream:
                export_candidate("v0.0.9", "a" * 40, Path(os.devnull), mode)
                self.assertNotIn("GRAPHIFY_HQ_EXPORT", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
