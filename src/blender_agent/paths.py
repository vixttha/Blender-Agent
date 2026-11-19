"""Workspace boundaries for every public entrypoint."""

from pathlib import Path

INPUT_SUFFIXES = frozenset({".stl", ".obj", ".glb", ".fbx", ".blend"})
OUTPUT_SUFFIXES = frozenset({".stl", ".obj", ".glb", ".fbx", ".blend"})


def root_path(workspace: str | Path) -> Path:
    root = Path(workspace).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("Workspace must be an existing directory.")
    return root


def within_workspace(value: str | Path, workspace: Path) -> Path:
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = workspace / candidate
    candidate = candidate.resolve()
    if not candidate.is_relative_to(workspace):
        raise ValueError("Path must remain inside the configured workspace.")
    return candidate


def source_path(value: str | Path, workspace: Path) -> Path:
    candidate = within_workspace(value, workspace)
    if candidate.suffix.lower() not in INPUT_SUFFIXES:
        raise ValueError("Unsupported source format; use STL, OBJ, GLB, FBX, or BLEND.")
    if not candidate.is_file():
        raise FileNotFoundError("Source file does not exist.")
    return candidate


def destination_path(
    value: str | Path, workspace: Path, *,
    source: Path | None = None, overwrite: bool = False
) -> Path:
    candidate = within_workspace(value, workspace)
    if candidate.suffix.lower() not in OUTPUT_SUFFIXES:
        raise ValueError("Unsupported destination format; use STL, OBJ, GLB, FBX, or BLEND.")
    if source is not None and candidate == source:
        raise ValueError("Source files cannot be modified in place.")
    if candidate.exists() and (not candidate.is_file() or not overwrite):
        raise FileExistsError("Destination already exists; choose another path or opt in to overwrite.")
    if not candidate.parent.exists():
        raise FileNotFoundError("Destination directory must already exist.")
    return candidate
