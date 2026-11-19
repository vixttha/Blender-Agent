"""Build and verify immutable Code Stack template maps with Graphify MCP."""

from __future__ import annotations

import ast
import asyncio
import hashlib
import json
import re
import sys
import tempfile
from importlib.metadata import version as package_version
from pathlib import Path, PurePosixPath
from subprocess import check_output

from graphify.build import build_from_json
from graphify.export import to_json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Shared Markdown parsing from the pinned Graphify HQ checkout in CI.
from version_maps import HEADING, LINK, prose_lines, reference_path, semver

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "graphify"
REPO = "vixttha/Blender-Agent"
SHA = re.compile(r"[0-9a-f]{40}")
MAX_FILES = 64
MAX_BYTES = 1_000_000


def git(*args):
    return check_output(["git", "-C", str(ROOT), *args])


def load_catalog():
    catalog = json.loads((ARCHIVE / "catalog.json").read_text(encoding="utf-8"))
    if catalog["schema_version"] != 1 or catalog["repository"] != REPO:
        raise ValueError("Incorrect Code Stack graph catalog")
    records = catalog["versions"]
    names = [entry["version"] for entry in records]
    if not names or names != sorted(set(names), key=semver):
        raise ValueError("Expected unique ascending template versions")
    root_entries = git("ls-tree", "--name-only", "-z", "HEAD").decode().split("\0")
    folders = {name for name in root_entries if re.fullmatch(r"v\d+\.\d+\.\d+", name)}
    if folders != set(names):
        raise ValueError("Version folders and graph catalog differ")
    for item in records:
        if not SHA.fullmatch(item["source_commit"]):
            raise ValueError("Version must pin a full Git source commit")
    return records


def version_files(revision, name):
    records = git("ls-tree", "-r", "-l", "-z", revision, "--", name + "/").decode().split("\0")
    files = {}
    for item in filter(None, records):
        metadata, path = item.split("\t", 1)
        mode, kind, oid, size = metadata.split()
        if kind != "blob" or mode not in {"100644", "100755"} or int(size) > MAX_BYTES:
            raise ValueError(f"Unsupported source entry: {path}")
        files[path] = (mode, oid)
    if not 1 <= len(files) <= MAX_FILES:
        raise ValueError(f"Missing or oversized template folder: {name}")
    return files


def verify_archived_files(revision, name, archive="HEAD"):
    files = version_files(revision, name)
    if files != version_files(archive, name):
        raise ValueError(f"{name} tracked paths, blobs, or modes differ from the pinned template version")
    return files


def build_graph(name, revision, files, output):
    nodes, edges = {}, {}
    probes = {}

    def node(identity, label, kind, path=None, line=None):
        nodes[identity] = {"id": identity, "label": label, "file_type": kind,
                           "source_file": path, "source_location": f"L{line}" if line else None}
        return identity

    def edge(start, end, relation, path, line=1):
        edges[(start, end, relation)] = {
            "source": start, "target": end, "relation": relation,
            "source_file": path, "source_location": f"L{line}", "confidence": "EXTRACTED",
            "confidence_score": 1.0, "weight": 1.0,
        }

    def file_id(path):
        return "document:" + path if path.endswith(".md") else "file:" + path

    def python_structure(path, body, owner):
        def definitions(parent, statements, prefix=""):
            for entry in statements:
                if not isinstance(entry, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                qualified = prefix + entry.name
                symbol = node(f"symbol:{path}:{qualified}", qualified, "code", path, entry.lineno)
                edge(parent, symbol, "defines", path, entry.lineno)
                probes.setdefault(path + ":symbol", (symbol, path, entry.lineno))
                if isinstance(entry, ast.ClassDef):
                    definitions(symbol, entry.body, qualified + ".")

        tree = ast.parse(body, filename=path)
        definitions(owner, tree.body)
        for entry in ast.walk(tree):
            if isinstance(entry, ast.Import):
                imports = [alias.name for alias in entry.names]
            elif isinstance(entry, ast.ImportFrom) and entry.module:
                imports = [entry.module]
            else:
                continue
            for imported in imports:
                local = (PurePosixPath(path).parent / (imported.replace(".", "/") + ".py")).as_posix()
                target = file_id(local) if local in files else node("module:" + imported, imported, "concept")
                edge(owner, target, "imports", path, entry.lineno)

    root = node("version:" + name, "Code Stack Template " + name, "concept")
    for path in sorted(files):
        document = path.endswith(".md")
        code = path.endswith(".py")
        identity = node(file_id(path), path, "document" if document else "code" if code else "concept",
                        path, 1)
        probes[path] = (identity, path, 1)
        edge(root, identity, "contains_file", path)
        if not (document or code):
            continue
        body = git("show", revision + ":" + path).decode("utf-8")
        if code:
            python_structure(path, body, identity)
            continue
        for line_no, line in prose_lines(body):
            heading = HEADING.match(line)
            if heading:
                section = node(f"heading:{path}:L{line_no}", heading.group(2), "concept", path, line_no)
                edge(identity, section, "contains_heading", path, line_no)
            for raw in LINK.findall(line):
                dest = reference_path(path, raw)
                if dest in files and dest != path:
                    edge(identity, file_id(dest), "links_to", path, line_no)

    if not any(key.startswith("symbol:") for key in nodes):
        raise ValueError(f"No Python symbols in {name} template map")
    graph = build_from_json({"nodes": [nodes[key] for key in sorted(nodes)],
                             "edges": [edges[key] for key in sorted(edges)]},
                            directed=True, dedup=False)
    graph.graph.update(template_version=name, scope="code_stack_template")
    output.mkdir(parents=True)
    graph_path = output / "graph.json"
    to_json(graph, {0: sorted(graph)}, str(graph_path), built_at_commit="")
    receipt = {
        "schema_version": 1,
        "version": name,
        "scope": "code_stack_template",
        "source_repository": REPO,
        "source_commit": revision,
        "graphify_version": package_version("graphifyy"),
        "graph_sha256": hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "source_blobs": {path: oid for path, (_, oid) in sorted(files.items())},
    }
    asyncio.run(verify_mcp(graph_path, receipt, probes.values()))
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


async def verify_mcp(graph_path, receipt, probes):
    server = StdioServerParameters(command=sys.executable,
                                   args=["-m", "graphify.serve", str(graph_path)])
    async with asyncio.timeout(30), stdio_client(server) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("graph_stats", {})
            stats = "\n".join(item.text for item in result.content if item.type == "text")
            expected = {f"Nodes: {receipt['nodes']}", f"Edges: {receipt['edges']}"}
            if result.is_error or not expected <= set(stats.splitlines()):
                raise ValueError("Graphify MCP did not report the generated graph counts")
            for identity, path, line in probes:
                result = await session.call_tool("get_node", {"node_id": identity})
                response = "\n".join(item.text for item in result.content if item.type == "text")
                if result.is_error or f"Source: {path} L{line}" not in response:
                    raise ValueError(f"Graphify MCP read-back failed for {identity}")
    print(f"{receipt['version']}: Graphify MCP PASS "
          f"({receipt['nodes']} nodes, {receipt['edges']} edges, {len(receipt['source_blobs'])} files)"
          f" source {receipt['source_commit']}", flush=True)


def emit(path, data):
    value = data.decode("utf-8")
    chunks = [value[i:i + 1500] for i in range(0, len(value), 1500)]
    for index, chunk in enumerate(chunks):
        print("CODE_STACK_GRAPH_EXPORT " + json.dumps({
            "path": path, "index": index, "total": len(chunks), "chunk": chunk,
        }, ensure_ascii=True))


def main():
    with tempfile.TemporaryDirectory() as directory:
        generated = Path(directory)
        differences = []
        for record in load_catalog():
            name, revision = record["version"], record["source_commit"]
            files = verify_archived_files(revision, name)
            build_graph(name, revision, files, generated / name)
            for filename in ("graph.json", "receipt.json"):
                path = f"{name}/{filename}"
                data = (generated / path).read_bytes()
                archived = ARCHIVE / path
                if not archived.is_file() or archived.read_bytes() != data:
                    differences.append(path)
                    emit(path, data)
        if differences:
            raise SystemExit("Commit verified graph output and re-run: " + ", ".join(differences))
        print("All Code Stack template maps match their deterministic rebuild.")


if __name__ == "__main__":
    main()
