"""Exercise the pinned brand verifier with a real project and disposable cases."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
LEGACY = ROOT / "brand-identity"
TRIAL = ROOT / "trials" / "brand-identity-v0.0.2" / "brand-identity"
DECISION = Path("01-strategy/creative-decision.json")
MANIFEST = Path("09-assets/manifest.json")


def verify(kit, *flags, expected_error=None):
    result = subprocess.run(
        [sys.executable, str(kit / "verify.py"), *flags],
        cwd=kit.parent, capture_output=True, text=True,
    )
    output = result.stdout + result.stderr
    if expected_error is None:
        if result.returncode:
            raise RuntimeError(output)
    elif result.returncode == 0 or expected_error not in output:
        raise RuntimeError(f"Expected rejection containing {expected_error!r}. Got {output}")
    print(output.strip(), flush=True)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    verify(TRIAL)
    verify(TRIAL, "--ready-for-artwork", expected_error="Owner name confirmation is required")
    print("TRIAL_BART_PENDING_GATE=PASS")

    with TemporaryDirectory() as directory:
        sandbox = Path(directory)
        kit = sandbox / "brand-identity"
        shutil.copytree(TRIAL, kit, ignore=shutil.ignore_patterns("__pycache__"))

        manifest = json.loads((LEGACY / MANIFEST).read_text(encoding="utf-8"))
        for asset in manifest["assets"]:
            relative = Path("09-assets") / asset["file"]
            shutil.copyfile(LEGACY / relative, kit / relative)
        write_json(kit / MANIFEST, manifest)
        verify(kit, expected_error="Owner name confirmation is required")
        print("TRIAL_LEGACY_INVENTORY_PENDING=REJECTED")

        decision = json.loads((kit / DECISION).read_text(encoding="utf-8"))
        decision["confirmation"] = {
            **decision["names"], "reference": "Simulated confirmation in a disposable runner fixture",
        }
        write_json(kit / DECISION, decision)
        verify(kit, "--ready-for-artwork")
        print("TRIAL_LEGACY_PNG_INTEGRITY=PASS")
        if not manifest["assets"] or any(asset["status"] != "draft" for asset in manifest["assets"]):
            raise RuntimeError("Expected the two historical draft exports")
        verify(kit, "--ready-for-handoff")
        print("FINDING_DRAFT_HANDOFF=REPRODUCED")

        evidence = sandbox / "docs" / "evidence.md"
        evidence.parent.mkdir()
        evidence.write_text("# Project evidence\n", encoding="utf-8")
        brief = kit / "01-strategy" / "brief.md"
        link = Path(os.path.relpath(evidence, brief.parent)).as_posix()
        brief.write_text(brief.read_text(encoding="utf-8") + f"\n[Project evidence]({link})\n", encoding="utf-8")
        verify(kit, expected_error="missing or external local path")
        print("FINDING_PROJECT_RELATIVE_LINK=REPRODUCED")


if __name__ == "__main__":
    main()
