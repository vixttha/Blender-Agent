"""Bounded, read-only mesh inspection. Counts do not certify model validity."""

from __future__ import annotations

import hashlib
import math
import struct
from pathlib import Path

from .paths import root_path, source_path

MAX_PREVIEW_BYTES = 128 * 1024 * 1024
MAX_VERTICES = 1_000_000
MAX_FACES = 2_000_000


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _bounds(vertices: list[tuple[float, float, float]]) -> dict | None:
    if not vertices:
        return None
    return {
        "min": [min(point[i] for point in vertices) for i in range(3)],
        "max": [max(point[i] for point in vertices) for i in range(3)],
    }


def _stl(path: Path) -> dict:
    length = path.stat().st_size
    if length > MAX_PREVIEW_BYTES:
        raise ValueError("STL exceeds the inspection size limit.")
    with path.open("rb") as stream:
        header = stream.read(84)
        if len(header) >= 84:
            triangles = struct.unpack_from("<I", header, 80)[0]
            if length == 84 + 50 * triangles:
                box_min = [math.inf] * 3
                box_max = [-math.inf] * 3
                for _ in range(triangles):
                    record = stream.read(50)
                    coords = struct.unpack_from("<9f", record, 12)
                    if not all(math.isfinite(v) for v in coords):
                        raise ValueError("Binary STL contains non-finite vertex coordinates.")
                    for axis in range(3):
                        for value in coords[axis::3]:
                            box_min[axis] = min(box_min[axis], value)
                            box_max[axis] = max(box_max[axis], value)
                bounds = {"min": box_min, "max": box_max} if triangles else None
                return {"encoding": "binary", "triangles": triangles, "bounds": bounds}
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Invalid STL: neither consistent binary nor UTF-8 ASCII.") from exc
    lines = [line.strip().split() for line in content.splitlines() if line.strip()]
    if len(lines) < 3 or lines[0][0].lower() != "solid" or lines[-1][0].lower() != "endsolid":
        raise ValueError("Invalid ASCII STL framing.")
    vertices: list[tuple[float, float, float]] = []
    facets = 0
    inside = False
    facet_vertices = 0
    for parts in lines[1:-1]:
        kind = parts[0].lower()
        if kind == "facet":
            if inside or len(parts) != 5 or parts[1].lower() != "normal":
                raise ValueError("Invalid ASCII STL facet.")
            inside, facet_vertices = True, 0
        elif kind == "vertex":
            if not inside or len(parts) != 4:
                raise ValueError("Vertex found outside an ASCII STL facet.")
            try:
                point = tuple(float(x) for x in parts[1:4])
            except ValueError as exc:
                raise ValueError("Invalid ASCII STL vertex.") from exc
            if not all(math.isfinite(v) for v in point):
                raise ValueError("ASCII STL contains non-finite coordinates.")
            vertices.append(point)
            facet_vertices += 1
            if facet_vertices > 3:
                raise ValueError("ASCII STL facet contains too many vertices.")
        elif kind == "endfacet":
            if not inside or facet_vertices != 3:
                raise ValueError("Incomplete ASCII STL facet.")
            inside = False
            facets += 1
        elif kind in {"outer", "endloop"}:
            continue
        else:
            raise ValueError("Unexpected ASCII STL token.")
    if inside or facets == 0 or len(vertices) != facets * 3:
        raise ValueError("Incomplete ASCII STL geometry.")
    return {"encoding": "ascii", "triangles": facets, "bounds": _bounds(vertices)}


def _obj(path: Path) -> dict:
    vertices: list[tuple[float, float, float]] = []
    faces = 0
    with path.open("r", encoding="utf-8-sig", errors="strict") as stream:
        for line in stream:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "v":
                if len(parts) < 4 or len(vertices) >= MAX_VERTICES:
                    raise ValueError("Invalid OBJ vertex or vertex count limit exceeded.")
                try:
                    point = tuple(float(x) for x in parts[1:4])
                except ValueError as exc:
                    raise ValueError("Invalid OBJ vertex.") from exc
                if not all(math.isfinite(v) for v in point):
                    raise ValueError("OBJ contains non-finite coordinates.")
                vertices.append(point)
            elif parts[0] == "f":
                if len(parts) < 4 or faces >= MAX_FACES:
                    raise ValueError("Invalid OBJ face or face count limit exceeded.")
                for token in parts[1:]:
                    vertex_ref = token.split("/")[0]
                    try:
                        index = int(vertex_ref)
                    except ValueError as exc:
                        raise ValueError("Invalid OBJ vertex reference.") from exc
                    if index == 0 or (index > 0 and index > len(vertices)) or (
                        index < 0 and -index > len(vertices)
                    ):
                        raise ValueError("OBJ face references a missing vertex.")
                faces += 1
    return {"vertices": len(vertices), "faces": faces, "bounds": _bounds(vertices)}


def inspect_asset(path: str | Path, workspace: str | Path = ".") -> dict:
    root = root_path(workspace)
    source = source_path(path, root)
    size = source.stat().st_size
    if size > 512 * 1024 * 1024:
        raise ValueError("File exceeds the metadata inspection size limit.")
    if source.suffix.lower() in {".stl", ".obj"} and size > MAX_PREVIEW_BYTES:
        raise ValueError("File exceeds the inspection size limit.")
    info = {
        "name": source.name, "format": source.suffix.lower()[1:],
        "size_bytes": size, "sha256": _sha256(source),
        "inspection": "structure_only",
        "limitations": "Does not prove manifoldness, printability, visual quality or game readiness.",
    }
    if source.suffix.lower() in {".stl", ".obj"}:
        if size > MAX_PREVIEW_BYTES:
            raise ValueError("File exceeds the inspection size limit.")
        if source.suffix.lower() == ".stl":
            info.update(_stl(source))
        else:
            info.update(_obj(source))
    else:
        info["limitations"] += " This format has metadata-only inspection without Blender."
    return info
