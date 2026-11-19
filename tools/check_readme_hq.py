"""Read-only validation for the Blender-Agent README HQ documentation branch."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

REQUIRED = (
    "README.md",
    "readme-hq/README.md",
    "readme-hq/versions/README.md",
    "readme-hq/versions/v0.0.1/README.md",
    "readme-hq/versions/v0.0.1/GUIDE.md",
    "readme-hq/versions/v0.0.1/CHANGELOG.md",
    "readme-hq/workspace/README.md",
    "readme-hq/workspace/v0.0.1/README.md",
    "versions/README.md",
    "workspace/README.md",
    "workspace/v0.0.1/README.md",
    "workspace/v0.0.1/DRAFT.md",
    "workspace/v0.0.1/CHANGELOG.md",
    "workspace/v0.0.1/REVIEW.md",
    "graphify/README.md",
    ".github/workflows/readme-hq.yml",
)
LINK = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
SECRET = re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_-]{10,}")
PRIVATE_PATH = re.compile(r"(?i)(?:C:\\Users\\|/Users/[^/\s]+/|/home/[^/\s]+/)")
PINNED = "45726472fbe7f32de32f87426dc0b21b8fc1e8f7"


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")
    if errors:
        return errors

    for live, archive in (
        ("README.md", "readme-hq/versions/v0.0.1/README.md"),
        ("readme-hq/README.md", "readme-hq/versions/v0.0.1/GUIDE.md"),
    ):
        if (root / live).read_bytes() != (root / archive).read_bytes():
            errors.append(f"archived HQ baseline drift: {live}")

    draft = (root / "workspace/v0.0.1/DRAFT.md").read_text(encoding="utf-8")
    if PINNED not in (root / "workspace/v0.0.1/README.md").read_text(encoding="utf-8"):
        errors.append("workspace source commit pin missing")
    if "not yet available" not in draft.lower() or "not shipped" not in draft.lower():
        errors.append("public draft must distinguish unreleased and planned features")
    if "Draft" not in (root / "versions/README.md").read_text(encoding="utf-8"):
        errors.append("public version index must say the current homepage is a draft")

    # Validate navigation on HQ source pages. The candidate homepage is intentionally
    # excluded: its relative links target the implementation branch's future main tree.
    workspace_pages = {page.relative_to(root).as_posix() for page in (root / "workspace").glob("v*/*.md")}
    for rel in sorted(set(REQUIRED) | workspace_pages):
        if not rel.endswith(".md") or rel == "workspace/v0.0.1/DRAFT.md":
            continue
        path = root / rel
        content = path.read_text(encoding="utf-8")
        if EMAIL.search(content):
            errors.append(f"public email address in {rel}")
        if SECRET.search(content):
            errors.append(f"credential-like assignment in {rel}")
        if PRIVATE_PATH.search(content):
            errors.append(f"personal home-directory path in {rel}")
        for raw in LINK.findall(content):
            dest = raw.strip().split(" ", 1)[0].strip("<>")
            parsed = urlsplit(dest)
            if parsed.scheme or parsed.netloc or dest.startswith("#") or dest.startswith("//"):
                continue
            candidate = (path.parent / unquote(parsed.path)).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                errors.append(f"link escapes repository: {rel} -> {dest}")
                continue
            if not candidate.exists():
                errors.append(f"broken local link: {rel} -> {dest}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    for problem in errors:
        print("FAIL:", problem)
    if errors:
        return 1
    print("PASS: README HQ v0.0.1 snapshots, required files, draft status, and branch navigation")
    print("NOTE: GitHub-hosted CI, external HTTP links, and application tests require separate evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
