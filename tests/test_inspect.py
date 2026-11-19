import hashlib
import struct
import tempfile
import unittest
from pathlib import Path

from blender_agent.inspect import inspect_asset


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_binary_stl_count_hash_and_bounds(self):
        header = b"BINARY STL" + b"\x00" * (80 - len(b"BINARY STL"))
        triangle = struct.pack("<12fH", 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0)
        data = header + struct.pack("<I", 1) + triangle
        (self.root / "model.stl").write_bytes(data)
        info = inspect_asset("model.stl", self.root)
        self.assertEqual(info["triangles"], 1)
        self.assertEqual(info["encoding"], "binary")
        self.assertEqual(info["bounds"], {"min": [0.0, 0.0, 0.0], "max": [1.0, 1.0, 0.0]})
        self.assertEqual(info["sha256"], hashlib.sha256(data).hexdigest())

    def test_ascii_stl(self):
        (self.root / "shape.stl").write_text(
            "solid shape\nfacet normal 0 0 1\nouter loop\n"
            "vertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\n"
            "endloop\nendfacet\nendsolid shape\n", encoding="utf-8")
        info = inspect_asset("shape.stl", self.root)
        self.assertEqual(info["triangles"], 1)
        self.assertEqual(info["encoding"], "ascii")

    def test_truncated_binary_stl_fails(self):
        (self.root / "bad.stl").write_bytes(b"binary" + b"\x00" * 74 + struct.pack("<I", 1))
        with self.assertRaises(ValueError):
            inspect_asset("bad.stl", self.root)

    def test_obj_vertices_faces(self):
        (self.root / "shape.obj").write_text(
            "v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n", encoding="utf-8")
        info = inspect_asset("shape.obj", self.root)
        self.assertEqual(info["vertices"], 3)
        self.assertEqual(info["faces"], 1)

    def test_obj_bad_vertex_fails(self):
        (self.root / "bad.obj").write_text("v NaN 0 0\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            inspect_asset("bad.obj", self.root)

    def test_metadata_only_for_blend(self):
        (self.root / "project.blend").write_bytes(b"BLENDER")
        info = inspect_asset("project.blend", self.root)
        self.assertEqual(info["format"], "blend")
        self.assertNotIn("faces", info)


if __name__ == "__main__":
    unittest.main()
