"""Generate deterministic, read-only Graphify version maps for Blender-Agent Refinement Toolkit."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import posixpath
import re
import subprocess
import sys
import tempfile
from importlib.metadata import version as package_version
from pathlib import Path
from urllib.parse import unquote, urlsplit

from graphify.build import build_from_json
from graphify.export import to_json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog" / "versions.json"
ARCHIVES = ROOT / "versions"
REPOSITORY = "vixttha/Blender-Agent-Refinement-Toolkit"
PRODUCT_NAME = "Blender-Agent Refinement Toolkit"
LEGACY_REPOSITORY = "vixttha/Blender-Agent"
LEGACY_PRODUCT_NAME = "Blender-Agent"
# Exact pre-rebrand source commits whose generated artifacts remain byte-for-byte reproducible.
LEGACY_SNAPSHOTS = {
    ("v0.0.1", "45726472fbe7f32de32f87426dc0b21b8fc1e8f7", True),
    ("v0.0.2", "cb945bd8531ee425615c1968612ab6503849369d", False),
    ("v0.0.3", "38e8f63c3fe2e372784276acdbb602cb7409b100", True),
    ("v0.0.3", "7febadd1d18bd15967e9eed6223098268dadfe2f", False),
}
RELEASE = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)\Z")
COMMIT = re.compile(r"[0-9a-f]{40}\Z")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#+)?\s*$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MAX_DOCUMENTS = 64
MAX_SOURCE_BYTES = 1_000_000


def git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return result.stdout


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def semver(tag: str) -> tuple[int, int, int]:
    match = RELEASE.fullmatch(tag)
    if match is None:
        raise ValueError("Invalid release version: " + tag)
    return tuple(map(int, match.groups()))


def check_path(path: str) -> None:
    if not isinstance(path, str) or not path or len(path) > 240:
        raise ValueError("Invalid source path")
    if (
        path.startswith(("/", "./")) or "\\" in path or "//" in path
        or any(part in ("", ".", "..") for part in path.split("/"))
        or not path.endswith(".md")
        or path.startswith(".github/")
        or path in ("SECURITY.md",)
    ):
        raise ValueError("Unsafe or non-Markdown source path: " + path)


def validate_catalog(catalog: object) -> list[dict]:
    if not isinstance(catalog, dict) or set(catalog) != {"schema_version", "repository", "versions"}:
        raise ValueError("Catalog keys differ from the required schema")
    if catalog["schema_version"] != 1 or catalog["repository"] != REPOSITORY:
        raise ValueError("Incorrect catalog version or repository")
    records = catalog["versions"]
    if not isinstance(records, list):
        raise ValueError("Catalog versions must be a list")
    previous = None
    for item in records:
        if not isinstance(item, dict) or set(item) != {"version", "source_commit", "release_tag", "source_files"}:
            raise ValueError("Unexpected version record fields")
        name, sha, tag, paths = (item[k] for k in ("version", "source_commit", "release_tag", "source_files"))
        if not isinstance(name, str) or not isinstance(tag, str):
            raise ValueError("Version and tag must be strings")
        order = semver(name)
        if previous is not None and previous >= order:
            raise ValueError("Versions must be unique and strictly ascending")
        previous = order
        if tag != name or not isinstance(sha, str) or not COMMIT.fullmatch(sha):
            raise ValueError("Release tag and full source commit must match the record")
        if not isinstance(paths, list) or not 1 <= len(paths) <= MAX_DOCUMENTS:
            raise ValueError("Source files must be a bounded non-empty list")
        if len(set(map(str, paths))) != len(paths):
            raise ValueError("Duplicate source paths")
        for path in paths:
            check_path(path)
        if paths != sorted(paths):
            raise ValueError("Source paths must be lexicographically sorted")
    return records


def read_sources(item: dict) -> dict[str, str]:
    sha = item["source_commit"]
    try:
        resolved = git("rev-parse", "--verify", item["release_tag"] + "^{commit}").decode().strip()
        if resolved != sha:
            raise ValueError("Release tag is not pinned to the declared source SHA")
        if git("cat-file", "-t", sha).decode().strip() != "commit":
            raise ValueError("Source SHA does not identify a commit")
    except subprocess.CalledProcessError as exc:
        raise ValueError("Missing source commit or matching release tag") from exc
    docs = {}
    for path in item["source_files"]:
        try:
            data = git("show", sha + ":" + path)
        except subprocess.CalledProcessError as exc:
            raise ValueError("Document missing from source commit: " + path) from exc
        if not 0 < len(data) <= MAX_SOURCE_BYTES:
            raise ValueError("Source document exceeds size bounds: " + path)
        docs[path] = data.decode("utf-8")
    return docs


def reference_path(source: str, raw: str) -> str | None:
    target = urlsplit(raw.strip().split(" ", 1)[0].strip("<>"))
    if target.scheme or target.netloc or not target.path:
        return None
    candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(target.path)))
    if candidate.startswith("../") or candidate.startswith("/") or candidate == "..":
        return None
    return candidate


def prose_lines(body: str):
    """Yield Markdown lines outside fenced code blocks, retaining source line numbers."""
    fence = None
    for line_number, line in enumerate(body.splitlines(), 1):
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        if indent <= 3 and stripped[:1] in ("`", "~"):
            marker = stripped[0]
            marker_length = len(stripped) - len(stripped.lstrip(marker))
            if marker_length >= 3:
                if fence is None:
                    fence = (marker, marker_length)
                    continue
                if fence[0] == marker and marker_length >= fence[1] and not stripped[marker_length:].strip():
                    fence = None
                    continue
        if fence is None:
            yield line_number, line

def make_map(tag: str, sha: str, docs: dict[str, str], folder: Path, fixture: bool = False, candidate: bool = False) -> dict:
    repository, product_name = REPOSITORY, PRODUCT_NAME
    if (tag, sha, candidate) in LEGACY_SNAPSHOTS:
        repository, product_name = LEGACY_REPOSITORY, LEGACY_PRODUCT_NAME
    nodes: dict[str, dict] = {}
    edges: dict[tuple, dict] = {}
    outlines: dict[str, list[tuple[str, str]]] = {}

    def add_node(identity: str, label: str, kind: str, path: str = "", line: int | None = None) -> None:
        nodes[identity] = {
            "id": identity, "label": label, "file_type": kind,
            "source_file": path, "source_location": f"L{line}" if line else None,
        }

    def add_edge(start: str, end: str, relation: str, path: str, line: int | None = None) -> None:
        edges[(start, end, relation)] = {
            "source": start, "target": end, "relation": relation,
            "source_file": path, "source_location": f"L{line}" if line else None,
            "confidence": "EXTRACTED", "confidence_score": 1.0, "weight": 1.0,
        }

    add_node("version:" + tag, product_name + " " + tag, "concept")
    for path, body in sorted(docs.items()):
        doc_id = "document:" + path
        add_node(doc_id, path, "document", path, 1)
        add_edge("version:" + tag, doc_id, "contains_document", path, 1)
        stack: list[tuple[int, str]] = []
        outline: list[tuple[str, str]] = []
        slug_counts: dict[str, int] = {}
        visible_lines = list(prose_lines(body))
        for line_no, line in visible_lines:
            match = HEADING.match(line)
            if not match:
                continue
            depth, heading = len(match.group(1)), match.group(2).strip()
            key = f"section:{path}:L{line_no}"
            add_node(key, heading, "concept", path, line_no)
            while stack and stack[-1][0] >= depth:
                stack.pop()
            add_edge(stack[-1][1] if stack else doc_id, key, "contains_section", path, line_no)
            stack.append((depth, key))
            slug = re.sub(r"[^\w\- ]", "", heading.lower()).strip().replace(" ", "-")
            index = slug_counts.get(slug, 0)
            slug_counts[slug] = index + 1
            outline.append((heading, slug + (f"-{index}" if index else "")))
        outlines[path] = outline
        for raw in LINK.findall("\n".join(line for _, line in visible_lines)):
            dest = reference_path(path, raw)
            if dest is None or dest == path:
                continue
            if dest in docs:
                target_id = "document:" + dest
            else:
                target_id = "reference:" + dest
                add_node(target_id, dest, "concept")
            add_edge(doc_id, target_id, "links_to", path)

    graph = build_from_json(
        {"nodes": list(nodes.values()), "edges": list(edges.values())},
        directed=True, dedup=False,
    )
    graph.graph.update(template_version=tag, scope="blender_agent_release_candidate" if candidate else "blender_agent_release")
    folder.mkdir(parents=True, exist_ok=True)
    graph_path = folder / "graph.json"
    to_json(graph, {0: list(graph)}, str(graph_path), built_at_commit="")
    receipt = {
        "schema_version": 1,
        "version": tag,
        "release_tag": tag if not (fixture or candidate) else None,
        "source_repository": repository,
        "source_commit": sha,
        "graphify_version": package_version("graphifyy"),
        "graph_sha256": hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "documents": {
            path: {"source_commit": sha, "source_path": path, "blob_sha1": blob_sha1(body.encode("utf-8"))}
            for path, body in sorted(docs.items())
        },
        "synthetic_fixture": fixture,
        "archive_status": "candidate" if candidate else "fixture" if fixture else "approved",
    }
    (folder / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# " + product_name + " " + tag, "",
        "[Graphify map](graph.json) · [Source receipt](receipt.json) · [All versions](../README.md)", "",
        "**Source commit:** " + sha, "",
    ]
    if candidate:
        lines.extend([
            f"**Candidate only — NOT an approved or published {product_name} release.**", "",
            "Approval, an immutable release tag, and promotion into the approved catalog are pending.", "",
        ])
    for path, headings in outlines.items():
        lines.extend(["## " + path, "", "Source document at the pinned release commit:", ""])
        lines.append(
            "https://github.com/" + repository + "/blob/" + sha + "/" + path
        )
        lines.append("")
        for label, slug in headings:
            lines.append("- [" + label.replace("[", "\\[").replace("]", "\\]") + "](" +
                         "https://github.com/" + repository + "/blob/" + sha + "/" + path + "#" + slug + ")")
        lines.append("")
    (folder / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return receipt


async def verify_mcp(graph_file: Path, receipt: dict) -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "graphify.serve", str(graph_file)],
    )
    async with asyncio.timeout(30), stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("graph_stats", {})
            stats = "\n".join(item.text for item in result.content if item.type == "text")
            if result.is_error or not {
                f"Nodes: {receipt['nodes']}", f"Edges: {receipt['edges']}"
            } <= set(stats.splitlines()):
                raise ValueError("Graphify MCP statistics mismatch: " + stats[:500])
            for path in receipt["documents"]:
                result = await session.call_tool("get_node", {"node_id": "document:" + path})
                response = "\n".join(item.text for item in result.content if item.type == "text")
                if result.is_error or ("Source: " + path + " L1") not in response:
                    raise ValueError("Graphify MCP document lookup failed: " + path)


def write_index(records: list[dict], output: Path) -> None:
    lines = [f"# {PRODUCT_NAME} version graphs", ""]
    if not records:
        lines.append(f"No approved {PRODUCT_NAME} release snapshots have been registered yet.")
        lines.append("")
        lines.extend([
            "Each accepted version receives a folder named vMAJOR.MINOR.PATCH containing:",
            "",
            "- README.md — a browsable outline linked to the original public source documents.",
            "- graph.json — deterministic Graphify graph of that version's documentation.",
            "- receipt.json — exact source commit, release tag, source-file SHA-1 values, graph SHA-256, Graphify version, and node/edge counts.",
            "",
            "Version folders are created from the approved immutable catalog. See [Graphify guide](../tools/graphify/README.md) and [catalog](../catalog/versions.json).",
        ])
    else:
        lines.extend([
            f"Maps index public documentation at the exact source commit of each approved {PRODUCT_NAME} version.",
            "Each map includes a Graphify graph, navigable outline, and verification receipt.",
            "",
        ])
        for record in reversed(records):
            tag = record["version"]
            lines.append("- [" + tag + "](" + tag + "/README.md) — " + record["source_commit"])
        lines.extend(["", "[Catalog](../catalog/versions.json) · [Generation guide](../tools/graphify/README.md)"])
    (output / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def generated_files(output: Path) -> dict[str, bytes]:
    return {
        p.relative_to(output).as_posix(): p.read_bytes()
        for p in output.rglob("*") if p.is_file()
    }


def compare(output: Path) -> None:
    expected = generated_files(output)
    actual = generated_files(ARCHIVES)
    changed = sorted(set(expected) & set(actual) - {
        path for path in set(expected) & set(actual) if expected[path] == actual[path]
    })
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    for name, paths in (("Changed", changed), ("Missing", missing), ("Unexpected", extra)):
        for path in paths:
            print(name + ": versions/" + path)
    if changed or missing or extra:
        raise ValueError("Committed version graphs differ from deterministic rebuild")


def self_test() -> None:
    raw = (ROOT / "tests" / "fixtures" / "sample.md").read_text(encoding="utf-8")
    example = {"schema_version": 1, "repository": REPOSITORY, "versions": []}
    assert validate_catalog(example) == []
    bad = json.loads(json.dumps(example))
    bad["versions"] = [{
        "version": "v1.0.0", "release_tag": "v1.0.0",
        "source_commit": "a" * 40, "source_files": ["../secret.md"],
    }]
    try:
        validate_catalog(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("Traversal path must be rejected")
    with tempfile.TemporaryDirectory() as temp:
        first = Path(temp) / "first"
        second = Path(temp) / "second"
        receipt = make_map("v0.0.0", "0" * 40, {"README.md": raw}, first, fixture=True)
        again = make_map("v0.0.0", "0" * 40, {"README.md": raw}, second, fixture=True)
        assert receipt["source_repository"] == REPOSITORY
        assert (first / "README.md").read_text(encoding="utf-8").startswith(f"# {PRODUCT_NAME} ")
        if receipt['nodes'] != 6 or receipt['edges'] != 5:
            raise ValueError('Code-fence injection polluted the synthetic heading/link graph')
        if generated_files(first) != generated_files(second) or receipt != again:
            raise ValueError("Graphify fixture is not byte-for-byte deterministic")
        asyncio.run(verify_mcp(first / "graph.json", receipt))
        print("Graphify MCP synthetic fixture PASS (" +
              str(receipt["nodes"]) + " nodes, " + str(receipt["edges"]) + " edges)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    choices = parser.add_mutually_exclusive_group(required=True)
    choices.add_argument("--check", action="store_true", help="Rebuild and compare frozen archives")
    choices.add_argument("--generate", action="store_true", help="Generate reviewed catalog version maps")
    choices.add_argument("--self-test", action="store_true", help="Verify a synthetic fixture with Graphify MCP")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    records = validate_catalog(json.loads(CATALOG.read_text(encoding="utf-8")))
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "versions"
        output.mkdir()
        write_index(records, output)
        for record in records:
            name = record["version"]
            receipt = make_map(name, record["source_commit"], read_sources(record), output / name)
            asyncio.run(verify_mcp(output / name / "graph.json", receipt))
            print(name + ": read-only Graphify MCP verification PASS")
        if args.check:
            compare(output)
            print("Graphify HQ deterministic archive check PASS")
        else:
            for path, data in generated_files(output).items():
                target = ARCHIVES / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            print("Generated " + str(len(records)) + " approved version map(s) for review")


if __name__ == "__main__":
    main()
