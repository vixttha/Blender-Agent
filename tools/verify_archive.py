"""Test each version and rebuild its pinned evidence on the GitHub runner."""

import base64
import json
import os
import re
import subprocess
import tempfile
import venv
from pathlib import Path


def run(*args):
    subprocess.run(args, check=True)


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def export_candidate(version, source, output):
    print(f"GRAPHIFY_HQ_SOURCE {version} {source}", flush=True)
    for name in ("graph.json", "receipt.json"):
        payload = base64.b64encode((output / name).read_bytes()).decode("ascii")
        for index, offset in enumerate(range(0, len(payload), 1024)):
            print(f"GRAPHIFY_HQ_EXPORT {version} {name} {index} {payload[offset:offset + 1024]}")
    print("Candidate rebuilt byte for byte and read back through Graphify MCP.", flush=True)


def verify_version(version, entry, head, staging):
    kit = Path("versions") / version
    source = entry["source_commit"]
    archived = source is not None
    if archived:
        if not re.fullmatch(r"[0-9a-f]{40}", source):
            raise ValueError(f"{version} requires a full source commit SHA")
        run("git", "merge-base", "--is-ancestor", source, head)
        run("git", "diff", "--exit-code", source, head, "--", str(kit))
    else:
        source = head

    environment = staging / "venv"
    venv.create(environment, with_pip=True)
    python = str(environment / "bin" / "python")
    run(
        python, "-m", "pip", "install", "--require-hashes", "--no-cache-dir",
        "--only-binary=:all:", "--no-deps", "-r", str(kit / "requirements.txt"),
    )
    run(python, "-m", "pip", "check")
    run(python, "-m", "unittest", "discover", "-s", str(kit), "-p", "test_*.py", "-v")

    manifest = json.loads((kit / "self-map.json").read_text(encoding="utf-8"))
    manifest.update(repository=os.environ["GITHUB_REPOSITORY"], source_commit=source)
    manifest_path = staging / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output = Path("graphify") / version if archived else staging / "candidate"
    command = (python, str(kit / "evidence_map.py"), str(manifest_path), str(output))
    if not archived:
        run(*command)
    run(*command, "--check")
    if archived:
        print(f"Verified the saved {version} graph and receipt at source {source}.", flush=True)
    else:
        export_candidate(version, source, output)


def main():
    catalog = json.loads(Path("graphify/catalog.json").read_text(encoding="utf-8"))
    versions = catalog["versions"]
    if not versions or not all(re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", key) for key in versions):
        raise ValueError("Expected version IDs in major.minor.patch form")
    ordered = sorted(versions, key=lambda key: tuple(map(int, key[1:].split("."))))
    if catalog["latest"] != ordered[-1]:
        raise ValueError("Catalog latest must identify the highest version")
    head = git_head()
    print(f"Template checkout SHA: {head}", flush=True)
    for version in ordered:
        if versions[version]["source_commit"] is None and version != catalog["latest"]:
            raise ValueError("Only the latest version can be a candidate")
        with tempfile.TemporaryDirectory() as temporary:
            verify_version(version, versions[version], head, Path(temporary))


if __name__ == "__main__":
    main()
