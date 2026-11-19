"""Regression checks for instruction requirements and GitHub receipt attribution."""

import json
import unittest
from pathlib import Path

from validate_archive import provenance, validate_instructions


class InstructionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        version = json.loads(Path("graphify/versions.json").read_text())["graph"]["active_version"]
        cls.draft = Path(version, "CHATGPT_PROJECT_INSTRUCTIONS.md").read_text()

    def test_active_instructions(self):
        validate_instructions(self.draft)

    def test_missing_worker_limit(self):
        with self.assertRaisesRegex(ValueError, "one active worker"):
            validate_instructions(self.draft.replace("one active Worker", "a Worker"))

    def test_missing_graphify_route(self):
        with self.assertRaisesRegex(ValueError, "Missing instruction policy"):
            validate_instructions(self.draft.replace("/tree/graphify-hq", "/tree/unrelated"))

    def test_wrong_delivery_order(self):
        head = "Head — select one feature"
        worker = "Worker — implement"
        wrong = self.draft.replace(head, "[swap]").replace(worker, head).replace("[swap]", worker)
        with self.assertRaisesRegex(ValueError, "out of order"):
            validate_instructions(wrong)


class ProvenanceTests(unittest.TestCase):
    tested = "1" * 40
    base = "2" * 40
    head = "3" * 40

    def test_push_receipt(self):
        result = provenance(self.tested, "push", {"after": self.tested}, [])
        self.assertEqual(result["tested_sha"], self.tested)
        self.assertIsNone(result["pr_head_sha"])

    def test_pr_receipt(self):
        event = {"pull_request": {"base": {"sha": self.base}, "head": {"sha": self.head}}}
        result = provenance(self.tested, "pull_request", event, [self.base, self.head])
        self.assertEqual(result, {"tested_sha": self.tested, "checkout_kind": "pr_merge_commit",
                                  "pr_head_sha": self.head, "pr_base_sha": self.base})
        with self.assertRaisesRegex(ValueError, "does not match"):
            provenance(self.tested, "pull_request", event, [self.base, self.tested])

    def test_push_revision_mismatch(self):
        with self.assertRaisesRegex(ValueError, "Unexpected push"):
            provenance(self.tested, "push", {"after": self.head}, [])
