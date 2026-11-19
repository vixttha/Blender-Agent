"""Test each version and rebuild its pinned evidence locally or in GitHub Actions."""

import argparse
import base64
import json
import os
import re
import subprocess
import tempfile
import venv
from pathlib import Path


GITHUB_REPOSITORY_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}")


def run(*args):
    subprocess.run(args, check=True)


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def execution_mode(environ):
    if environ.get("GITHUB_ACTIONS") != "true":
        return "local"
    event_path = environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise ValueError("GitHub Actions did not supply an event payload")
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    repository = event.get("repository") or {}
    if repository.get("visibility") in {"private", "internal"} or repository.get("private") is True:
        return "github-private"
    if repository.get("private") is False and repository.get("visibility") in {None, "public"}:
        return "github-public"
    raise ValueError("GitHub Actions event did not identify repository visibility")


def local_repository():
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=False,
    )
    remote = result.stdout.strip().removesuffix("/")
    match = re.fullmatch(r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)(.+)", remote)
    return match[1].removesuffix(".git") if match else None


def source_repository(entry, candidate_repository):
    if entry["source_commit"] is not None:
        repository = entry.get("source_repository")
    else:
        repository = candidate_repository
    if not isinstance(repository, str) or not GITHUB_REPOSITORY_NAME.fullmatch(repository):
        raise ValueError("Expected a GitHub owner/repository for the source. For a local candidate, pass --repository.")
    return repository


def export_candidate(version, source, output, mode):
    print(f"GRAPHIFY_HQ_SOURCE {version} {source}", flush=True)
    if mode != "github-public":
        print("Candidate verified. Graph and receipt payload omitted from the console.", flush=True)
        return
    for name in ("graph.json", "receipt.json"):
        payload = base64.b64encode((output / name).read_bytes()).decode("ascii")
        for index, offset in enumerate(range(0, len(payload), 1024)):
            print(f"GRAPHIFY_HQ_EXPORT {version} {name} {index} {payload[offset:offset + 1024]}")
    print("Candidate rebuilt byte for byte and read back through Graphify MCP.", flush=True)


def verify_version(version, entry, head, staging, mode, candidate_repository, candidate_output):
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

    repository = source_repository(entry, candidate_repository)
    environment = staging / "venv"
    venv.create(environment, with_pip=True)
    python = str(environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
    run(
        python, "-m", "pip", "install", "--require-hashes", "--no-cache-dir",
        "--only-binary=:all:", "--no-deps", "-r", str(kit / "requirements.txt"),
    )
    run(python, "-m", "pip", "check")
    run(python, "-m", "unittest", "discover", "-s", str(kit), "-p", "test_*.py", "-v")

    manifest = json.loads((kit / "self-map.json").read_text(encoding="utf-8"))
    manifest.update(repository=repository, source_commit=source)
    manifest_path = staging / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output = Path("graphify") / version if archived else candidate_output or staging / "candidate"
    command = (python, str(kit / "evidence_map.py"), str(manifest_path), str(output))
    if not archived:
        run(*command)
    run(*command, "--check")
    if archived:
        print(f"Verified the saved {version} graph and receipt at source {source}.", flush=True)
    else:
        export_candidate(version, source, output, mode)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", help="Source owner/repository for a local candidate without a GitHub origin")
    parser.add_argument("--candidate-output", type=Path, help="Keep a generated candidate graph and receipt in this directory")
    args = parser.parse_args()

    mode = execution_mode(os.environ)
    if mode != "local" and args.repository:
        parser.error("--repository is only available for local candidates")
    if mode == "local":
        candidate_repository = args.repository or local_repository()
    else:
        candidate_repository = os.environ.get("GITHUB_REPOSITORY")
    os.environ.setdefault("PYTHONHASHSEED", "0")
    os.environ.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")
    print(f"Graphify execution mode: {mode}", flush=True)

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
            verify_version(version, versions[version], head, Path(temporary), mode,
                           candidate_repository, args.candidate_output)


if __name__ == "__main__":
    main()
