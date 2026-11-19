import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from blender_agent.jobs import execute


class JobTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "input.stl").write_bytes(b"untouched")

    @staticmethod
    def fake_success(command, **kwargs):
        job = json.loads(Path(command[-1]).read_text(encoding="utf-8"))
        Path(job["output"]).write_bytes(b"mock-export")
        Path(job["report"]).write_text(
            json.dumps({"mesh_objects": 1, "vertices": 8, "faces": 6,
                        "boundary_edges": 0, "nonmanifold_edges": 0}), encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "blender mock output")

    def test_create_promotes_checked_output(self):
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs.subprocess.run", side_effect=self.fake_success) as runner:
            info = execute("create", workspace=self.root, output="cube.stl", kind="cube")
        self.assertTrue(info["ok"])
        self.assertEqual((self.root / "cube.stl").read_bytes(), b"mock-export")
        self.assertIn("--disable-autoexec", runner.call_args.args[0])
        self.assertEqual(runner.call_args.kwargs["shell"] if "shell" in runner.call_args.kwargs else False, False)

    def test_convert_never_modifies_input(self):
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs.subprocess.run", side_effect=self.fake_success):
            execute("convert", workspace=self.root, source="input.stl", output="export.glb")
        self.assertEqual((self.root / "input.stl").read_bytes(), b"untouched")

    def test_missing_blender_gives_clear_error(self):
        with patch("blender_agent.jobs.shutil.which", return_value=None):
            with self.assertRaises(FileNotFoundError):
                execute("create", workspace=self.root, output="cube.obj", kind="cube")

    def test_failure_does_not_publish_output(self):
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs.subprocess.run",
                   return_value=subprocess.CompletedProcess([], 17, "script error")):
            with self.assertRaises(RuntimeError):
                execute("repair", workspace=self.root, source="input.stl", output="repair.stl")
        self.assertFalse((self.root / "repair.stl").exists())
        self.assertEqual((self.root / "input.stl").read_bytes(), b"untouched")

    def test_output_collision_rejected(self):
        (self.root / "cube.stl").write_bytes(b"existing")
        with self.assertRaises(FileExistsError):
            execute("create", workspace=self.root, output="cube.stl", kind="cube")

    def test_invalid_operation_rejected(self):
        with self.assertRaises(ValueError):
            execute("run_python", workspace=self.root, output="cube.stl")

    def test_invalid_timeout_rejected(self):
        with self.assertRaises(ValueError):
            execute("create", workspace=self.root, output="cube.stl", kind="cube", timeout=10000)

    def test_source_is_never_destination(self):
        with self.assertRaises(ValueError):
            execute("repair", workspace=self.root, source="input.stl",
                    output="input.stl", overwrite=True)


if __name__ == "__main__":
    unittest.main()
