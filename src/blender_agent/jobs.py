"""Run narrowly-scoped, non-interactive Blender jobs on isolated output paths."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from .paths import destination_path, root_path, source_path

PRIMITIVES = frozenset({"cube", "uv_sphere", "cylinder"})
DEFAULT_TIMEOUT = 180
MAX_TIMEOUT = 900


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
    if not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT:
        raise ValueError("Timeout must be between 1 and 900 seconds.")
    if operation == "create":
        if kind not in PRIMITIVES:
            raise ValueError("Choose cube, uv_sphere, or cylinder.")
        if not 0 < size <= 10000:
            raise ValueError("Primitive size must be between 0 and 10000.")
        input_path = None
    else:
        if source is None:
            raise ValueError("Source path is required.")
        input_path = source_path(source, root_path(workspace))
    root = root_path(workspace)
    final = destination_path(output, root, source=input_path, overwrite=overwrite)
    executable = shutil.which(blender)
    if executable is None:
        raise FileNotFoundError("Blender executable not found; install Blender and configure --blender.")
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
        try:
            completed = subprocess.run(
                command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, timeout=timeout, check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("Blender operation exceeded its timeout.") from exc
        if completed.returncode != 0:
            raise RuntimeError("Blender operation failed: " + completed.stdout[-2000:])
        if not temporary.is_file() or temporary.stat().st_size == 0 or not report.is_file():
            raise RuntimeError("Blender did not produce a verifiable output and report.")
        details = json.loads(report.read_text(encoding="utf-8"))
        # File replacement happens only after the worker exits successfully.
        if final.exists() and not overwrite:
            raise FileExistsError("Destination appeared during execution.")
        os.replace(temporary, final)
    return {
        "ok": True, "operation": operation, "output": str(final.relative_to(root)),
        "size_bytes": final.stat().st_size, "geometry": details,
        "note": "Geometry summary only; not a production or printability certification.",
    }
