"""Validate versioned instructions and record the actual GitHub Actions checkout."""

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO = "vixttha/Blender-Agent"
ARCHIVE = "chatgpt-project-instructions"
HISTORY = "33513f6e0e1f8bfe8acb7972066ef194219eb98c"
VERSION = re.compile(r"v\d+\.\d+\.\d+")
SHA = re.compile(r"[0-9a-f]{40}")
DOCUMENTS = ("README.md", "CHATGPT_PROJECT_INSTRUCTIONS.md", "ACCEPTANCE.md", "VERIFICATION.md")
STAGES = (
    ("head.*select one feature", ("acceptance criteria", "scope", "one active worker")),
    ("worker.*implement", ("reuse", "architecture", "tests")),
    ("validate.*public github runners", ("github-hosted", "tested sha", "head", "base")),
    ("internal auditor.*verify findings", ("demonstrated gaps", "repair")),
    ("head.*merge approval and archive", ("authorization", "integrate once", "merged sha")),
)
POLICIES = (
    "https://github.com/" + REPO,
    "https://github.com/" + REPO + "/tree/graphify-hq",
    "archivewright", "solo", "public", "creator-identifying", "credentials",
    "$0", "local ci", "self-hosted", "$graphify", "graph checksum",
    "gpt-6.1-sol", "medium", "meta-prompts", "feature freezes",
    "active pr", "blender smoke", "pending", "summary",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def validate_instructions(doc):
    normalized = doc.casefold()
    for token in POLICIES:
        require(token in normalized, f"Missing instruction policy: {token}")
    stages = list(re.finditer(r"(?m)^\s*\d+\.\s+\*\*([^*\n]+)\*\*", normalized))
    require(len(stages) == len(STAGES), "Expected five delivery stages")
    for index, (heading, criteria) in enumerate(STAGES):
        stage = stages[index]
        end = stages[index + 1].start() if index + 1 < len(stages) else len(normalized)
        body = normalized[stage.end():end].split("\n## ", 1)[0]
        require(re.fullmatch(heading + r"\.?", stage[1]), f"Delivery stage out of order: {stage[1]}")
        for phrase in criteria:
            require(phrase in body, f"Missing {phrase} in {stage[1]}")


def provenance(tested, event_name, event, parents):
    require(SHA.fullmatch(tested), "Invalid tested SHA")
    result = {"tested_sha": tested, "checkout_kind": "branch_commit",
              "pr_head_sha": None, "pr_base_sha": None}
    if event_name == "pull_request":
        pr = event["pull_request"]
        head, base = pr["head"]["sha"], pr["base"]["sha"]
        require(SHA.fullmatch(head) and SHA.fullmatch(base), "Invalid PR head or base")
        require(parents == [base, head], "Tested merge commit does not match the PR base and head")
        result.update(checkout_kind="pr_merge_commit", pr_head_sha=head, pr_base_sha=base)
    else:
        require(event_name == "push" and event["after"] == tested, "Unexpected push revision or event")
    return result


def validate_catalog(root):
    manifest = json.loads((root / "graphify/versions.json").read_text())
    info, nodes, links = manifest["graph"], manifest["nodes"], manifest["links"]
    require(info["repository"] == REPO and info["archive_branch"] == ARCHIVE, "Wrong archive identity")
    require(info["mcp_verified"] is False, "Lineage manifest must describe its manual provenance")
    ids = {node["id"] for node in nodes}
    require(len(ids) == len(nodes), "Duplicate lineage IDs")
    require(all(edge["source"] in ids and edge["target"] in ids for edge in links), "Dangling lineage link")
    versions = {node["directory"]: node for node in nodes if node["kind"] == "instructions-version"}
    directories = {p.name for p in root.iterdir() if p.is_dir() and VERSION.fullmatch(p.name)}
    require(len(versions) == sum(n["kind"] == "instructions-version" for n in nodes), "Duplicate version directories")
    require(set(versions) == directories and info["active_version"] in versions, "Version catalog mismatch")
    readme = (root / "README.md").read_text()
    mermaid = (root / "graphify/versions.mmd").read_text()
    require(versions["v0.0.1"].get("frozen_at") == HISTORY, "Historical pin changed")
    for version, node in versions.items():
        require(node["id"] == f"version:{version}", f"Wrong node ID for {version}")
        status = node["status"]
        require(status in {"candidate", "accepted"}, f"Invalid status for {version}")
        require(f"| [{version}]({version}/) | {status.title()} |" in readme, f"README status differs for {version}")
        require(version in mermaid, f"Mermaid lineage lacks {version}")
        require({"source": f"branch:{ARCHIVE}", "target": node["id"], "relation": "contains"} in links,
                f"Lineage lacks branch link for {version}")
        for name in DOCUMENTS:
            require((root / version / name).is_file(), f"Missing {version}/{name}")
        frozen = node.get("frozen_at")
        require(status != "accepted" or frozen, f"Accepted version {version} needs a source pin")
        if frozen:
            require(SHA.fullmatch(frozen), f"Invalid source pin for {version}")
            original = git(root, "rev-parse", f"{frozen}:{version}")
            current = git(root, "rev-parse", f"HEAD:{version}")
            require(original == current, f"Frozen version {version} changed")
    return info["active_version"]


def validate_links(root, paths):
    for path in paths:
        body = path.read_text()
        for raw in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", body):
            url = urlsplit(raw)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            require(target.is_relative_to(root) and target.exists(), f"Broken archive link in {path.name}: {raw}")


def validate_snapshot(root, active, hq_revision):
    folder = root / "graphify" / "instructions" / active
    if not folder.exists():
        return
    receipt = json.loads((folder / "receipt.json").read_text())
    digest = hashlib.sha256((folder / "graph.json").read_bytes()).hexdigest()
    require(receipt["graph_sha256"] == digest, "Archived graph checksum differs")
    require(receipt["scope"] == "chatgpt_project_instructions" and receipt["version"] == active,
            "Archived graph scope differs")
    require(receipt["mcp_verified"] is True and receipt["graphify_hq_commit"] == hq_revision,
            "Archived graph provenance differs")
    source = receipt["source_commit"]
    require(SHA.fullmatch(source), "Archived graph source SHA is invalid")
    expected_docs = {f"{active}/{name}" for name in DOCUMENTS if name != "VERIFICATION.md"}
    require(set(receipt["documents"]) == expected_docs, "Archived graph source list differs")
    for path, item in receipt["documents"].items():
        blob = git(root, "rev-parse", f"{source}:{path}")
        current = git(root, "rev-parse", f"HEAD:{path}")
        require(item["blob_sha1"] == blob == current, f"Archived graph is stale for {path}")


def main():
    root = Path.cwd()
    expected = os.environ["GITHUB_SHA"]
    actual = git(root, "rev-parse", "HEAD")
    require(expected == actual, "Actual checkout differs from GitHub SHA")
    event = os.environ["GITHUB_EVENT_NAME"]
    payload = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    parents = re.findall(r"(?m)^parent ([0-9a-f]{40})$",
                         git(root, "cat-file", "-p", actual).split("\n\n", 1)[0])
    require(payload["repository"]["full_name"] == REPO, "Unexpected repository")
    runner = os.environ["RUNNER_KIND"]
    require(payload["repository"]["visibility"] == "public" and runner == "github-hosted",
            "Expected a public GitHub-hosted runner")
    receipt = provenance(actual, event, payload, parents)
    active = validate_catalog(root)
    validate_instructions((root / active / "CHATGPT_PROJECT_INSTRUCTIONS.md").read_text())
    validate_links(root, [root / "README.md", root / "graphify/README.md",
                          *(root / active / doc for doc in DOCUMENTS)])
    validate_snapshot(root, active, os.environ["GRAPHIFY_HQ_SHA"])
    require((root / "LICENSE").read_text().startswith("MIT License"), "Archive reuse terms missing")
    receipt.update(
        repository=REPO, version=active, event=event, runner=runner, validation="PASS",
        workflow_run=f"https://github.com/{REPO}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
        job=os.environ["GITHUB_JOB"],
        lineage_sha256=hashlib.sha256((root / "graphify/versions.json").read_bytes()).hexdigest(),
    )
    summary = json.dumps(receipt, indent=2)
    print("ARCHIVE_VALIDATION=PASS")
    print(summary)
    with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a") as output:
        output.write("## Archive validation\n\n" + chr(96) * 3 + "json\n" + summary + "\n" + chr(96) * 3 + "\n")


if __name__ == "__main__":
    main()
