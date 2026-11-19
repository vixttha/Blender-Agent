"""Regression checks for the immutable Code Stack archive."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import code_stack_maps as maps


class ArchiveIdentityTests(unittest.TestCase):
    def test_rejects_a_mode_only_change(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(maps, "ROOT", Path(directory)):
            maps.git("init", "--quiet")
            version = "v0.0.1"
            path = f"{version}/tool.py"
            source = Path(directory, path)
            source.parent.mkdir()
            source.write_text("pass\n", encoding="utf-8")
            maps.git("add", "--chmod=-x", "--", path)
            pinned = maps.git("write-tree").decode().strip()
            pinned_mode, pinned_blob = maps.verify_archived_files(pinned, version, pinned)[path]

            maps.git("update-index", "--chmod=+x", "--", path)
            changed = maps.git("write-tree").decode().strip()
            changed_mode, changed_blob = maps.version_files(changed, version)[path]
            self.assertEqual((pinned_mode, changed_mode), ("100644", "100755"))
            self.assertEqual(pinned_blob, changed_blob)
            with self.assertRaisesRegex(ValueError, "paths, blobs, or modes differ"):
                maps.verify_archived_files(pinned, version, changed)


if __name__ == "__main__":
    unittest.main()
