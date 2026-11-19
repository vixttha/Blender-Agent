#!/usr/bin/env python3
"""Validate the public instructions archive and print exact-commit CI receipts."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = "vixttha/Blender-Agent"
BRANCH = "chatgpt-project-instructions"
REQUIRED = (
    "README.md",
    "v0.0.1/README.md",
    "v0.0.1/CHATGPT_PROJECT_INSTRUCTIONS.md",
    "v0.0.1/ACCEPTANCE.md",
    "graphify/README.md",
    "graphify/versions.json",
    "graphify/versions.mmd",
    ".github/workflows/instructions-archive.yml",
)
NEEDED = (
    "Head — select one feature",
    "Worker — implement",
    "Validate — public GitHub runners",
    "Internal Auditor — verify findings",
    "Head — merge approval and archive",
    "exact tested commit SHA",
    "GitHub-hosted runners",
    "demonstrated gaps",
    "main",
    "graphify/versions.json",
)
def check(condition: bool, explanation: str) -> None:
    if not condition:
        raise AssertionError(explanation)

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path("."))
    p.add_argument("--sha", required=True, help="Actual expected GitHub Actions checkout SHA")
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    root = args.root.resolve()
    check(bool(re.fullmatch(r"[0-9a-f]{40}", args.sha)), "Expected an exact 40-char commit SHA")
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    check(actual == args.sha, f"Checkout mismatch: actual {actual}, expected {args.sha}")
    for rel in REQUIRED:
        check((root / rel).is_file(), f"Missing required file: {rel}")
    doc = (root / "v0.0.1/CHATGPT_PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
    for token in NEEDED:
        check(token.casefold() in doc.casefold(), f"Missing project instruction: {token}")
    check(doc.find("**Head — select one feature.") < doc.find("**Worker — implement.") < doc.find("**Validate — public GitHub runners.") < doc.find("**Internal Auditor — verify findings.") < doc.find("**Head — merge approval and archive."), "Execution stages out of order")
    check("https://github.com/" + REPO in doc, "Missing canonical GitHub URL")
    check("no self-hosted" in doc.casefold(), "No self-hosted requirement missing")
    check("explicit maintainer authorization" in doc, "Maintainer approval requirement missing")
    check("must **not stunt progress**" in doc, "Project finalization guard missing")
    index = json.loads((root / "graphify/versions.json").read_text(encoding="utf-8"))
    info = index["graph"]
    check(info["repository"] == REPO and info["archive_branch"] == BRANCH, "Graph identity mismatch")
    check(info["mcp_verified"] is False and "not Graphify MCP" in info["generator"], "No unverified MCP claim permitted")
    nodes = {item["id"]: item for item in index["nodes"]}
    check(len(nodes) == len(index["nodes"]), "Duplicate graph node IDs")
    edges = index["links"]
    check(all(edge["source"] in nodes and edge["target"] in nodes for edge in edges), "Dangling graph edge")
    versions = sorted((p.name for p in root.iterdir() if p.is_dir() and re.fullmatch(r"v\d+\.\d+\.\d+", p.name)))
    check(versions and versions == sorted(node["directory"] for node in nodes.values() if node.get("kind") == "instructions-version"), "Graph version folders disagree with archive")
    for version in versions:
        for leaf in ("README.md", "ACCEPTANCE.md", "CHATGPT_PROJECT_INSTRUCTIONS.md"):
            check((root / version / leaf).is_file(), f"Missing {version}/{leaf}")
        check(any(e["source"] == "branch:" + BRANCH and e["target"] == "version:" + version and e["relation"] == "contains" for e in edges), f"No branch contains edge for {version}")
    workflow = (root / ".github/workflows/instructions-archive.yml").read_text(encoding="utf-8")
    check("runs-on: ubuntu-latest" in workflow, "Require standard free GitHub-hosted runner")
    check("contents: read" in workflow, "Require read-only token")
    check("REPO_VISIBILITY" in workflow and "RUNNER_KIND" in workflow, "Require visibility/runner checks")
    check("self-hosted" not in re.sub(r"#.*", "", workflow), "Self-hosted runner reference in workflow")
    check("uses:" not in workflow, "External Actions dependency not allowed in baseline workflow")
    check("git rev-parse HEAD" in workflow and "--sha \"$GITHUB_SHA\"" in workflow, "Workflow does not bind verification to exact SHA")
    mermaid = (root / "graphify/versions.mmd").read_text(encoding="utf-8")
    check(all(version in mermaid for version in versions), "Human graph missing version")
    graph_hash = sha256(root / "graphify/versions.json")
    receipts = {
        "schema_version": 1,
        "repository": REPO,
        "archive_branch": BRANCH,
        "source_commit": actual,
        "workflow": os.getenv("GITHUB_WORKFLOW", "unverified-local-workflow"),
        "event": os.getenv("GITHUB_EVENT_NAME", "unverified-event"),
        "workflow_run": (f"https://github.com/{REPO}/actions/runs/{os.getenv('GITHUB_RUN_ID')}" if os.getenv("GITHUB_RUN_ID") else None),
        "runner": os.getenv("RUNNER_KIND", "unverified"),
        "validation": "PASS",
        "version_folders": versions,
        "graph_sha256": graph_hash,
        "graph_nodes": len(nodes),
        "graph_links": len(edges),
        "graphify_mcp_verified": False,
        "chatgpt_project_installation_verified": False,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "receipt.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
    print("ARCHIVE_VALIDATION=PASS")
    print("EXACT_SHA=" + actual)
    print("GRAPH_SHA256=" + graph_hash)
    print(json.dumps(receipts, indent=2))

if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as err:
        print("ARCHIVE_VALIDATION=FAIL: " + str(err), file=sys.stderr)
        sys.exit(1)
