"""Build an instructions graph with the pinned Graphify HQ implementation."""

import asyncio
import base64
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    root = Path.cwd()
    source = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    if source != os.environ["GITHUB_SHA"]:
        raise ValueError("Graph source differs from the workflow checkout")
    version = json.loads((root / "graphify/versions.json").read_text())["graph"]["active_version"]
    dependencies = Path(os.environ["GRAPHIFY_HQ_TOOLS"])
    sys.path.insert(0, str(dependencies))
    from version_maps import make_map, verify_mcp

    docs = {f"{version}/{name}": (root / version / name).read_bytes().decode("utf-8")
            for name in ("README.md", "CHATGPT_PROJECT_INSTRUCTIONS.md", "ACCEPTANCE.md")}
    output = Path(os.environ["RUNNER_TEMP"]) / "instructions-graph"
    receipt = make_map(version, source, docs, output, candidate=True)
    graph_path = output / "graph.json"
    graph = json.loads(graph_path.read_text())
    graph["scope"] = "chatgpt_project_instructions"
    graph.setdefault("graph", {})["scope"] = "chatgpt_project_instructions"
    for node in graph["nodes"]:
        if node["id"] == f"version:{version}":
            node["label"] = f"Blender-Agent project instructions {version}"
    graph["built_at_commit"] = source
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    asyncio.run(verify_mcp(graph_path, receipt))

    receipt.update(
        scope="chatgpt_project_instructions",
        source_ref=os.environ["GITHUB_REF"],
        graph_sha256=hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        graphify_hq_commit=os.environ["GRAPHIFY_HQ_SHA"],
        workflow_run=f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
        mcp_verified=True,
    )
    receipt_path = output / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print("GRAPHIFY_MCP_READBACK=PASS")
    with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a") as summary:
        summary.write("\n## Graphify MCP read-back\n\n" + chr(96) * 3 + "json\n" +
                      receipt_path.read_text() + chr(96) * 3 + "\n")
    print(receipt_path.read_text())
    if os.environ["GITHUB_EVENT_NAME"] == "push" and not (root / "graphify/instructions" / version).exists():
        for path in (graph_path, receipt_path):
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            for index in range(0, len(encoded), 1024):
                print(f"GRAPHIFY_EXPORT {path.name} {index // 1024:04d} {encoded[index:index + 1024]}")


if __name__ == "__main__":
    main()
