"""Regression coverage for README HQ versioning and navigation."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_readme_hq import validate


class ReadmeHQTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.archive = "readme-hq/versions/v0.0.1"
        self.write("README.md", "# HQ\n\n[Start](#hq)\n")
        self.write("readme-hq/README.md", "# Guide\n")
        self.write("readme-hq/versions/README.md", "| v0.0.1 | First |\n")
        self.write(f"{self.archive}/README.md", "# HQ\n\n[Start](#hq)\n")
        self.write(f"{self.archive}/GUIDE.md", "# Guide\n")
        self.write(f"{self.archive}/CHANGELOG.md", "# Changes\n")
        self.write("readme-hq/workspace/README.md", "# HQ workspace\n")
        self.write("versions/README.md", "# Public history\n")
        self.write("workspace/README.md", "| v0.0.1 | Draft |\n")
        self.write("workspace/v0.0.1/README.md", "# Workspace\n")
        self.write("workspace/v0.0.1/DRAFT.md", "# Draft\n")
        self.write("workspace/v0.0.1/CHANGELOG.md", "# Changes\n")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args], capture_output=True, text=True, check=True,
        ).stdout.strip()

    def commit(self):
        self.git("add", ".")
        self.git("-c", "user.email=ci@example.invalid", "-c", "user.name=README CI", "commit", "-qm", "Fixture")
        return self.git("rev-parse", "HEAD")

    def test_clean_baseline(self):
        self.assertEqual([], validate(self.root))

    def test_new_hq_version_and_public_archive(self):
        self.git("init", "-q")
        baseline = self.commit()
        self.write("readme-hq/versions/README.md", "| v0.0.10 | Latest |\n| v0.0.1 | First |\n")
        self.write("README.md", "# New HQ\n")
        self.write("readme-hq/versions/v0.0.10/README.md", "# New HQ\n")
        self.write("readme-hq/versions/v0.0.10/GUIDE.md", "# Guide\n")
        self.write("readme-hq/versions/v0.0.10/CHANGELOG.md", "# Changes\n")
        self.write("versions/README.md", "| v0.0.1 | Published |\n")
        self.write("versions/v0.0.1/README.md", "# Public README\n")
        self.write("versions/v0.0.1/CHANGELOG.md", "# Changes\n")
        self.commit()
        self.assertEqual([], validate(self.root, baseline))

    def test_frozen_changelog_cannot_be_rewritten(self):
        self.git("init", "-q")
        baseline = self.commit()
        self.write(f"{self.archive}/CHANGELOG.md", "# Rewritten\n")
        self.commit()
        self.assertTrue(any("existing archive changed" in error for error in validate(self.root, baseline)))

    def test_archive_drift_and_missing_workspace_file(self):
        self.write("README.md", "# Wrong\n")
        (self.root / "workspace/v0.0.1/DRAFT.md").unlink()
        errors = validate(self.root)
        self.assertTrue(any("latest HQ snapshot drift" in error for error in errors))
        self.assertTrue(any("missing required file" in error for error in errors))

    def test_duplicate_version_row(self):
        self.write("workspace/README.md", "| v0.0.1 | Draft |\n| v0.0.1 | Duplicate |\n")
        self.assertTrue(any("list each version folder once" in error for error in validate(self.root)))

    def test_broken_relative_absolute_and_anchor_links(self):
        self.write("workspace/v0.0.1/DRAFT.md", (
            "# Draft\n\n"
            "[Missing relative](missing.md)\n"
            "[Missing absolute](https://github.com/vixttha/Blender-Agent/blob/readme-hq/missing.md)\n"
            "[Missing heading](#not-present)\n"
            "![Missing image](missing.png)\n"
            "[Escaping link](../../../outside.md)\n"
            "[ref]: missing-reference.md\n"
        ))
        errors = validate(self.root)
        self.assertEqual(4, sum("missing" in error and "Markdown heading" not in error for error in errors))
        self.assertTrue(any("missing Markdown heading" in error for error in errors))
        self.assertTrue(any("link escapes repository" in error for error in errors))

    def test_pinned_source_file_and_heading(self):
        self.git("init", "-q")
        baseline = self.commit()
        origin = f"https://github.com/vixttha/Blender-Agent/blob/{baseline}"
        self.write("workspace/v0.0.1/DRAFT.md", f"# Draft\n\n[Source]({origin}/README.md#hq)\n")
        self.assertEqual([], validate(self.root))
        self.write("workspace/v0.0.1/DRAFT.md", f"# Draft\n\n[Source]({origin}/README.md#missing)\n")
        self.assertTrue(any("missing Markdown heading" in error for error in validate(self.root)))

    def test_public_draft_is_scanned_for_personal_data(self):
        self.write("workspace/v0.0.1/DRAFT.md", "# Draft\n\nContact: sample@example.invalid\n")
        self.assertTrue(any("possible personal path" in error for error in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
