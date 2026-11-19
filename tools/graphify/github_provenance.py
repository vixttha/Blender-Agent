"""Verify candidate pull request provenance and report current GitHub review state."""

import json
import os
from functools import cache
from pathlib import Path
from urllib.request import Request, urlopen

from version_maps import COMMIT, REPOSITORY


def github_json(route: str):
    token = os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Blender-Agent-Graphify-HQ"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request(f"https://api.github.com/repos/{REPOSITORY}/{route}", headers=headers)
    with urlopen(request, timeout=15) as response:
        return json.load(response)


def pages(route: str, fetch=github_json):
    for page in range(1, 11):
        data = fetch(f"{route}?per_page=100&page={page}")
        if not isinstance(data, list):
            raise ValueError("Expected a GitHub API list: " + route)
        yield from data
        if len(data) < 100:
            return
    raise ValueError("GitHub API pagination limit reached: " + route)


def verify_pull_request(candidate: dict, fetch=github_json) -> dict:
    number = candidate["source_pr"]
    source = candidate["source_commit"]
    route = f"pulls/{number}"
    pr = fetch(route)
    head = pr["head"]
    if (
        pr["number"] != number
        or pr["base"]["repo"]["full_name"].lower() != REPOSITORY.lower()
        or (head["repo"] or {}).get("full_name", "").lower() != REPOSITORY.lower()
        or head["ref"] != candidate["source_branch"]
        or not COMMIT.fullmatch(head["sha"])
    ):
        raise ValueError(f"Candidate does not match the GitHub source of PR #{number}")

    is_head = source == head["sha"]
    if not is_head and not any(commit["sha"] == source for commit in pages(route + "/commits", fetch)):
        raise ValueError(f"Candidate {source} is absent from the GitHub commit list for PR #{number}")

    # Use the latest decision per reviewer across commits. Comments leave decisions intact.
    # Count an approval only when its latest decision is tied to the archived commit.
    decisions = {}
    for review in pages(route + "/reviews", fetch):
        if review["state"] in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"} and review["user"]:
            decisions[review["user"]["id"]] = review
    approvals = sum(
        review["state"] == "APPROVED" and review["commit_id"] == source
        for review in decisions.values()
    )
    return {
        "version": candidate["version"],
        "source_pr": number,
        "source_commit": source,
        "source_relation": "current head" if is_head else "historical PR commit",
        "head_commit": head["sha"],
        "pr_state": "merged" if pr["merged"] else "draft" if pr["draft"] and pr["state"] == "open" else pr["state"],
        "merge_commit": pr["merge_commit_sha"] if pr["merged"] else None,
        "exact_commit_approvals": approvals,
    }


def report_provenance(entries: list[dict]) -> None:
    lines = ["### Candidate provenance from GitHub", ""]
    fetch = cache(github_json)
    for entry in entries:
        result = verify_pull_request(entry, fetch)
        line = (
            f"- {result['version']} · PR #{result['source_pr']} · {result['pr_state']} · "
            f"{result['source_relation']} `{result['source_commit']}` · "
            f"PR head `{result['head_commit']}` · "
            f"{result['exact_commit_approvals']} exact-commit review approvals"
        )
        if result["merge_commit"]:
            line += f" · merge commit `{result['merge_commit']}`"
        lines.append(line)
    report = "\n".join(lines) + "\n"
    print(report, end="")
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with Path(summary).open("a", encoding="utf-8") as output:
            output.write("\n" + report)
