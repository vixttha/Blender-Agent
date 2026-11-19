import hashlib
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from blender_agent.inspect import MAX_PREVIEW_BYTES, inspect_asset


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_binary_stl_count_hash_bounds(self):
        header = b"BINARY STL" + b"\x00" * (80 - len(b"BINARY STL"))
        triangle = struct.pack("<12fH", 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0)
        data = header + struct.pack("<I", 1) + triangle
        (self.root / "model.stl").write_bytes(data)
        info = inspect_asset("model.stl", self.root)
        self.assertEqual(info["triangles"], 1)
        self.assertEqual(info["encoding"], "binary")
        self.assertEqual(info["bounds"], {"min": [0., 0., 0.], "max": [1., 1., 0.]})
        self.assertEqual(info["sha256"], hashlib.sha256(data).hexdigest())

    def test_ascii_stl_mixed_case_tokens(self):
        (self.root / "shape.stl").write_text(
            "SoLiD shape\nFaCeT NORMAL 0 0 1\nOUTER LOOP\n"
            "VERTEX 0 0 0\nVertex 1 0 0\nvertex 0 1 0\n"
            "ENDLOOP\nENDFACET\nENDSoliD shape\n", encoding="utf-8")
        info = inspect_asset("shape.stl", self.root)
        self.assertEqual(info["triangles"], 1)
        self.assertEqual(info["encoding"], "ascii")

    def test_ascii_stl_unterminated_facet(self):
        (self.root / "shape.stl").write_text(
            "solid\nfacet normal 0 0 1\nvertex 0 0 0\nvertex 1 0 0\n"
            "vertex 0 1 0\nendsolid\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            inspect_asset("shape.stl", self.root)

    def test_ascii_stl_extra_facet_vertex(self):
        (self.root / "shape.stl").write_text(
            "solid\nfacet normal 0 0 1\nvertex 0 0 0\nvertex 1 0 0\n"
            "vertex 0 1 0\nvertex 1 1 1\nendfacet\nendsolid\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            inspect_asset("shape.stl", self.root)

    def test_truncated_binary_stl_fails(self):
        (self.root / "bad.stl").write_bytes(b"binary" + b"\x00" * 74 + struct.pack("<I", 1))
        with self.assertRaises(ValueError):
            inspect_asset("bad.stl", self.root)

    def test_binary_nonfinite_vertex_fails(self):
        header = b"\x00" * 80 + struct.pack("<I", 1)
        record = struct.pack("<12fH", 0, 0, 1, float("inf"), 0, 0,
                             1, 0, 0, 0, 1, 0, 0)
        (self.root / "bad.stl").write_bytes(header + record)
        with self.assertRaisesRegex(ValueError, "non-finite"):
            inspect_asset("bad.stl", self.root)

    def test_empty_binary_stl_rejected(self):
        (self.root / "empty.stl").write_bytes(b"\x00" * 80 + struct.pack("<I", 0))
        with self.assertRaisesRegex(ValueError, "no triangles"):
            inspect_asset("empty.stl", self.root)

    def test_empty_obj_rejected(self):
        (self.root / "empty.obj").write_text("# no vertices or faces\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no mesh geometry"):
            inspect_asset("empty.obj", self.root)

    def test_binary_stl_size_cap(self):
        path = self.root / "huge.stl"
        with path.open("wb") as stream:
            stream.truncate(MAX_PREVIEW_BYTES + 1)
        with self.assertRaisesRegex(ValueError, "size limit"):
            inspect_asset("huge.stl", self.root)

    def test_obj_valid_positive_and_negative_references(self):
        (self.root / "shape.obj").write_text(
            "v 0 0 0\nv 1 0 0\nv 0 1 0\n"
            "f 1 2 3\nf -3/-1/-1 -2/-1/-1 -1/-1/-1\n", encoding="utf-8")
        info = inspect_asset("shape.obj", self.root)
        self.assertEqual(info["vertices"], 3)
        self.assertEqual(info["faces"], 2)

    def test_obj_bad_vertex(self):
        (self.root / "bad.obj").write_text("v NaN 0 0\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            inspect_asset("bad.obj", self.root)

    def test_obj_bad_face_reference(self):
        for face in ("f 1 2 4", "f 0 1 2", "f -4 -2 -1", "f nonsense 1 2"):
            with self.subTest(face=face):
                (self.root / "bad.obj").write_text(
                    "v 0 0 0\nv 1 0 0\nv 0 1 0\n" + face + "\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    inspect_asset("bad.obj", self.root)

    def test_obj_truncated_face(self):
        (self.root / "bad.obj").write_text("v 0 0 0\nf 1 2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            inspect_asset("bad.obj", self.root)

    def test_obj_size_cap(self):
        path = self.root / "large.obj"
        with path.open("wb") as stream:
            stream.truncate(MAX_PREVIEW_BYTES + 1)
        with self.assertRaisesRegex(ValueError, "size limit"):
            inspect_asset("large.obj", self.root)

    def test_metadata_only_for_blend(self):
        (self.root / "project.blend").write_bytes(b"BLENDER")
        info = inspect_asset("project.blend", self.root)
        self.assertEqual(info["format"], "blend")
        self.assertNotIn("faces", info)


if __name__ == "__main__":
    unittest.main()
