"""Build and check Graphify snapshots for unapproved Blender-Agent candidates.

An unapproved PR head must never enter catalog/versions.json.
Snapshots stay in candidates/, isolated from approved version archives.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import tempfile
from pathlib import Path

from github_provenance import report_provenance
from traceability import validate_features
from version_maps import (
    REPOSITORY,
    ROOT,
    check_path,
    generated_files,
    git,
    make_map,
    read_source,
    semver,
    verify_mcp,
)

CATALOG = ROOT / "catalog" / "candidates.json"
ARCHIVE = ROOT / "candidates"
BRANCH = re.compile(r"[A-Za-z0-9._/-]{1,160}\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")


def validate_catalog(payload: object) -> list[dict]:
    if not isinstance(payload, dict) or set(payload) != {"schema_version", "repository", "candidates"}:
        raise ValueError("Candidate catalog schema mismatch")
    if payload["schema_version"] != 1 or payload["repository"] != REPOSITORY:
        raise ValueError("Wrong repository or catalog schema version")
    entries = payload["candidates"]
    if not isinstance(entries, list):
        raise ValueError("Candidates must be a list")
    tags: set[str] = set()
    for item in entries:
        if not isinstance(item, dict) or set(item) - {"features"} != {
            "version", "source_commit", "source_branch", "source_pr", "source_files"
        }:
            raise ValueError("Invalid candidate record")
        tag, sha, branch, number, paths = (
            item["version"], item["source_commit"], item["source_branch"],
            item["source_pr"], item["source_files"]
        )
        if not isinstance(tag, str):
            raise ValueError("Invalid candidate version")
        semver(tag)
        if tag in tags:
            raise ValueError("Duplicate candidate version")
        tags.add(tag)
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            raise ValueError("Candidate must pin full source commit")
        if (
            not isinstance(branch, str) or not BRANCH.fullmatch(branch)
            or branch.startswith(("/", "-")) or ".." in branch or "//" in branch
            or branch.endswith(("/", "."))
        ):
            raise ValueError("Invalid candidate source branch")
        if type(number) is not int or number <= 0:
            raise ValueError("Invalid candidate PR number")
        if not isinstance(paths, list) or not 1 <= len(paths) <= 64:
            raise ValueError("Candidate must have bounded source document list")
        for path in paths:
            check_path(path)
        if len(set(paths)) != len(paths) or paths != sorted(paths):
            raise ValueError("Candidate source documents must be unique and sorted")
        if "features" in item:
            validate_features(item["features"], paths)
    return entries


def read_sources(item: dict) -> dict[str, str]:
    sha = item["source_commit"]
    try:
        if git("cat-file", "-t", sha).decode().strip() != "commit":
            raise ValueError("Candidate source is not a commit")
    except subprocess.CalledProcessError as exc:
        raise ValueError("Pinned candidate commit missing from checkout: " + sha) from exc
    return {path: read_source(sha, path) for path in item["source_files"]}


def build(output: Path, entries: list[dict]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Blender-Agent release candidates",
        "",
        "**These are proposed versions only, not approved releases.**",
        "Do not promote these maps to versions/ without an approved release and verified tag.",
        "",
    ]
    for item in entries:
        tag = item["version"]
        dest = output / tag
        receipt = make_map(
            tag, item["source_commit"], read_sources(item), dest,
            candidate=True, features=item.get("features"),
        )
        receipt["source_pr"] = item["source_pr"]
        receipt["source_branch"] = item["source_branch"]
        (dest / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        info = dest / "README.md"
        data = info.read_text(encoding="utf-8")
        data += "\n[Review the source PR](https://github.com/" + REPOSITORY + "/pull/" + str(item["source_pr"]) + ")\n"
        info.write_text(data, encoding="utf-8")
        asyncio.run(verify_mcp(dest / "graph.json", receipt))
        lines.append("- [" + tag + "](" + tag + "/README.md) — PR #" +
                     str(item["source_pr"]) + ", pinned source " + item["source_commit"])
        print(tag + ": candidate Graphify MCP read-back PASS")
    lines.extend(["", "[Approved version archive](../versions/README.md)"])
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify(output: Path) -> None:
    expected = generated_files(output)
    actual = generated_files(ARCHIVE)
    differences = sorted(set(expected) ^ set(actual))
    differences += sorted(path for path in set(expected) & set(actual)
                          if expected[path] != actual[path])
    if differences:
        for path in differences:
            print("Candidate archive mismatch: candidates/" + path)
        raise ValueError("Candidate graphs differ from deterministic rebuild")
    print("Graphify candidate archive deterministic check PASS")


def export(output: Path) -> None:
    for path, data in sorted(generated_files(output).items()):
        content = data.decode("utf-8")
        chunks = [content[i:i + 1200] for i in range(0, len(content), 1200)]
        for index, chunk in enumerate(chunks):
            print("GRAPHIFY_CANDIDATE_EXPORT " + json.dumps({
                "path": path,
                "index": index,
                "total": len(chunks),
                "chunk": chunk,
            }, ensure_ascii=True))
    print("Graphify candidate export complete")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--generate", action="store_true", help="Write reviewed candidate maps")
    group.add_argument("--emit", action="store_true", help="Print generated files in bounded JSON chunks")
    args = parser.parse_args()
    entries = validate_catalog(json.loads(CATALOG.read_text(encoding="utf-8")))
    report_provenance(entries)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "candidates"
        build(out, entries)
        if args.emit:
            export(out)
        elif args.generate:
            for path, data in generated_files(out).items():
                target = ARCHIVE / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        else:
            verify(out)


if __name__ == "__main__":
    main()
