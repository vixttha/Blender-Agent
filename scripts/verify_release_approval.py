"""Verify an owner-dispatched release decision and exact-commit CI without publishing."""

import json
import os
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


def validate_dispatch(event, env, version):
    owner = event["repository"]["owner"]
    default_branch = event["repository"]["default_branch"]
    approval = {
        "release_tag": env["RELEASE_TAG"],
        "release_sha": env["RELEASE_SHA"],
        "ci_run_id": env["RELEASE_CI_RUN_ID"],
    }
    if env["GITHUB_EVENT_NAME"] != "workflow_dispatch":
        raise ValueError("Release approval requires a manual workflow dispatch.")
    if str(owner["id"]) != env["GITHUB_ACTOR_ID"] or owner["login"] != env["GITHUB_TRIGGERING_ACTOR"]:
        raise ValueError("The repository owner must dispatch the release decision.")
    if any(event["inputs"].get(key) != value for key, value in approval.items()):
        raise ValueError("Release inputs differ from the owner's dispatch.")
    tag, sha, run_id = approval.values()
    if not re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", tag):
        raise ValueError("Release tag must use the final vMAJOR.MINOR.PATCH form.")
    if tag != f"v{version}":
        raise ValueError("The approved tag does not match the package version.")
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or sha != env["GITHUB_SHA"] or (
        env["GITHUB_REF"] != f"refs/heads/{default_branch}"
    ):
        raise ValueError("Dispatch must select the exact approved commit on the default branch.")
    if not re.fullmatch(r"[1-9][0-9]*", run_id):
        raise ValueError("A valid application CI run ID is required.")
    return tag, sha, int(run_id), default_branch


def validate_ci(run, jobs, *, sha, default_branch, expected_run, expected_workflow):
    if (run["id"], run["workflow_id"], run["head_sha"], run["head_branch"], run["event"],
        run["status"], run["conclusion"]) != (
        expected_run, expected_workflow, sha, default_branch, "push", "completed", "success",
    ):
        raise ValueError("Application CI must pass on the exact approved default-branch commit.")
    results = jobs["jobs"]
    if not results or len(results) != jobs["total_count"] or any(job["conclusion"] != "success" for job in results):
        raise ValueError("Every application CI job must be present and successful.")


def main():
    env = os.environ
    event = json.loads(Path(env["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    version = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    tag, sha, run_id, branch = validate_dispatch(event, env, version)
    prefix = f'{env["GITHUB_API_URL"]}/repos/{env["GITHUB_REPOSITORY"]}'

    def get(path):
        request = Request(
            prefix + path,
            headers={"Accept": "application/vnd.github+json", "Authorization": f'Bearer {env["GH_TOKEN"]}'},
        )
        with urlopen(request, timeout=20) as response:
            return json.load(response)

    if get(f"/commits/{quote(branch, safe='')}")["sha"] != sha:
        raise ValueError("The default branch advanced after the release dispatch.")
    workflow = get("/actions/workflows/ci.yml")
    run = get(f"/actions/runs/{run_id}")
    jobs = get(f"/actions/runs/{run_id}/jobs?per_page=100")
    validate_ci(run, jobs, sha=sha, default_branch=branch, expected_run=run_id, expected_workflow=workflow["id"])
    with Path(env["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
        print(f"release_tag={tag}", f"release_sha={sha}", sep="\n", file=output)
    print(f"Verified owner approval for {tag} at {sha} using CI run {run_id}.")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, ValueError) as exc:
        print(f"Release approval rejected. {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
