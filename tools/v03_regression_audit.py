"""Read-only v0.0.3 audit cases using ordinary temporary mesh fixtures."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from blender_agent import __version__


def report(case, result):
    print("V03_AUDIT " + json.dumps({"case": case, **result}), flush=True)


def cli(workspace, *args, blender=None):
    command = [sys.executable, "-m", "blender_agent", "--workspace", str(workspace)]
    if blender is not None:
        command += ["--blender", str(blender)]
    result = subprocess.run([*command, *args], capture_output=True, text=True, timeout=80)
    return {
        "returncode": result.returncode,
        "value": json.loads(result.stdout) if result.stdout else None,
        "error": json.loads(result.stderr).get("error") if result.stderr else None,
    }


def inspect_cases(workspace):
    ascii_stl = """solid audit
facet normal 0 0 1
outer loop
vertex 0 0 0
vertex 1 0 0
vertex 0 1 0
endloop
endfacet
endsolid audit
"""
    cases = {
        "stl-valid": ascii_stl,
        "stl-no-loop": ascii_stl.replace("outer loop\n", "").replace("endloop\n", ""),
        "stl-wrong-loop": ascii_stl.replace("outer loop", "outer unrelated"),
        "stl-no-closing-loop": ascii_stl.replace("endloop\n", ""),
    }
    for case, fixture in cases.items():
        filename = case + ".stl"
        (workspace / filename).write_text(fixture, encoding="ascii")
        result = cli(workspace, "inspect", filename)
        report(case, result)
        if case == "stl-valid":
            assert result["returncode"] == 0 and result["value"]["triangles"] == 1

    vertices = "v 0 0 0\nv 1 0 0\nv 0 1 0\n"
    for case, face in (
        ("obj-plain", "f 1 2 3\n"),
        ("obj-inline-comment", "f 1 2 3 # triangle face\n"),
        ("obj-full-line-comment", "# triangle face\nf 1 2 3\n"),
    ):
        filename = case + ".obj"
        (workspace / filename).write_text(vertices + face, encoding="ascii")
        result = cli(workspace, "inspect", filename)
        report(case, result)
        if case != "obj-inline-comment":
            assert result["returncode"] == 0 and result["value"]["faces"] == 1


def blender_cases(workspace, blender):
    for case in ("obj-plain", "obj-inline-comment"):
        destination = case + "-converted.stl"
        result = cli(workspace, "convert", case + ".obj", destination, blender=blender)
        report(case + "-blender-import", result)
        if result["returncode"] == 0:
            report(case + "-blender-output", cli(workspace, "inspect", destination))
        if case == "obj-plain":
            assert result["returncode"] == 0

    for suffix in ("stl", "obj", "glb", "fbx", "blend"):
        for extension in (suffix, suffix.upper()):
            filename = "case-" + extension + "." + extension
            result = cli(workspace, "create", "cube", filename, blender=blender)
            report("export-" + extension, {**result, "requested_file_exists": (workspace / filename).is_file()})
            if extension == suffix:
                assert result["returncode"] == 0

    fixture = """
import bpy
from pathlib import Path

root = Path.cwd()
bpy.ops.wm.read_factory_settings(use_empty=True)
active = bpy.context.scene
bpy.ops.mesh.primitive_cube_add()
extra = bpy.data.scenes.new("Second scene")
mesh = bpy.data.meshes.new("Triangle")
mesh.from_pydata([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [], [(0, 1, 2)])
extra.collection.objects.link(bpy.data.objects.new("Triangle", mesh))
assert len(active.objects) == len(extra.objects) == 1
bpy.ops.wm.save_as_mainfile(filepath=str(root / "two-scenes.blend"))
"""
    script = workspace / "create_two_scenes.py"
    script.write_text(fixture, encoding="utf-8")
    subprocess.run(
        [str(blender), "--background", "--factory-startup", "--disable-autoexec",
         "--python-exit-code", "17", "--python", str(script)],
        cwd=workspace, check=True, capture_output=True, timeout=55,
    )
    converted = cli(workspace, "convert", "two-scenes.blend", "two-scenes.stl", blender=blender)
    report("pre-export-two-scenes", converted)
    if converted["returncode"] == 0:
        report("two-scenes-artifact", cli(workspace, "inspect", "two-scenes.stl"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blender", type=Path)
    args = parser.parse_args()
    assert __version__ == "0.0.3"
    with tempfile.TemporaryDirectory(prefix="v03-audit-") as location:
        workspace = Path(location)
        inspect_cases(workspace)
        if args.blender is not None:
            blender_cases(workspace, args.blender.resolve())


if __name__ == "__main__":
    main()
