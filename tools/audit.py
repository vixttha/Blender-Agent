"""Inventory a pinned Git tree and check a Code Stack registry."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

SHA = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
LANGUAGES = {
    ".py": "Python", ".pyi": "Python", ".pyx": "Cython", ".js": "JavaScript",
    ".mjs": "JavaScript", ".cjs": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".mts": "TypeScript", ".cts": "TypeScript",
    ".tsx": "TypeScript", ".rs": "Rust", ".go": "Go", ".c": "C",
    ".cc": "C++", ".cpp": "C++", ".cxx": "C++", ".hpp": "C++",
    ".cs": "C#", ".fs": "F#", ".fsx": "F#", ".java": "Java", ".kt": "Kotlin",
    ".kts": "Kotlin", ".swift": "Swift", ".dart": "Dart", ".lua": "Lua",
    ".gd": "GDScript", ".zig": "Zig", ".nim": "Nim", ".d": "D",
    ".odin": "Odin", ".rb": "Ruby", ".php": "PHP", ".pl": "Perl",
    ".ex": "Elixir", ".exs": "Elixir", ".erl": "Erlang", ".hrl": "Erlang",
    ".hs": "Haskell", ".ml": "OCaml", ".mli": "OCaml", ".clj": "Clojure",
    ".cljs": "ClojureScript", ".scala": "Scala", ".jl": "Julia", ".r": "R",
    ".f": "Fortran", ".f90": "Fortran", ".sh": "Shell", ".bash": "Shell",
    ".zsh": "Shell", ".ps1": "PowerShell", ".psm1": "PowerShell",
    ".bat": "Batch", ".cmd": "Batch", ".sql": "SQL", ".s": "Assembly",
    ".asm": "Assembly", ".cu": "CUDA C++", ".wgsl": "WGSL",
    ".glsl": "GLSL", ".frag": "GLSL", ".vert": "GLSL", ".hlsl": "HLSL",
    ".metal": "Metal Shading Language", ".osl": "OSL",
    ".ispc": "ISPC", ".sol": "Solidity", ".v": "Verilog / V (review)",
    ".sv": "SystemVerilog", ".vhd": "VHDL", ".vb": "Visual Basic",
    ".hx": "Haxe", ".m": "Objective-C / MATLAB (review)",
    ".h": "C / C++ header (review)", ".mm": "Objective-C++",
}
FORMATS = {
    ".json": "JSON", ".jsonc": "JSON with comments", ".toml": "TOML",
    ".yaml": "YAML", ".yml": "YAML", ".xml": "XML", ".md": "Markdown",
    ".rst": "reStructuredText", ".adoc": "AsciiDoc", ".html": "HTML",
    ".htm": "HTML", ".css": "CSS", ".scss": "SCSS", ".svg": "SVG",
    ".vue": "Vue component", ".svelte": "Svelte component", ".ipynb": "Notebook",
    ".gradle": "Gradle script (review)", ".cmake": "CMake", ".tf": "HCL",
    ".proto": "Protocol Buffers", ".wit": "WebAssembly Interface Type",
}
SPECIAL = {
    "Dockerfile": "Dockerfile", "Containerfile": "Containerfile",
    "Makefile": "Make", "CMakeLists.txt": "CMake", ".gitignore": "Git configuration",
    ".gitattributes": "Git configuration", "LICENSE": "License text",
    "COPYING": "License text",
}
ASSETS = {
    ".blend", ".stl", ".obj", ".glb", ".gltf", ".fbx", ".png", ".jpg",
    ".jpeg", ".webp", ".gif", ".ico", ".pdf", ".zip", ".wasm", ".woff2",
}
STATES = {"active", "conditional", "research", "retired"}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def inventory(repo, revision, overrides):
    if not SHA.fullmatch(revision):
        raise ValueError("source commit must be a full Git object ID")
    if git(repo, "rev-parse", "HEAD").decode().strip() != revision:
        raise ValueError("checked-out HEAD differs from the requested source commit")
    if git(repo, "cat-file", "-t", revision).strip() != b"commit":
        raise ValueError("source object must be a commit")
    entries = {}
    raw = git(repo, "ls-tree", "-r", "-z", "--full-tree", revision)
    for item in raw.split(b"\0"):
        if item:
            metadata, path = item.split(b"\t", 1)
            mode, kind, _ = metadata.decode("ascii").split()
            entries[path.decode("utf-8", errors="surrogateescape")] = (mode, kind)
    if set(overrides) - entries.keys():
        raise ValueError("override names an untracked path")

    grouped = {"languages": {}, "formats": {}, "assets": [], "review_paths": []}
    for path, (mode, kind) in sorted(entries.items()):
        file = Path(path)
        suffix = file.suffix.lower()
        if mode == "120000" or kind != "blob":
            grouped["review_paths"].append(path)
        elif path in overrides or suffix in LANGUAGES:
            language = overrides[path] if path in overrides else LANGUAGES[suffix]
            if "(review)" in language:
                grouped["review_paths"].append(path)
            else:
                grouped["languages"].setdefault(language, []).append(path)
        elif file.name in SPECIAL or suffix in FORMATS:
            name = SPECIAL.get(file.name) or FORMATS[suffix]
            grouped["formats"].setdefault(name, []).append(path)
        elif suffix in ASSETS:
            grouped["assets"].append(path)
        else:
            grouped["review_paths"].append(path)
    return grouped, entries


def check_registry(config, repo, entries, grouped):
    if config["schema_version"] != 1:
        raise ValueError("unsupported schema version")
    if not config["project"].strip():
        raise ValueError("project name is required")
    revision = config["source_commit"]
    sources = config["sources"]
    ids = [row["id"] for row in sources]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate evidence ID")
    for row in sources:
        url = urlsplit(row["url"])
        if url.scheme != "https" or not url.netloc or url.username is not None:
            raise ValueError(f"evidence {row['id']} needs a public HTTPS URL")
        if not row["claim"].strip():
            raise ValueError(f"evidence {row['id']} needs a claim")
    technologies = config["technologies"]
    names = [row["name"] for row in technologies]
    if len(names) != len(set(names)):
        raise ValueError("duplicate technology name")
    for row in technologies:
        if row["status"] not in STATES:
            raise ValueError(f"invalid status for {row['name']}")
        if not row["role"].strip() or not row["evidence"] or set(row["evidence"]) - set(ids):
            raise ValueError(f"incomplete role or evidence for {row['name']}")

    missing = sorted(set(config["required_paths"]) - entries.keys())
    if missing:
        raise ValueError("missing required tracked paths: " + ", ".join(missing))
    active = {row["name"] for row in technologies if row["status"] == "active"}
    current = set(grouped["languages"])
    if current - active:
        raise ValueError("unregistered source languages: " + ", ".join(sorted(current - active)))
    if any(row["name"] not in current for row in technologies
           if row["status"] == "active" and row.get("tracked_language", False)):
        raise ValueError("a declared tracked language has no matching source file")
    unreviewed = sorted(set(grouped["review_paths"]) - set(config.get("reviewed_paths", [])))
    if unreviewed:
        raise ValueError("unreviewed tracked paths: " + ", ".join(unreviewed))
    for path, fragments in config.get("source_checks", {}).items():
        if entries.get(path, ("", ""))[0] not in {"100644", "100755"}:
            raise ValueError(f"source check needs a regular tracked file: {path}")
        body = git(repo, "show", f"{revision}:{path}").decode("utf-8")
        for fragment in fragments:
            if fragment not in body:
                raise ValueError(f"source check failed: {path} must contain {fragment!r}")


def run(repo, config):
    grouped, entries = inventory(repo, config["source_commit"], config.get("overrides", {}))
    check_registry(config, repo, entries, grouped)
    return {"project": config["project"], "source_commit": config["source_commit"],
            "tracked_entries": len(entries), **grouped}


def print_report(report, output):
    print(f"Code Stack audit for {report['project']}", file=output)
    print(f"Source commit: {report['source_commit']}", file=output)
    print(f"Tracked entries: {report['tracked_entries']}", file=output)
    counts = Counter({name: len(paths) for name, paths in report["languages"].items()})
    for name, count in sorted(counts.items()):
        print(f"- {name}: {count} tracked source files", file=output)
    print("Supporting formats: " + ", ".join(sorted(report["formats"])), file=output)
    print(f"Reviewed ambiguous or unclassified paths: {len(report['review_paths'])}", file=output)
    print("Result: PASS (inventory and evidence references)", file=output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="target checkout")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--config", type=Path, help="Code Stack registry JSON")
    mode.add_argument("--discover", metavar="COMMIT", help="inventory a full Git commit before registration")
    parser.add_argument("--json", type=Path, help="write a complete machine-readable report")
    parser.add_argument("--summary", type=Path, help="append a short report to the job summary")
    args = parser.parse_args()
    try:
        if args.discover:
            grouped, entries = inventory(args.repo, args.discover, {})
            report = {"source_commit": args.discover, "tracked_entries": len(entries), **grouped}
            result = json.dumps(report, indent=2, sort_keys=True) + "\n"
            if args.json:
                args.json.write_text(result, encoding="utf-8")
            else:
                sys.stdout.write(result)
            return
        config = json.loads(args.config.read_text(encoding="utf-8"))
        report = run(args.repo, config)
        if args.json:
            args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")
        if args.summary:
            with args.summary.open("a", encoding="utf-8") as output:
                print_report(report, output)
        print_report(report, sys.stdout)
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Code Stack audit failed: {error}\n")


if __name__ == "__main__":
    main()
