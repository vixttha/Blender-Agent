"""Exercise ordinary cross-format assets against the published toolkit."""

import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

from blender_agent import __version__


def report(key, **values):
    print("V03_MORE " + json.dumps({"check": key, **values}), flush=True)


def cli(root, blender, *args):
    result = subprocess.run(
        [sys.executable, "-m", "blender_agent", "--workspace", str(root),
         "--blender", str(blender), *args],
        capture_output=True, text=True, timeout=75,
    )
    return {"code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def create_blender_fixtures(root, blender):
    script = root / "create_fixture.py"
    script.write_text("""
import bpy
from pathlib import Path

root = Path.cwd()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add()
bpy.ops.wm.save_as_mainfile(filepath=str(root / "library.blend"))
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(root / "library.blend"), link=True) as (source, dest):
    dest.objects = ["Cube"]
other = bpy.data.scenes.new("Reference scene")
other.collection.objects.link(dest.objects[0])
bpy.ops.mesh.primitive_cube_add()
assert len(bpy.context.scene.objects) == 1
assert bpy.context.scene.objects[0].data.library is None
assert other.objects[0].data.library is not None
bpy.ops.wm.save_as_mainfile(filepath=str(root / "linked-reference.blend"))
""", encoding="utf-8")
    result = subprocess.run(
        [str(blender), "--background", "--factory-startup", "--disable-autoexec",
         "--python-exit-code", "17", "--python", str(script)],
        cwd=root, capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)


def glb_image_count(path):
    if not path.is_file():
        return None
    with path.open("rb") as stream:
        magic, _, _, chunk_length, chunk_type = struct.unpack("<4sIII4s", stream.read(20))
        assert magic == b"glTF" and chunk_type == b"JSON"
        return len(json.loads(stream.read(chunk_length)).get("images", []))


def main():
    assert __version__ == "0.0.3"
    blender = Path(sys.argv[1]).resolve(strict=True)
    triangle = "v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n"
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        for encoding in ("utf-8", "cp1252"):
            name = f"{encoding}.obj"
            (root / name).write_bytes(("# café\n" + triangle).encode(encoding))
            inspection = cli(root, blender, "inspect", name)
            conversion = cli(root, blender, "convert", name, f"{encoding}.stl")
            report("encoded-obj", encoding=encoding, inspection=inspection, conversion=conversion)
            if encoding == "utf-8":
                assert inspection["code"] == 0 and conversion["code"] == 0

        (root / "assets").mkdir()
        (root / "exports").mkdir()
        texture = root / "assets" / "color.png"
        texture.write_bytes(bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010802000000907753de0000000c49444154789c63f8cfc0000003010100c9fe92ef0000000049454e44ae426082"))
        (root / "assets" / "paint.mtl").write_text(
            "newmtl paint\nKd 1 1 1\nmap_Kd color.png\n", encoding="ascii",
        )
        (root / "assets" / "paint.obj").write_text(
            "mtllib paint.mtl\nv 0 0 0\nv 1 0 0\nv 0 1 0\n"
            "vt 0 0\nvt 1 0\nvt 0 1\nusemtl paint\nf 1/1 2/2 3/3\n", encoding="ascii",
        )
        baseline = cli(root, blender, "convert", "assets/paint.obj", "exports/direct.glb")
        exported = cli(root, blender, "convert", "assets/paint.obj", "exports/paint.obj")
        reimport = cli(root, blender, "convert", "exports/paint.obj", "exports/reimport.glb")
        mtl = root / "exports" / "paint.mtl"
        refs = [line for line in mtl.read_text().splitlines() if line.startswith("map_")] if mtl.exists() else []
        report("obj-image", baseline=baseline, exported=exported, reimport=reimport,
               baseline_images=glb_image_count(root / "exports" / "direct.glb"),
               reimport_images=glb_image_count(root / "exports" / "reimport.glb"), texture_refs=refs)

        create_blender_fixtures(root, blender)
        for command in ("convert", "repair"):
            result = cli(root, blender, command, "linked-reference.blend", command + ".stl")
            report("inactive-linked-scene", operation=command, result=result,
                   published=(root / (command + ".stl")).is_file())


if __name__ == "__main__":
    main()
