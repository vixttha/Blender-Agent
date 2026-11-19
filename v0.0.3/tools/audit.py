"""Inventory a pinned Git tree, validate its registry and report source freshness."""

import argparse
from datetime import date
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
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
KINDS = {"repo-file", "ci-run", "upstream"}
BASES = {"language", "format", "source", "proposal"}
EMBEDDED = {".vue", ".svelte", ".ipynb", ".gradle"}
VENDORED = {"vendor", "vendored", "third_party", "node_modules"}
GENERATED = {"generated", "__generated__", "dist"}
DOC_PATHS = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md"}
SHEBANGS = {
    "python": "Python", "python3": "Python", "bash": "Shell", "sh": "Shell",
    "zsh": "Shell", "dash": "Shell", "node": "JavaScript", "ruby": "Ruby",
    "perl": "Perl", "php": "PHP", "pwsh": "PowerShell",
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def text_field(value, field):
    if not isinstance(value, str) or not value.strip() or value.strip() != value:
        raise ValueError(f"{field} must be a nonblank string without surrounding whitespace")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{field} must not include control characters")
    return value


def object_field(value, field):
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def list_field(value, field):
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    return value


def text_list(value, field):
    return [text_field(item, f"{field}[{index}]")
            for index, item in enumerate(list_field(value, field))]


def revision_field(value, field):
    if not OID.fullmatch(text_field(value, field)):
        raise ValueError(f"{field} must be a full Git object ID")
    return value


def path_entries(config, key):
    records = object_field(config.get(key, {}), key)
    for path, record in records.items():
        text_field(path, key)
        yield path, record


def validate_config(config):
    config = object_field(config, "registry")
    if type(config.get("schema_version")) is not int or config["schema_version"] != 2:
        raise ValueError("schema_version must be 2; see MIGRATION.md for a v0.0.1 registry")
    text_field(config.get("project"), "project")
    revision = revision_field(config.get("source_commit"), "source_commit")
    source_repository = config.get("source_repository")
    if source_repository is not None:
        value = text_field(source_repository, "source_repository")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
            raise ValueError("source_repository must have the owner/repository form")
    for field in ("source_ref", "source_state"):
        if field in config:
            text_field(config[field], field)
    if "template_commit" in config:
        revision_field(config["template_commit"], "template_commit")
    for key in ("required_paths", "docs_only_paths"):
        text_list(config.get(key, []), key)
    for path, reason in path_entries(config, "reviewed_paths"):
        text_field(reason, f"reviewed_paths[{path}]")
    for path, rule in path_entries(config, "overrides"):
        rule = object_field(rule, f"overrides[{path}]")
        label = f"overrides[{path}]"
        kind = text_field(rule.get("kind"), label + ".kind")
        if kind not in {"language", "format", "generated", "vendored"}:
            raise ValueError(f"{label}.kind is unsupported")
        if kind in {"language", "format"}:
            text_field(rule.get("name"), label + ".name")
        elif "name" in rule:
            raise ValueError(f"{label}.name is only allowed for language and format overrides")
        text_field(rule.get("reason"), label + ".reason")
    for path, fragments in path_entries(config, "source_checks"):
        if not text_list(fragments, f"source_checks[{path}]"):
            raise ValueError(f"source_checks[{path}] needs at least one fragment")

    sources = {}
    for index, row in enumerate(list_field(config.get("sources"), "sources")):
        label = f"sources[{index}]"
        row = object_field(row, label)
        source_id = text_field(row.get("id"), label + ".id")
        if source_id in sources:
            raise ValueError(f"duplicate evidence ID: {source_id}")
        kind = text_field(row.get("kind"), label + ".kind")
        if kind not in KINDS:
            raise ValueError(f"{label}.kind is unsupported")
        raw_url = text_field(row.get("url"), label + ".url")
        url = urlsplit(raw_url)
        if (url.scheme != "https" or not url.hostname or url.username is not None
                or any(char.isspace() for char in raw_url)):
            raise ValueError(f"{label}.url must be an HTTPS reference without credentials")
        text_field(row.get("claim"), label + ".claim")
        review = text_field(row.get("review"), label + ".review")
        if review not in {"reviewed", "unchecked"}:
            raise ValueError(f"{label}.review must be reviewed or unchecked")
        if review == "reviewed":
            date.fromisoformat(text_field(row.get("reviewed_on"), label + ".reviewed_on"))
        if kind in {"repo-file", "ci-run"}:
            published_commit = revision_field(row.get("commit"), label + ".commit")
            if kind == "repo-file":
                if published_commit != revision:
                    raise ValueError(f"{label}.commit must match the audited source commit")
                path = text_field(row.get("path"), label + ".path")
                if source_repository and url.hostname == "github.com":
                    expected = f"/{source_repository}/blob/{revision}/{path}"
                    if unquote(url.path) != expected:
                        raise ValueError(f"{label}.url must identify the declared GitHub repository, commit and path")
        sources[source_id] = row

    names = set()
    for index, row in enumerate(list_field(config.get("technologies"), "technologies")):
        label = f"technologies[{index}]"
        row = object_field(row, label)
        name = text_field(row.get("name"), label + ".name")
        if name in names:
            raise ValueError(f"duplicate technology name: {name}")
        names.add(name)
        state = text_field(row.get("status"), label + ".status")
        basis = text_field(row.get("basis"), label + ".basis")
        if state not in STATES or basis not in BASES or (state == "active" and basis == "proposal"):
            raise ValueError(f"{label} has an invalid status or evidence basis")
        text_field(row.get("role"), label + ".role")
        refs = text_list(row.get("evidence"), label + ".evidence")
        if not refs or set(refs) - sources.keys():
            raise ValueError(f"{label}.evidence must reference known evidence IDs")
        if state == "active" and basis == "source":
            if not any(sources[ref]["kind"] == "repo-file" for ref in refs):
                raise ValueError(f"{label} needs repository-file evidence for its source basis")
    return sources


def decode_paths(raw):
    return [item.decode("utf-8", errors="surrogateescape")
            for item in raw.split(b"\0") if item]


def shebang_language(repo, blob_sha):
    # Read small candidate blobs only. Content is never executed.
    if int(git(repo, "cat-file", "-s", blob_sha)) > 1024 * 1024:
        return None
    line = git(repo, "cat-file", "blob", blob_sha).split(b"\n", 1)[0]
    if not line.startswith(b"#!") or b"\0" in line or len(line) > 256:
        return None
    args = line[2:].decode("ascii", errors="replace").split()
    if not args:
        return None
    executable = PurePosixPath(args[0]).name
    if executable == "env":
        args = args[1:]
        if args[:1] == ["-S"]:
            args = args[1:]
        executable = args[0] if args else ""
    if re.fullmatch(r"python3\.[0-9]+", executable):
        return "Python"
    return SHEBANGS.get(executable)


def classify(repo, path, entry, override):
    mode, kind, blob_sha = entry
    if kind != "blob" or mode == "120000":
        return "review_paths", None
    if override:
        group = {"language": "languages", "format": "formats",
                 "generated": "generated", "vendored": "vendored"}[override["kind"]]
        return group, override.get("name")
    file = PurePosixPath(path)
    parents = set(file.parts[:-1])
    if parents & VENDORED:
        return "vendored", None
    if parents & GENERATED:
        return "generated", None
    suffix = file.suffix.lower()
    if suffix in EMBEDDED or file.name.lower().endswith(".gradle.kts"):
        return "review_paths", None
    if suffix in LANGUAGES:
        name = LANGUAGES[suffix]
        return ("review_paths", None) if "(review)" in name else ("languages", name)
    if file.name in SPECIAL or suffix in FORMATS:
        return "formats", SPECIAL.get(file.name) or FORMATS[suffix]
    if suffix in ASSETS:
        return "assets", None
    if not suffix and mode == "100755":
        name = shebang_language(repo, blob_sha)
        if name:
            return "languages", name
    return "review_paths", None


def inventory(repo, revision, overrides, *, require_checkout=True):
    revision_field(revision, "source_commit")
    if require_checkout and git(repo, "rev-parse", "HEAD").decode().strip() != revision:
        raise ValueError("checked-out HEAD differs from the requested source commit")
    if git(repo, "cat-file", "-t", revision).strip() != b"commit":
        raise ValueError("source object must be a commit")
    raw = git(repo, "ls-tree", "-r", "-z", "--full-tree", revision)
    entries = {}
    for item in decode_paths(raw):
        metadata, path = item.split("\t", 1)
        entries[path] = tuple(metadata.split())
    for path in overrides:
        if path not in entries or entries[path][0] not in {"100644", "100755"}:
            raise ValueError(f"override needs a regular tracked file: {path}")

    groups = {"languages": {}, "formats": {}, "assets": [], "review_paths": [],
              "generated": [], "vendored": []}
    for path, entry in sorted(entries.items()):
        group, name = classify(repo, path, entry, overrides.get(path))
        if name:
            groups[group].setdefault(name, []).append(path)
        else:
            groups[group].append(path)
    return groups, entries


def check_registry(config, repo, entries, grouped, sources):
    missing = sorted(path for path in config.get("required_paths", [])
                     if entries.get(path, ("",))[0] not in {"100644", "100755"})
    if missing:
        raise ValueError("missing required regular tracked paths: " + ", ".join(missing))
    active = {row["name"]: row["basis"] for row in config["technologies"]
              if row["status"] == "active"}
    expected_languages = {name for name, basis in active.items() if basis == "language"}
    observed_languages = set(grouped["languages"])
    if observed_languages - expected_languages:
        raise ValueError("unregistered source languages: "
                         + ", ".join(sorted(observed_languages - expected_languages)))
    if expected_languages - observed_languages:
        raise ValueError("declared languages without files: "
                         + ", ".join(sorted(expected_languages - observed_languages)))
    missing_formats = {name for name, basis in active.items()
                       if basis == "format" and name not in grouped["formats"]}
    if missing_formats:
        raise ValueError("declared formats without files: " + ", ".join(sorted(missing_formats)))
    reviewed = set(config.get("reviewed_paths", {}))
    needs_review = set(grouped["review_paths"])
    if needs_review - reviewed:
        raise ValueError("unreviewed tracked paths: " + ", ".join(sorted(needs_review - reviewed)))
    if reviewed - needs_review:
        raise ValueError("stale reviewed paths: " + ", ".join(sorted(reviewed - needs_review)))

    evidence_paths = {row["path"] for row in sources.values() if row["kind"] == "repo-file"}
    source_checks = config.get("source_checks", {})
    for path in set(source_checks) | evidence_paths:
        if entries.get(path, ("",))[0] not in {"100644", "100755"}:
            raise ValueError(f"evidence or source check needs a regular tracked file: {path}")
    for path, fragments in source_checks.items():
        body = git(repo, "show", f"{config['source_commit']}:{path}").decode("utf-8")
        for fragment in fragments:
            if fragment not in body:
                raise ValueError(f"source check failed: {path} must contain {fragment!r}")


def freshness(repo, revision, ref, docs_paths):
    result = {"ref": ref, "commit": None, "status": "unknown", "changed_paths": []}
    if not ref:
        result["reason"] = "no comparison ref supplied"
        return result
    if not ref.startswith("refs/"):
        raise ValueError("comparison refs must be fully qualified refs/ names")
    try:
        git(repo, "check-ref-format", ref)
        live = git(repo, "rev-parse", "--verify", "--end-of-options",
                   f"{ref}^{{commit}}").decode().strip()
        result["commit"] = live
        if live == revision:
            result["status"] = "current"
            return result
        git(repo, "merge-base", "--is-ancestor", revision, live)
        changes = decode_paths(git(repo, "diff", "--name-only", "--no-renames", "-z",
                                   revision, live, "--"))
    except subprocess.CalledProcessError:
        result["reason"] = "comparison ref or ancestry unavailable"
        return result
    result["changed_paths"] = sorted(changes)
    result["status"] = "docs-only" if set(changes) <= docs_paths else "stack-relevant"
    if not changes:
        result["reason"] = "different commit, identical tracked tree"
    return result


def run(repo, config, live_ref=None, release_ref=None):
    sources = validate_config(config)
    revision = config["source_commit"]
    groups, entries = inventory(repo, revision, config.get("overrides", {}))
    check_registry(config, repo, entries, groups, sources)
    docs_paths = DOC_PATHS | set(config.get("docs_only_paths", []))
    return {
        "project": config["project"],
        "source_repository": config.get("source_repository"),
        "source_ref": config.get("source_ref"),
        "source_commit": revision,
        "template_commit": config.get("template_commit"),
        "tracked_entries": len(entries),
        **groups,
        "freshness": {
            "live": freshness(repo, revision, live_ref, docs_paths),
            "release": freshness(repo, revision, release_ref, docs_paths),
        },
        "evidence": {
            "references_checked": len(sources),
            "repo_file_references_checked": sum(row["kind"] == "repo-file" for row in sources.values()),
            "reviewed_as_recorded": sum(row["review"] == "reviewed" for row in sources.values()),
            "external_links_fetched": 0,
            "claim_contents_checked": False,
        },
    }


def compact_receipt(report):
    identity = {key: report[key] for key in (
        "project", "source_repository", "source_ref", "source_commit", "template_commit",
        "tracked_entries", "evidence")}
    return {
        "receipt_version": 1,
        "result": "pass",
        "scope": "tracked Git inventory and structural evidence checks",
        **identity,
        "languages": {key: len(paths) for key, paths in report["languages"].items()},
        "formats": {key: len(paths) for key, paths in report["formats"].items()},
        "reviewed_paths": len(report["review_paths"]),
        "generated": len(report["generated"]),
        "vendored": len(report["vendored"]),
        "freshness": {
            key: {**{field: value for field, value in comparison.items() if field != "changed_paths"},
                  "changed_count": len(comparison["changed_paths"]),
                  "changed_sample": comparison["changed_paths"][:10]}
            for key, comparison in report["freshness"].items()
        },
        "github": {name.lower(): os.environ.get(f"GITHUB_{name}") for name in (
            "REPOSITORY", "RUN_ID", "RUN_ATTEMPT", "EVENT_NAME", "SHA", "JOB")},
    }


def json_text(data, indent=None):
    return json.dumps(data, sort_keys=True, indent=indent)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="target checkout")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--config", type=Path, help="schema v2 registry JSON")
    mode.add_argument("--discover", metavar="COMMIT", help="inventory a pinned commit before registration")
    parser.add_argument("--live-ref", help="fully qualified live ref fetched into the target checkout")
    parser.add_argument("--release-ref", help="fully qualified release ref fetched into the target checkout")
    parser.add_argument("--json", type=Path, help="write the full report")
    parser.add_argument("--summary", type=Path, help="append the audit receipt to a Markdown summary")
    args = parser.parse_args()
    if args.discover and (args.summary or args.live_ref or args.release_ref):
        parser.error("--summary and comparison refs require --config")
    try:
        if args.discover:
            groups, entries = inventory(args.repo, args.discover, {})
            report = {"source_commit": args.discover, "tracked_entries": len(entries), **groups}
            if not args.json:
                print(json_text(report, indent=2))
        else:
            config = json.loads(args.config.read_text(encoding="utf-8"))
            report = run(args.repo, config, args.live_ref, args.release_ref)
            receipt = json_text(compact_receipt(report))
            print("CODE_STACK_RECEIPT " + receipt)
            print("Result: PASS (tracked inventory and structural evidence checks)")
            if args.summary:
                with args.summary.open("a", encoding="utf-8") as output:
                    print("\n### Code Stack audit receipt\n\n~~~json", file=output)
                    print(receipt, file=output)
                    print("~~~", file=output)
        if args.json:
            args.json.write_text(json_text(report, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Code Stack audit failed: {error}\n")


if __name__ == "__main__":
    main()
