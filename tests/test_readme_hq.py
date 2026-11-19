"""Negative regression checks for the README HQ validator."""

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_readme_hq import REQUIRED, validate  # noqa: E402


class ReadmeHQTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for rel in REQUIRED:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)
        for area in ("versions", "workspace"):
            shutil.copytree(ROOT / area, self.root / area, dirs_exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_baseline(self):
        self.assertEqual([], validate(self.root))

    def test_archive_drift_rejected(self):
        (self.root / "readme-hq/versions/v0.0.1/README.md").write_text("# Wrong\n", encoding="utf-8")
        self.assertTrue(any("drift" in x for x in validate(self.root)))

    def test_missing_draft_rejected(self):
        (self.root / "workspace/v0.0.1/DRAFT.md").unlink()
        self.assertTrue(any("missing required" in x for x in validate(self.root)))

    def test_broken_branch_link_rejected(self):
        p = self.root / "graphify/README.md"
        p.write_text(p.read_text() + "\n[Missing](../no-such-file.md)\n")
        self.assertTrue(any("broken local link" in x for x in validate(self.root)))

    def test_broken_workspace_image_rejected(self):
        image = self.root / "workspace/v0.0.3/assets/triangle-inspection.webp"
        image.unlink()
        self.assertIn(
            "broken local link: workspace/v0.0.3/DRAFT.md -> assets/triangle-inspection.webp",
            validate(self.root),
        )

    def test_promoted_readme_keeps_image_links(self):
        workspace = self.root / "workspace/v0.0.3"
        promoted = self.root / "homepage"
        promoted.mkdir()
        shutil.copyfile(workspace / "DRAFT.md", promoted / "README.md")
        shutil.copytree(workspace / "assets", promoted / "assets")

        readme = (promoted / "README.md").read_text(encoding="utf-8")
        images = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", readme)
        self.assertCountEqual(images, [
            "assets/triangle-inspection.webp",
            "assets/wireframe-cube.webp",
        ])
        for path in images:
            data = (promoted / path).read_bytes()
            self.assertEqual(data[:4] + data[8:12], b"RIFFWEBP", path)

    def test_secret_rejected(self):
        p = self.root / "graphify/README.md"
        p.write_text(p.read_text() + "\napi_key=abcdefghijklmnop\n")
        self.assertTrue(any("credential-like" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
