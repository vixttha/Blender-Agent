"""Capture the verified walkthrough output used by the still-pilot composition."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PILOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PILOT.parents[2] / "tools"))

from check_readme_walkthrough import README, RELEASE_SHA, run_walkthrough

with tempfile.TemporaryDirectory(prefix="bart-pilot-") as directory:
    temp = Path(directory)
    run_walkthrough(README.read_text(encoding="utf-8"), temp)
    result = json.loads((temp / "triangle-result.json").read_text(encoding="utf-8"))

fields = ("format", "vertices", "faces", "size_bytes", "sha256")
inspection = {field: result[field] for field in fields}
inspection["source_sha"] = RELEASE_SHA
encoded = json.dumps(inspection, indent=2)
evidence = PILOT / "evidence"
evidence.mkdir(exist_ok=True)
(evidence / "inspection.json").write_text(encoded + "\n", encoding="utf-8")
(PILOT / "assets" / "inspection.js").write_text(
    "window.bartPilotInspection = " + encoded + ";\n", encoding="utf-8"
)
