"""Read-only mesh-file inspection without starting Blender.

A structural summary is NOT a manifold, printability, or game-readiness test.
"""

from __future__ import annotations

import hashlib
import math
import struct
from pathlib import Path

from .paths import root_path, source_path

MAX_PREVIEW_BYTES = 128 * 1024 * 1024


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
    with path.open("rb") as stream:
        header = stream.read(84)
        if len(header) >= 84:
            triangles = struct.unpack_from("<I", header, 80)[0]
            if length == 84 + 50 * triangles:
                # Binary STL count is authoritative only when the byte length matches.
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
    # ASCII STL: inspect basic structure only; it does not establish watertightness.
    if length > MAX_PREVIEW_BYTES:
        raise ValueError("Unrecognized STL larger than inspection safety limit.")
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Invalid STL: neither a consistent binary STL nor UTF-8 ASCII STL.") from exc
    if not content.lstrip().lower().startswith("solid"):
        raise ValueError("Invalid STL header.")
    vertices: list[tuple[float, float, float]] = []
    facets = 0
    for line in content.splitlines():
        parts = line.strip().split()
        if len(parts) >= 2 and parts[:2] == ["facet", "normal"]:
            facets += 1
        if len(parts) == 4 and parts[0] == "vertex":
            try:
                point = tuple(float(x) for x in parts[1:4])
            except ValueError as exc:
                raise ValueError("Invalid ASCII STL vertex.") from exc
            if not all(math.isfinite(v) for v in point):
                raise ValueError("ASCII STL contains non-finite vertex coordinates.")
            vertices.append(point)
    if facets == 0 or len(vertices) != facets * 3 or "endsolid" not in content.lower():
        raise ValueError("Invalid or incomplete ASCII STL structure.")
    return {"encoding": "ascii", "triangles": facets, "bounds": _bounds(vertices)}


def _obj(path: Path) -> dict:
    vertices = []
    faces = 0
    with path.open("r", encoding="utf-8-sig", errors="strict") as stream:
        for line in stream:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "v" and len(parts) >= 4:
                try:
                    point = tuple(float(x) for x in parts[1:4])
                except ValueError as exc:
                    raise ValueError("Invalid OBJ vertex.") from exc
                if not all(math.isfinite(v) for v in point):
                    raise ValueError("OBJ contains non-finite vertex coordinates.")
                vertices.append(point)
            elif parts[0] == "f":
                if len(parts) < 4:
                    raise ValueError("Invalid OBJ face.")
                faces += 1
    return {"vertices": len(vertices), "faces": faces, "bounds": _bounds(vertices)}


def inspect_asset(path: str | Path, workspace: str | Path = ".") -> dict:
    root = root_path(workspace)
    source = source_path(path, root)
    size = source.stat().st_size
    info = {
        "name": source.name, "format": source.suffix.lower()[1:],
        "size_bytes": size, "sha256": _sha256(source),
        "inspection": "structure_only",
        "limitations": "Does not prove manifold geometry, printability, visual quality or game readiness.",
    }
    if source.suffix.lower() == ".stl":
        info.update(_stl(source))
    elif source.suffix.lower() == ".obj":
        if size > MAX_PREVIEW_BYTES:
            raise ValueError("OBJ exceeds read-only inspection safety limit.")
        info.update(_obj(source))
    else:
        info["limitations"] += " Detailed inspection of this format requires Blender."
    return info
