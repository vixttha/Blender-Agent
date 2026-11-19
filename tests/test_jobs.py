import concurrent.futures
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from blender_agent.jobs import (
    MAX_INPUT_BYTES, MAX_LOG_BYTES, MAX_OUTPUT_BYTES, _publish, _run_blender, execute,
)


class JobTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "input.stl").write_bytes(b"untouched")

    @staticmethod
    def fake_success(command, *, cwd, timeout):
        job = json.loads(Path(command[-1]).read_text(encoding="utf-8"))
        Path(job["output"]).write_bytes(b"mock-export")
        Path(job["report"]).write_text(
            json.dumps({"mesh_objects": 1, "vertices": 8, "faces": 6,
                        "boundary_edges": 0, "nonmanifold_edges": 0}),
            encoding="utf-8",
        )
        return "success"

    @staticmethod
    def fake_obj(command, *, cwd, timeout):
        JobTests.fake_success(command, cwd=cwd, timeout=timeout)
        job = json.loads(Path(command[-1]).read_text(encoding="utf-8"))
        output = Path(job["output"])
        library = output.with_suffix(".mtl")
        output.write_text(f"mtllib {library.name}\n", encoding="utf-8")
        library.write_bytes(b"new material")
        return "success"

    def test_obj_rolls_back_material_when_obj_appears_late(self):
        def late_collision(command, *, cwd, timeout):
            self.fake_obj(command, cwd=cwd, timeout=timeout)
            (self.root / "cube.obj").write_bytes(b"other writer")

        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=late_collision):
            with self.assertRaises(FileExistsError):
                execute("create", workspace=self.root, output="cube.obj", kind="cube")
        self.assertEqual((self.root / "cube.obj").read_bytes(), b"other writer")
        self.assertFalse((self.root / "cube.mtl").exists())

    def test_obj_refuses_missing_material_library(self):
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=self.fake_success):
            with self.assertRaisesRegex(RuntimeError, "did not produce the OBJ material library"):
                execute("create", workspace=self.root, output="cube.obj", kind="cube")
        self.assertFalse((self.root / "cube.obj").exists())

    def test_obj_overwrite_restores_previous_library_if_obj_replace_fails(self):
        obj = self.root / "out.obj"
        material = obj.with_suffix(".mtl")
        obj.write_bytes(b"old obj")
        material.write_bytes(b"old material")
        from os import replace

        def fail_obj_replace(source, destination):
            if destination == obj:
                raise PermissionError("could not replace OBJ")
            replace(source, destination)

        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=self.fake_obj):
            with patch("blender_agent.jobs.os.replace", side_effect=fail_obj_replace):
                with self.assertRaisesRegex(PermissionError, "could not replace OBJ"):
                    execute("convert", workspace=self.root, source="input.stl", output="out.obj", overwrite=True)
            self.assertEqual(obj.read_bytes(), b"old obj")
            self.assertEqual(material.read_bytes(), b"old material")
            info = execute("convert", workspace=self.root, source="input.stl", output="out.obj", overwrite=True)
        self.assertEqual(info["material_library"], "out.mtl")
        self.assertEqual(material.read_bytes(), b"new material")

    def test_obj_overwrite_preserves_material_referenced_by_source(self):
        source = self.root / "input.obj"
        source.write_text('mtllib "out.mtl"\n', encoding="utf-8")
        material = self.root / "out.mtl"
        material.write_bytes(b"source material")
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=self.fake_obj):
            with self.assertRaisesRegex(ValueError, "Source material libraries"):
                execute("convert", workspace=self.root, source="input.obj", output="out.obj", overwrite=True)
        self.assertEqual(material.read_bytes(), b"source material")
        self.assertFalse((self.root / "out.obj").exists())

    def test_create_promotes_checked_output(self):
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=self.fake_success) as runner:
            info = execute("create", workspace=self.root, output="cube.stl", kind="cube")
        self.assertTrue(info["ok"])
        self.assertEqual((self.root / "cube.stl").read_bytes(), b"mock-export")
        self.assertIn("--disable-autoexec", runner.call_args.args[0])

    def test_convert_never_modifies_input(self):
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=self.fake_success):
            execute("convert", workspace=self.root, source="input.stl", output="export.glb")
        self.assertEqual((self.root / "input.stl").read_bytes(), b"untouched")

    def test_missing_blender_fails_cleanly(self):
        with patch("blender_agent.jobs.shutil.which", return_value=None):
            with self.assertRaises(FileNotFoundError):
                execute("create", workspace=self.root, output="cube.obj", kind="cube")

    def test_failure_does_not_publish_output(self):
        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=RuntimeError("worker failed")):
            with self.assertRaises(RuntimeError):
                execute("repair", workspace=self.root, source="input.stl", output="repair.stl")
        self.assertFalse((self.root / "repair.stl").exists())
        self.assertEqual((self.root / "input.stl").read_bytes(), b"untouched")

    def test_existing_output_refused(self):
        (self.root / "cube.stl").write_bytes(b"existing")
        with self.assertRaises(FileExistsError):
            execute("create", workspace=self.root, output="cube.stl", kind="cube")

    def test_unsafe_operation_and_size_refused(self):
        with self.assertRaises(ValueError):
            execute("run_python", workspace=self.root, output="cube.stl")
        for value in (float("nan"), float("inf"), -1, 0, 10001):
            with self.subTest(value=value), self.assertRaises(ValueError):
                execute("create", workspace=self.root, output="cube.stl", kind="cube", size=value)

    def test_invalid_timeout_rejected(self):
        for value in (0, 901, True):
            with self.subTest(timeout=value), self.assertRaises(ValueError):
                execute("create", workspace=self.root, output="cube.stl", kind="cube", timeout=value)

    def test_source_cannot_be_replaced_even_with_overwrite(self):
        with self.assertRaises(ValueError):
            execute("repair", workspace=self.root, source="input.stl",
                    output="input.stl", overwrite=True)

    def test_input_size_cap(self):
        (self.root / "huge.stl").write_bytes(b"")
        with (self.root / "huge.stl").open("r+b") as handle:
            handle.truncate(MAX_INPUT_BYTES + 1)
        with self.assertRaisesRegex(ValueError, "size limit"):
            execute("convert", workspace=self.root, source="huge.stl", output="out.stl")

    def test_oversized_output_never_promoted(self):
        temp = self.root / "temp.stl"
        final = self.root / "final.stl"
        with temp.open("wb") as stream:
            stream.truncate(MAX_OUTPUT_BYTES + 1)
        with self.assertRaises(RuntimeError):
            _publish(temp, final, self.root, overwrite=False)
        self.assertFalse(final.exists())

    def test_atomic_no_overwrite_even_when_destination_appears_late(self):
        temp = self.root / "temp.stl"
        final = self.root / "target.stl"
        temp.write_bytes(b"generated")
        final.write_bytes(b"another writer")
        with self.assertRaises(FileExistsError):
            _publish(temp, final, self.root, overwrite=False)
        self.assertEqual(final.read_bytes(), b"another writer")

    def test_parallel_writers_exactly_one_wins(self):
        barrier = threading.Barrier(2)

        def fake_race(command, *, cwd, timeout):
            job = json.loads(Path(command[-1]).read_text(encoding="utf-8"))
            Path(job["output"]).write_bytes(threading.current_thread().name.encode())
            Path(job["report"]).write_text('{"mesh_objects": 1}', encoding="utf-8")
            barrier.wait(timeout=10)
            return "ok"

        def attempt():
            try:
                return execute("create", workspace=self.root, output="shared.stl", kind="cube")
            except FileExistsError:
                return "collision"

        with patch("blender_agent.jobs.shutil.which", return_value="/bin/blender"), \
             patch("blender_agent.jobs._run_blender", side_effect=fake_race):
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                a = pool.submit(attempt)
                b = pool.submit(attempt)
                results = [a.result(timeout=15), b.result(timeout=15)]
        self.assertEqual(sum(isinstance(result, dict) for result in results), 1)
        self.assertEqual(results.count("collision"), 1)
        self.assertTrue((self.root / "shared.stl").read_bytes().startswith(b"ThreadPoolExecutor-"))

    def test_log_output_cap_terminates_noisy_process(self):
        code = "import sys;sys.stdout.write('x'*" + str(MAX_LOG_BYTES + 100000) + ");sys.stdout.flush()"
        with self.assertRaisesRegex(RuntimeError, "log-size"):
            _run_blender([sys.executable, "-c", code], cwd=self.root, timeout=10)

    def test_subprocess_timeout_is_enforced(self):
        with self.assertRaisesRegex(RuntimeError, "timeout"):
            _run_blender([sys.executable, "-c", "import time;time.sleep(30)"],
                         cwd=self.root, timeout=1)

    def test_subprocess_nonzero_exit_is_failure(self):
        with self.assertRaisesRegex(RuntimeError, "bad data"):
            _run_blender([sys.executable, "-c",
                          "import sys;print('bad data');sys.exit(4)"],
                         cwd=self.root, timeout=10)


if __name__ == "__main__":
    unittest.main()
