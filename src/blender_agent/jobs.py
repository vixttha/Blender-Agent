"""Narrow, bounded Blender operations with atomic no-clobber output publication."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path

from .obj_records import obj_records
from .paths import destination_path, root_path, source_path, within_workspace

PRIMITIVES = frozenset({"cube", "uv_sphere", "cylinder"})
DEFAULT_TIMEOUT = 180
MAX_TIMEOUT = 900
MAX_INPUT_BYTES = 512 * 1024 * 1024
MAX_OUTPUT_BYTES = 512 * 1024 * 1024
MAX_LOG_BYTES = 256 * 1024


def _run_blender(command: list[str], cwd: Path, timeout: int) -> str:
    """Read process output incrementally and kill processes exceeding the log cap."""
    chunks: list[bytes] = []
    used = 0
    exceeded = threading.Event()
    process = subprocess.Popen(
        command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    assert process.stdout is not None

    def drain() -> None:
        nonlocal used
        try:
            while True:
                data = process.stdout.read(8192)
                if not data:
                    break
                used += len(data)
                if used > MAX_LOG_BYTES:
                    exceeded.set()
                    try:
                        process.kill()
                    except OSError:
                        pass
                    break
                chunks.append(data)
        finally:
            process.stdout.close()

    thread = threading.Thread(target=drain, daemon=True)
    thread.start()
    try:
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            process.kill()
            process.wait()
            raise RuntimeError("Blender operation exceeded its timeout.") from exc
    finally:
        thread.join(timeout=5)
    if exceeded.is_set():
        raise RuntimeError("Blender output exceeded the log-size safety limit.")
    log = b"".join(chunks).decode("utf-8", errors="replace")[-2000:]
    if code != 0:
        raise RuntimeError("Blender operation failed: " + log)
    return log


def _validate_publication(temp: Path, final: Path, root: Path) -> int:
    if not temp.is_file() or temp.is_symlink():
        raise RuntimeError("Temporary result is not a regular file.")
    size = temp.stat().st_size
    if not 0 < size <= MAX_OUTPUT_BYTES:
        raise RuntimeError("Generated output is empty or exceeds the size limit.")
    if final.parent.is_symlink() or final.parent.resolve() != final.parent:
        raise ValueError("Output directories must not be symlinks.")
    if temp.parent.resolve() != temp.parent:
        raise ValueError("Temporary directory was unexpectedly moved.")
    if final.is_symlink() or within_workspace(final, root) != final:
        raise ValueError("Output path must remain a regular path inside the workspace.")
    if within_workspace(temp, root) != temp:
        raise ValueError("Temporary path changed outside the workspace.")
    return size


def _publish(temp: Path, final: Path, root: Path, *, overwrite: bool) -> None:
    """Create a destination exclusively, or replace it with explicit permission."""
    _validate_publication(temp, final, root)
    if overwrite:
        if final.exists() and not final.is_file():
            raise FileExistsError("Destination is not a regular file.")
        os.replace(temp, final)
    else:
        # No check-then-replace race: an existing name is never overwritten.
        os.link(temp, final)


def _material_libraries(obj: Path):
    with obj.open(encoding="utf-8-sig", errors="surrogateescape") as stream:
        for line in obj_records(stream):
            parts = line.split(None, 1)
            if len(parts) == 2 and parts[0] == "mtllib":
                yield parts[1].strip().removeprefix('"').removesuffix('"')


def _publish_obj(temp: Path, final: Path, root: Path, *, source: Path | None, overwrite: bool) -> Path:
    """Publish the material library first and undo that change if publishing the OBJ fails."""
    material = final.with_suffix(".mtl")
    staged = temp.with_suffix(".mtl")
    size = _validate_publication(temp, final, root)
    if not staged.is_file():
        raise RuntimeError("Blender did not produce the OBJ material library.")
    if size + _validate_publication(staged, material, root) > MAX_OUTPUT_BYTES:
        raise RuntimeError("Combined OBJ and material library exceed the output size limit.")
    if next(_material_libraries(temp), None) != material.name:
        raise RuntimeError("OBJ does not reference its matching material library.")

    # Serialize publication by material filename, including explicit CLI replacements.
    key = hashlib.sha256(os.fsencode(material.name.casefold())).hexdigest()
    lock = final.parent / f".blender-agent-obj-{key}.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise FileExistsError("Destination already exists or another OBJ export is publishing it.") from exc
    try:
        _validate_publication(temp, final, root)
        _validate_publication(staged, material, root)
        backup = None
        if material.exists():
            if not overwrite or not material.is_file():
                raise FileExistsError("Destination already exists: OBJ material library.")
            if source is not None and source.suffix.lower() == ".obj":
                if source.with_suffix(".mtl").resolve() == material or any(
                    (source.parent / name).resolve() == material for name in _material_libraries(source)
                ):
                    raise ValueError("Source material libraries cannot be modified in place.")
            backup = temp.parent / "previous-material"
            os.link(material, backup)

        published = staged.stat()
        _publish(staged, material, root, overwrite=backup is not None)
        try:
            _publish(temp, final, root, overwrite=overwrite)
        except (OSError, ValueError, RuntimeError):
            if material.exists() and os.path.samestat(published, material.stat()):
                if backup is None:
                    material.unlink()
                else:
                    os.replace(backup, material)
            raise
    finally:
        lock.rmdir()
    return material


def execute(
    operation: str,
    *,
    workspace: str | Path = ".",
    source: str | Path | None = None,
    output: str | Path,
    kind: str | None = None,
    size: float = 1.0,
    blender: str = "blender",
    overwrite: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    if operation not in {"create", "convert", "repair"}:
        raise ValueError("Unknown operation.")
    if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= MAX_TIMEOUT:
        raise ValueError("Timeout must be between 1 and 900 seconds.")
    root = root_path(workspace)
    if operation == "create":
        if kind not in PRIMITIVES:
            raise ValueError("Choose cube, uv_sphere, or cylinder.")
        if not isinstance(size, (float, int)) or not math.isfinite(size) or not 0 < size <= 10000:
            raise ValueError("Primitive size must be finite and between 0 and 10000.")
        input_path = None
    else:
        if source is None:
            raise ValueError("Source path is required.")
        input_path = source_path(source, root)
        if input_path.stat().st_size > MAX_INPUT_BYTES:
            raise ValueError("Source file exceeds the size limit.")
    final = destination_path(output, root, source=input_path, overwrite=overwrite)
    if final.parent.is_symlink() or final.parent.resolve() != final.parent:
        raise ValueError("Output directories must not be symlinks.")
    executable = shutil.which(blender)
    if executable is None:
        raise FileNotFoundError("Blender executable not found; configure --blender.")
    worker = Path(__file__).with_name("blender_worker.py")
    with tempfile.TemporaryDirectory(prefix=".blender-agent-", dir=final.parent) as directory:
        temporary = Path(directory) / final.name
        report = Path(directory) / "report.json"
        job = Path(directory) / "job.json"
        job.write_text(json.dumps({
            "operation": operation,
            "source": str(input_path) if input_path else None,
            "output": str(temporary),
            "report": str(report),
            "kind": kind,
            "size": size,
        }), encoding="utf-8")
        command = [
            executable, "--background", "--factory-startup", "--disable-autoexec",
            "--python-exit-code", "17", "--python", str(worker), "--", str(job),
        ]
        _run_blender(command, cwd=root, timeout=timeout)
        if not temporary.is_file() or not report.is_file():
            raise RuntimeError("Blender did not produce the output and geometry report.")
        if temporary.stat().st_size == 0 or temporary.stat().st_size > MAX_OUTPUT_BYTES:
            raise RuntimeError("Generated output is empty or exceeds the size limit.")
        details = json.loads(report.read_text(encoding="utf-8"))
        if not isinstance(details, dict) or details.get("mesh_objects", 0) < 1:
            raise RuntimeError("Blender geometry report is incomplete.")
        material = None
        if final.suffix.lower() == ".obj":
            material = _publish_obj(temporary, final, root, source=input_path, overwrite=overwrite)
        else:
            _publish(temporary, final, root, overwrite=overwrite)
    result = {
        "ok": True, "operation": operation, "output": str(final.relative_to(root)),
        "size_bytes": final.stat().st_size, "geometry": details,
        "note": "Geometry summary only; not a production or printability certification.",
    }
    if material is not None:
        result["material_library"] = str(material.relative_to(root))
    return result
