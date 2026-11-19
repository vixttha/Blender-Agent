"""Negative regression checks for the README HQ validator."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_readme_hq import validate  # noqa: E402


class ReadmeHQTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        paths = (
            "README.md", "readme-hq/README.md", "readme-hq/versions/README.md",
            "readme-hq/versions/v0.0.1/README.md",
            "readme-hq/versions/v0.0.1/GUIDE.md",
            "readme-hq/versions/v0.0.1/CHANGELOG.md",
            "readme-hq/workspace/README.md",
            "readme-hq/workspace/v0.0.1/README.md",
            "versions/README.md", "workspace/README.md",
            "workspace/v0.0.1/README.md",
            "workspace/v0.0.1/DRAFT.md",
            "workspace/v0.0.1/CHANGELOG.md",
            "workspace/v0.0.1/REVIEW.md",
            "graphify/README.md", ".github/workflows/readme-hq.yml",
        )
        for rel in paths:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_baseline(self):
        self.assertEqual([], validate(self.root))

    def test_archive_drift_rejected(self):
        (self.root / "README.md").write_text("# Wrong\n", encoding="utf-8")
        self.assertTrue(any("drift" in x for x in validate(self.root)))

    def test_missing_draft_rejected(self):
        (self.root / "workspace/v0.0.1/DRAFT.md").unlink()
        self.assertTrue(any("missing required" in x for x in validate(self.root)))

    def test_broken_branch_link_rejected(self):
        p = self.root / "graphify/README.md"
        p.write_text(p.read_text() + "\n[Missing](../no-such-file.md)\n")
        self.assertTrue(any("broken local link" in x for x in validate(self.root)))

    def test_secret_rejected(self):
        p = self.root / "graphify/README.md"
        p.write_text(p.read_text() + "\napi_key=abcdefghijklmnop\n")
        self.assertTrue(any("credential-like" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
