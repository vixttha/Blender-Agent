import os
import tempfile
import unittest
from pathlib import Path

from blender_agent.paths import destination_path, root_path, source_path


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = root_path(self.temp.name)
        (self.root / "asset.stl").write_bytes(b"not a real model")

    def test_existing_source_inside_workspace(self):
        self.assertEqual(source_path("asset.stl", self.root), self.root / "asset.stl")

    def test_traversal_rejected(self):
        with self.assertRaises(ValueError):
            source_path("../outside.stl", self.root)

    def test_absolute_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            destination_path(self.root.parent / "escaped.stl", self.root)

    def test_unsupported_type_rejected(self):
        with self.assertRaises(ValueError):
            destination_path("script.py", self.root)

    def test_existing_destination_requires_override(self):
        with self.assertRaises(FileExistsError):
            destination_path("asset.stl", self.root)

    def test_input_cannot_be_output_even_with_override(self):
        with self.assertRaises(ValueError):
            destination_path("asset.stl", self.root, source=self.root / "asset.stl", overwrite=True)

    def test_missing_output_parent_is_rejected(self):
        with self.assertRaises(FileNotFoundError):
            destination_path("missing/mesh.stl", self.root)

    def test_symlink_escape_is_rejected_if_supported(self):
        target = self.root.parent / "outside-mesh.stl"
        target.write_text("outside", encoding="utf-8")
        self.addCleanup(lambda: target.unlink(missing_ok=True))
        link = self.root / "linked.stl"
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation requires additional permissions.")
        with self.assertRaises(ValueError):
            source_path(link, self.root)


if __name__ == "__main__":
    unittest.main()
