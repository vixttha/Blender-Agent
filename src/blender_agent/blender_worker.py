"""Trusted static worker executed by Blender, not by the host Python interpreter.

Only fixed, enumerated operations are available; no model-supplied Python is executed.
"""

import json
import sys
from pathlib import Path

import bmesh
import bpy


def _clear():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def _import(path):
    extension = path.suffix.lower()
    if extension == ".blend":
        bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    elif extension == ".stl":
        bpy.ops.wm.stl_import(filepath=str(path))
    elif extension == ".obj":
        bpy.ops.wm.obj_import(filepath=str(path))
    elif extension == ".glb":
        bpy.ops.import_scene.gltf(filepath=str(path))
    elif extension == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(path))
    else:
        raise ValueError("Unsupported import format.")


def _export(path):
    extension = path.suffix.lower()
    if extension == ".blend":
        bpy.ops.wm.save_as_mainfile(filepath=str(path))
    elif extension == ".stl":
        bpy.ops.wm.stl_export(filepath=str(path), export_selected_objects=False)
    elif extension == ".obj":
        bpy.ops.wm.obj_export(filepath=str(path))
    elif extension == ".glb":
        bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB")
    elif extension == ".fbx":
        bpy.ops.export_scene.fbx(filepath=str(path))
    else:
        raise ValueError("Unsupported export format.")


def _create(kind, size):
    if kind == "cube":
        bpy.ops.mesh.primitive_cube_add(size=size)
    elif kind == "uv_sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=size / 2)
    elif kind == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=size / 2, depth=size)
    else:
        raise ValueError("Unsupported primitive.")


def _repair():
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        mesh = obj.data
        bm = bmesh.new()
        try:
            bm.from_mesh(mesh)
            bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=0.0001)
            if bm.faces:
                bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
            bm.to_mesh(mesh)
            mesh.update()
        finally:
            bm.free()


def _geometry():
    total = {"mesh_objects": 0, "vertices": 0, "faces": 0,
             "boundary_edges": 0, "nonmanifold_edges": 0}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        total["mesh_objects"] += 1
        bm = bmesh.new()
        try:
            bm.from_mesh(obj.data)
            total["vertices"] += len(bm.verts)
            total["faces"] += len(bm.faces)
            total["boundary_edges"] += sum(1 for edge in bm.edges if edge.is_boundary)
            total["nonmanifold_edges"] += sum(1 for edge in bm.edges if not edge.is_manifold)
        finally:
            bm.free()
    return total


def main():
    if bpy.app.version < (4, 1, 0):
        raise RuntimeError("Blender 4.1 or newer is required.")
    arguments = sys.argv[sys.argv.index("--") + 1:]
    if len(arguments) != 1:
        raise ValueError("Expected one job manifest path.")
    job = json.loads(Path(arguments[0]).read_text(encoding="utf-8"))
    operation = job["operation"]
    _clear()
    if operation == "create":
        _create(job["kind"], float(job["size"]))
    elif operation in {"convert", "repair"}:
        _import(Path(job["source"]))
        if operation == "repair":
            _repair()
    else:
        raise ValueError("Unknown operation.")
    geometry = _geometry()
    if geometry["mesh_objects"] == 0:
        raise ValueError("No mesh objects are available for output.")
    output = Path(job["output"])
    _export(output)
    Path(job["report"]).write_text(json.dumps(geometry), encoding="utf-8")


if __name__ == "__main__":
    main()
