"""Discover components and evidence in a pinned Git tree without executing it."""

from collections import defaultdict
import json
from pathlib import PurePosixPath
import re
import subprocess
import tomllib

from audit import decode_paths, git
from language_profiles import ROLES

MAX_MANIFEST_BYTES = 256 * 1024
MANIFESTS = {
    "pyproject.toml": "python", "setup.py": "python", "setup.cfg": "python",
    "requirements.txt": "python", "package.json": "javascript", "Cargo.toml": "native",
    "go.mod": "go", "pom.xml": "jvm", "build.gradle": "jvm", "build.gradle.kts": "jvm",
    "Package.swift": "swift", "Gemfile": "ruby", "composer.json": "php", "CMakeLists.txt": "native",
}
BUILD_TOOLS = {
    "go.mod": "Go modules", "Cargo.toml": "Cargo", "pom.xml": "Maven",
    "build.gradle": "Gradle", "build.gradle.kts": "Gradle", "CMakeLists.txt": "CMake",
    "Package.swift": "Swift Package Manager", "Gemfile": "Bundler", "composer.json": "Composer",
}
BROWSER_TOOLS = {"vite", "webpack", "next", "react", "vue", "svelte", "@angular/core", "parcel"}
CI_PATHS = {".gitlab-ci.yml", ".circleci/config.yml", "azure-pipelines.yml", "Jenkinsfile"}
SAFE_FIELD = re.compile(r"[A-Za-z0-9_.@/+^<>=!~*,| -]{1,100}")


def regular(entry):
    return entry and entry[0] in {"100644", "100755"} and entry[1] == "blob"


def git_blob(repo, entry):
    oid = entry[2]
    if int(git(repo, "cat-file", "-s", oid)) <= MAX_MANIFEST_BYTES:
        return git(repo, "cat-file", "blob", oid).decode("utf-8")
    raise ValueError("manifest exceeds the scan size limit")


def mapping(value):
    return value if isinstance(value, dict) else {}


def deploy_value(value):
    return value if isinstance(value, str) and SAFE_FIELD.fullmatch(value) else None


def manifest_kind(name):
    if name.endswith((".csproj", ".fsproj", ".vbproj")):
        return "dotnet"
    return MANIFESTS.get(name)


def inspect_manifest(repo, entry, path):
    name = PurePosixPath(path).name
    roles = {manifest_kind(name)}
    facts = {"path": path, "ecosystem": manifest_kind(name)}
    if name in BUILD_TOOLS:
        facts["build_tool"] = BUILD_TOOLS[name]
    if name not in {"pyproject.toml", "package.json", "go.mod", "Cargo.toml"}:
        return roles, facts
    try:
        body = git_blob(repo, entry)
        if name in {"pyproject.toml", "Cargo.toml"}:
            data = tomllib.loads(body)
        elif name == "package.json":
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")
        else:
            data = {}
    except (ValueError, RecursionError):
        facts["detail"] = "Manifest content unavailable or unrecognized"
        return roles, facts

    if name == "pyproject.toml":
        project = mapping(data.get("project"))
        facts["declared_runtime"] = deploy_value(project.get("requires-python"))
        facts["build_tool"] = deploy_value(mapping(data.get("build-system")).get("build-backend"))
        scripts = mapping(project.get("scripts"))
        if scripts:
            roles.add("cli")
        if any(re.search(r"(?:^|[-_.])mcp(?:$|[-_.])", script, re.I) for script in scripts):
            roles.add("service")
            facts["entry_point_signal"] = "MCP-named Python console entry"
    elif name == "package.json":
        facts["declared_runtime"] = deploy_value(mapping(data.get("engines")).get("node"))
        manager = deploy_value(data.get("packageManager"))
        if manager:
            facts["build_tool"] = manager
        dependencies = set(mapping(data.get("dependencies"))) | set(mapping(data.get("devDependencies")))
        if dependencies & BROWSER_TOOLS:
            roles.add("browser")
        if isinstance(data.get("bin"), (str, dict)) and data["bin"]:
            roles.add("cli")
    elif name == "Cargo.toml":
        facts["declared_runtime"] = deploy_value(mapping(data.get("package")).get("rust-version"))
    elif name == "go.mod":
        match = re.search(r"^go ([0-9.]+)\s*$", body, re.M)
        if match:
            facts["declared_runtime"] = match[1]
    return roles, {key: value for key, value in facts.items() if value is not None}


def source_role_paths(repo, revision, classified_python):
    if not classified_python:
        return []
    # Git searches the pinned tree. Filter results through first-party source classification.
    try:
        hits = git(repo, "grep", "-I", "-l", "-z", "-E",
                   r"^[[:space:]]*(import[[:space:]]+bpy([[:space:],.]|$)|from[[:space:]]+bpy([[:space:].]|$))",
                   revision, "--", "*.py")
    except subprocess.CalledProcessError as error:
        if error.returncode != 1:
            raise
        return []
    prefix = revision + ":"
    return sorted(path[len(prefix):] for path in decode_paths(hits)
                  if path.startswith(prefix) and path[len(prefix):] in classified_python)


def component_root(path, roots):
    return next((parent.as_posix() for parent in PurePosixPath(path).parents if parent.as_posix() in roots), ".")


def discover(repo, revision, groups, entries, goals):
    first_party = sorted(set(entries) - set(groups["generated"]) - set(groups["vendored"]))
    manifest_paths = [path for path in first_party
                      if regular(entries[path]) and manifest_kind(PurePosixPath(path).name)]
    roots = {PurePosixPath(path).parent.as_posix() for path in manifest_paths} | {goal["component"] for goal in goals}
    components = defaultdict(lambda: {"roles": defaultdict(set), "languages": defaultdict(list), "manifests": []})

    for path in manifest_paths:
        root = PurePosixPath(path).parent.as_posix()
        roles, fact = inspect_manifest(repo, entries[path], path)
        components[root]["manifests"].append(fact)
        for role in roles:
            components[root]["roles"][role].add(path)

    for language, paths in groups["languages"].items():
        for path in paths:
            components[component_root(path, roots)]["languages"][language].append(path)
    for path in source_role_paths(repo, revision, set(groups["languages"].get("Python", []))):
        components[component_root(path, roots)]["roles"]["blender-worker"].add(path)

    for goal in goals:
        components[goal["component"]]["roles"][goal["role"]]

    # Associate source-only and mixed-language components with matching language roles.
    for row in components.values():
        roles, languages = row["roles"], row["languages"]
        if "browser" in roles and not roles["browser"]:
            jsx = sorted(path for lang in ("JavaScript", "TypeScript")
                         for path in languages.get(lang, []) if path.endswith((".tsx", ".jsx")))
            roles["browser"].update(jsx[:1])
        covered = {language for role in roles for language in ROLES[role][1]}
        for language, paths in sorted(languages.items()):
            if language in covered:
                continue
            candidates = [role for role, (_, names) in ROLES.items()
                          if role not in {"browser", "blender-worker", "cli", "service"} and language in names]
            roles[candidates[0] if candidates else "unknown"].add(paths[0])

    result = []
    for root, row in sorted(components.items()):
        result.append({
            "path": root,
            "languages": dict(sorted((language, len(paths)) for language, paths in row["languages"].items())),
            "language_samples": {language: paths[0] for language, paths in sorted(row["languages"].items())},
            "manifests": row["manifests"],
            "roles": {role: sorted(paths) for role, paths in sorted(row["roles"].items())},
        })
    ci = [path for path in first_party if regular(entries[path])
          and (path in CI_PATHS or re.fullmatch(r"\.github/workflows/[^/]+\.ya?ml", path))]
    tooling = []
    package_tools = {
        "package-lock.json": "npm", "pnpm-lock.yaml": "pnpm", "yarn.lock": "Yarn",
        "bun.lock": "Bun", "bun.lockb": "Bun", "uv.lock": "uv", "poetry.lock": "Poetry",
        "Makefile": "Make", "Dockerfile": "Docker", "Containerfile": "Container toolchain",
    }
    for path in first_party:
        name = PurePosixPath(path).name
        if regular(entries[path]) and name in package_tools:
            tooling.append({"name": package_tools[name], "path": path})
    return result, ci, tooling
