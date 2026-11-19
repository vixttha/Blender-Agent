"""Validate README HQ versions and Markdown navigation using the repository's Git objects."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

HQ = "readme-hq"
REPO = "/vixttha/Blender-Agent/"
VERSION = r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
SHA = r"[0-9a-f]{40}"
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)")
LINK_DEFINITION = re.compile(r"(?m)^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)")
HEADING = re.compile(r"(?m)^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"(?ms)^ {0,3}([~`]{3,})[^\n]*\n.*?^ {0,3}\1[~`]*[ \t]*$")
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
SECRET = re.compile(r"""(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*['"]?[A-Za-z0-9_-]{10,}""")
PRIVATE_PATH = re.compile(r"(?i)(?:C:\\Users\\|/Users/[^/\s]+/|/home/[^/\s]+/)")


def git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8",
    )


def headings(content):
    used = set()
    for title in HEADING.findall(FENCE.sub("", content)):
        title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
        slug = re.sub(r"[^\w -]", "", title.lower()).replace(" ", "-")
        unique = slug
        suffix = 1
        while unique in used:
            unique = f"{slug}-{suffix}"
            suffix += 1
        used.add(unique)
    return used


def check_link(root, page, content, raw):
    try:
        url = urlsplit(raw.strip("<>"))
    except ValueError:
        return "malformed link"
    fragment = unquote(url.fragment)
    path = unquote(url.path)
    if url.hostname == "github.com" and path.startswith(REPO):
        route, _, tail = path.removeprefix(REPO).partition("/")
        if route not in ("blob", "tree"):
            return None
        ref, _, path = tail.partition("/")
        if ref == HQ:
            if not path and route == "tree":
                return None
            if not valid_path(path):
                return "link escapes repository"
            target = root / path
            if (route == "blob" and not target.is_file()) or (route == "tree" and not target.is_dir()):
                return f"missing {route} on {HQ}"
        elif re.fullmatch(SHA, ref) or ref == "main":
            # CI fetches main and all reachable refs. Read pins without switching branches.
            commit = "origin/main" if ref == "main" else ref
            if not path and route == "tree":
                return None if git(root, "cat-file", "-e", f"{commit}^{{commit}}").returncode == 0 else "missing Git revision"
            if not valid_path(path):
                return "link escapes repository"
            kind = git(root, "cat-file", "-t", f"{commit}:{path}")
            if kind.returncode or kind.stdout.strip() != route:
                return f"missing {route} in Git revision {ref}"
            if fragment and route == "blob" and path.endswith(".md") and not line_fragment(fragment):
                linked = git(root, "show", f"{commit}:{path}").stdout
                return None if fragment in headings(linked) else "missing Markdown heading"
            return None
        else:
            return None  # Feature branch URLs and external HTTP status are review checks.
    elif url.scheme or url.netloc:
        return None
    elif not path:
        return None if not fragment or fragment in headings(content) or line_fragment(fragment) else "missing Markdown heading"
    else:
        target = page.parent / path
    target = target.resolve()
    if not target.is_relative_to(root):
        return "link escapes repository"
    if not target.exists():
        return "missing local target"
    if fragment and target.is_dir():
        target = target / "README.md"
    if fragment and target.suffix == ".md" and not line_fragment(fragment):
        if not target.is_file() or fragment not in headings(target.read_text(encoding="utf-8")):
            return "missing Markdown heading"
    return None


def valid_path(path):
    parts = PurePosixPath(path)
    return not parts.is_absolute() and ".." not in parts.parts and bool(parts.parts)


def line_fragment(fragment):
    return re.fullmatch(r"L\d+(?:-L\d+)?", fragment)


def check_index(root, rel, required, errors):
    index = root / rel / "README.md"
    if not index.is_file():
        errors.append(f"missing index: {rel}/README.md")
        return []
    rows = Counter(re.findall(rf"(?m)^\|\s*`?({VERSION})`?\s*\|", index.read_text(encoding="utf-8")))
    versions = sorted(
        (path.name for path in index.parent.iterdir() if path.is_dir() and re.fullmatch(VERSION, path.name)),
        key=lambda version: tuple(map(int, version[1:].split("."))),
    )
    if any(count != 1 for count in rows.values()) or set(rows) != set(versions):
        errors.append(f"{rel}/README.md must list each version folder once")
    for version in versions:
        for name in required:
            if not (index.parent / version / name).is_file():
                errors.append(f"missing required file: {rel}/{version}/{name}")
    return versions


def check_frozen(root, baseline, errors):
    if not baseline:
        return
    if not re.fullmatch(SHA, baseline) or git(root, "cat-file", "-e", f"{baseline}^{{commit}}").returncode:
        errors.append("archive baseline is not an available commit")
        return
    for area in ("readme-hq/versions", "versions"):
        old = git(root, "ls-tree", "-d", "--name-only", f"{baseline}:{area}")
        if old.returncode:
            errors.append(f"cannot read archive baseline: {area}")
            continue
        for version in old.stdout.splitlines():
            if not re.fullmatch(VERSION, version):
                continue
            folder = f"{area}/{version}/"
            if git(root, "diff", "--quiet", baseline, "HEAD", "--", folder).returncode:
                errors.append(f"existing archive changed: {folder}")


def validate(root, baseline=None):
    root = root.resolve()
    errors = []
    versions = check_index(root, "readme-hq/versions", ("README.md", "GUIDE.md", "CHANGELOG.md"), errors)
    check_index(root, "readme-hq/workspace", ("README.md",), errors)
    check_index(root, "versions", ("README.md", "CHANGELOG.md"), errors)
    check_index(root, "workspace", ("README.md", "DRAFT.md", "CHANGELOG.md"), errors)
    if not versions:
        errors.append("missing HQ archive")
    else:
        for live, archived in (("README.md", "README.md"), ("readme-hq/README.md", "GUIDE.md")):
            archive = root / "readme-hq/versions" / versions[-1] / archived
            if not (root / live).is_file() or (archive.is_file() and (root / live).read_bytes() != archive.read_bytes()):
                errors.append(f"latest HQ snapshot drift: {live}")

    for page in sorted(root.rglob("*.md")):
        rel = page.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if not page.resolve().is_relative_to(root):
            errors.append(f"{rel}: Markdown file escapes repository")
            continue
        content = page.read_text(encoding="utf-8")
        if EMAIL.search(content) or SECRET.search(content) or PRIVATE_PATH.search(content):
            errors.append(f"{rel}: possible personal path, email address, or credential")
        prose = FENCE.sub("", content)
        links = INLINE_LINK.findall(prose) + LINK_DEFINITION.findall(prose)
        for number, raw in enumerate(links, start=1):
            problem = check_link(root, page, content, raw)
            if problem:
                errors.append(f"{rel}: {problem} (link {number})")
    check_frozen(root, baseline, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", help="Prior HQ commit whose archived folders are frozen")
    args = parser.parse_args()
    baseline = None if args.baseline == "0" * 40 else args.baseline
    errors = validate(Path(__file__).resolve().parents[1], baseline)
    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print("PASS: version indexes, archive snapshots and Markdown navigation")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
