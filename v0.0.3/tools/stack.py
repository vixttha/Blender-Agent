"""Generate a portable Code Stack language review from a Git repository and ref."""

import argparse
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from urllib.parse import quote, urlsplit

from audit import LANGUAGES, decode_paths, git, inventory, json_text
from language_profiles import BLENDER_API, PROFILES, ROLES
from scan import discover

VERSION = "v0.0.3"
ACTIONS = {"keep", "adopt", "defer", "drop"}
GITHUB_ID = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")


def revision_at(repo, ref):
    return git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()


def github_project(repo):
    try:
        origin = git(repo, "config", "--get", "remote.origin.url").decode().strip()
    except subprocess.CalledProcessError as error:
        if error.returncode == 1:
            return None
        raise
    if origin.startswith("git@github.com:"):
        slug = origin.removeprefix("git@github.com:")
    else:
        url = urlsplit(origin)
        slug = url.path.strip("/") if url.scheme in {"ssh", "https"} and url.hostname == "github.com" else ""
    slug = slug.removesuffix(".git")
    return slug if GITHUB_ID.fullmatch(slug) else None


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path else {}


def component_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("component must be a project-relative Git path or .")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value != path.as_posix():
        raise ValueError("component must be a normalized project-relative path or .")
    return value


def goals_from(context):
    if not isinstance(context, dict) or set(context) - {"goals"}:
        raise ValueError("context must be a JSON object with an optional goals array")
    if "goals" in context and not isinstance(context["goals"], list):
        raise ValueError("context.goals must be an array")
    goals = {}
    for entry in context.get("goals", []):
        if not isinstance(entry, dict):
            raise ValueError("each goal must be a JSON object")
        component = component_path(entry.get("component"))
        role, need = entry.get("role"), entry.get("need")
        if not isinstance(role, str) or role not in ROLES or role == "unknown":
            raise ValueError("each goal needs a supported role")
        if not isinstance(need, str) or not need.strip():
            raise ValueError("each goal needs a short project requirement")
        key = (component, role)
        if key in goals:
            raise ValueError("duplicate goal for the same component and role")
        goals[key] = {"component": component, "role": role, "need": need.strip()}
    return goals


def language_choice(role, language, current, planned):
    if role == "blender-worker" and language != "Python":
        return "drop", "This job uses Blender's in-process Python API. A native helper would need a separate integration decision.", BLENDER_API
    if language in current:
        return "keep", "Present in this component and a fit for the detected or stated role. An alternative should solve a specific constraint.", None
    if role == "blender-worker" and language == "Python":
        return "adopt", "Blender exposes its in-process scripting interface through bpy.", BLENDER_API
    if role == "native":
        return "defer", "Profile the end-to-end workload and verify packaging on supported platforms before adopting a native toolchain.", None
    if planned and not current and language == ROLES[role][1][0]:
        return "adopt", "Candidate for the stated requirement. Confirm runtime, deployment and compatibility in a small pilot.", None
    return "defer", "Consider if a stated requirement gives this runtime a concrete advantage over the baseline.", None


def decision_key(row):
    component = component_path(row.get("component"))
    role, language = row.get("role"), row.get("language")
    if not isinstance(role, str) or role not in ROLES or not isinstance(language, str) or not language:
        raise ValueError("decision needs a valid component, role and language")
    return component, role, language


def digest_json(value):
    return hashlib.sha256(json_text(value).encode("utf-8")).hexdigest()


def compare_components(components, goals, entries, ci):
    rows = []
    for component in components:
        root = component["path"]
        for role, signals in component["roles"].items():
            goal = goals.get((root, role))
            supported = ROLES[role][1]
            current = set(component["languages"]) & set(supported)
            if role == "unknown":
                unsupported = set(component["languages"]) - set(PROFILES)
                for language in sorted(unsupported):
                    rows.append({
                        "component": root, "role": role, "language": language, "verdict": "keep",
                        "reason": "Detected source needs an owner for comparison. Assess its role before a migration.",
                        "evidence_paths": [component["language_samples"][language]],
                        "benefit": "Retains the current implementation.",
                        "cost": "No reviewed tradeoff profile exists in this template.",
                        "primary_sources": [],
                    })
                continue
            for language in supported:
                source, benefit, cost = PROFILES[language]
                verdict, reason, role_source = language_choice(role, language, current, goal is not None)
                paths = set(signals)
                paths.update(component["language_samples"][name] for name in current)
                rows.append({
                    "component": root, "role": role, "language": language, "verdict": verdict,
                    "reason": reason, "benefit": benefit, "cost": cost,
                    "evidence_paths": sorted(paths),
                    "primary_sources": [source] + ([role_source] if role_source else []),
                    "goal": goal,
                })
    for row in rows:
        # A changed representative source, integration signal, CI, goal or rule reopens review.
        bound_paths = set(row["evidence_paths"]) | set(ci)
        row["evidence_fingerprint"] = digest_json([
            VERSION, row, {path: entries[path][2] for path in sorted(bound_paths)},
        ])
    return sorted(rows, key=lambda row: (row["component"], row["role"],
                                         ("keep", "adopt", "defer", "drop").index(row["verdict"]),
                                         row["language"]))


def previous_changes(repo, previous, revision, project, repository):
    if not previous:
        return {"state": "initial", "previous_commit": None, "changed_paths": []}
    if not isinstance(previous, dict) or previous.get("schema_version") != 3:
        raise ValueError("--previous must be a generated Code Stack schema 3 registry")
    if (previous.get("source_repository"), previous.get("project")) != (repository, project):
        raise ValueError("previous registry belongs to a different project")
    old = previous.get("source_commit", "")
    if not isinstance(old, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", old):
        raise ValueError("previous registry requires a full source commit")
    if old == revision:
        return {"state": "same-commit", "previous_commit": old, "changed_paths": []}
    try:
        revision_at(repo, old)
    except subprocess.CalledProcessError:
        return {"state": "previous-source-unavailable", "previous_commit": old, "changed_paths": []}
    paths = decode_paths(git(repo, "diff", "--name-only", "--no-renames", "-z", old, revision, "--"))
    return {"state": "compared", "previous_commit": old, "changed_paths": sorted(paths)}


def preserve_decisions(previous, reviewed, rows, revision):
    current = {decision_key(row): row for row in rows}
    carried = {decision_key(row): dict(row) for row in previous.get("approved_decisions", [])}
    old_rows = {decision_key(row): row for row in previous.get("recommendations", [])}
    if not isinstance(reviewed, list):
        raise ValueError("approved decisions must be an array")
    seen = set()
    for item in reviewed:
        if not isinstance(item, dict):
            raise ValueError("each approval must be an object")
        key = decision_key(item)
        action, reason = item.get("action"), item.get("reason")
        if key in seen or key not in current or not isinstance(action, str) or action not in ACTIONS or not isinstance(reason, str) or not reason.strip():
            raise ValueError("approval needs a unique current recommendation, action and reason")
        seen.add(key)
        carried[key] = {
            "component": key[0], "role": key[1], "language": key[2],
            "action": action, "reason": reason.strip(), "approved_at_source": revision,
            "approved_evidence": current[key]["evidence_fingerprint"],
        }
    for key, item in carried.items():
        if key not in current:
            item["status"] = "component-or-candidate-missing"
        elif item["approved_evidence"] != current[key]["evidence_fingerprint"]:
            item["status"] = "review-needed"
        else:
            item["status"] = "current"
    changes = []
    if previous:
        for key in sorted(old_rows.keys() | current.keys()):
            old, new = old_rows.get(key, {}), current.get(key, {})
            if old.get("evidence_fingerprint") != new.get("evidence_fingerprint"):
                changes.append({"component": key[0], "role": key[1], "language": key[2],
                                "before": old.get("verdict"), "after": new.get("verdict")})
    return [row for _, row in sorted(carried.items())], changes


def evidence_record(repository, revision, path, entry):
    return {
        "path": path, "blob": entry[2],
        "url": f"https://github.com/{repository}/blob/{revision}/{quote(path, errors='surrogateescape')}" if repository else None,
    }


def build_registry(repo, ref, project, context, previous, approvals):
    revision = revision_at(repo, ref)
    repository = github_project(repo)
    project = project or (repository.split("/")[-1] if repository else repo.resolve().name)
    changes = previous_changes(repo, previous, revision, project, repository)
    goals = goals_from(context)
    groups, entries = inventory(repo, revision, {}, require_checkout=False)
    components, ci, tooling = discover(repo, revision, groups, entries, list(goals.values()))
    recommendations = compare_components(components, goals, entries, ci)
    decisions, changed_rows = preserve_decisions(previous, approvals, recommendations, revision)
    evidence_paths = set(ci) | {item["path"] for item in tooling}
    for component in components:
        evidence_paths.update(component["language_samples"].values())
        evidence_paths.update(item["path"] for item in component["manifests"])
    for row in recommendations:
        evidence_paths.update(row["evidence_paths"])
    return {
        "schema_version": 3, "template_version": VERSION, "project": project,
        "source_repository": repository, "source_ref": ref, "source_commit": revision,
        "tracked_entries": len(entries), "inventory": groups, "components": components,
        "ci_definitions": ci, "tooling": tooling, "goals": list(goals.values()),
        "evidence": {path: evidence_record(repository, revision, path, entries[path])
                     for path in sorted(evidence_paths)},
        "recommendations": recommendations, "approved_decisions": decisions,
        "refresh": {**changes, "recommendations_for_review": changed_rows},
        "catalog": {
            "inventory_labels": sorted({name for name in LANGUAGES.values() if "(review)" not in name}),
            "compared_profiles": sorted({row["language"] for row in recommendations} & set(PROFILES)),
            "profiles_outside_detected_roles": sorted(set(PROFILES) - {row["language"] for row in recommendations}),
        },
    }


def safe(value):
    # Bound source-controlled text to a single Markdown line, without active links or markup.
    line = str(value).encode("utf-8", "backslashreplace").decode("utf-8")
    return "".join(f"&#{ord(char)};" if char in "|[]*`_~\\" else html.escape(char)
                   for char in line.replace("\r", " ").replace("\n", " "))


def render_report(registry):
    inventory_data = registry["inventory"]
    evidence = registry["evidence"]
    lines = [f"# Code Stack · {safe(registry['project'])}", "",
             f"Source commit `{registry['source_commit']}` · template {VERSION}",
             "", "## Observed stack", ""]
    for group in ("languages", "formats"):
        lines.append(f"**{group.title()}**")
        lines.append("")
        lines.extend(f"- {safe(name)} · {len(paths)} tracked files" for name, paths in inventory_data[group].items())
        if not inventory_data[group]:
            lines.append("- None classified")
        lines.append("")
    for component in registry["components"]:
        facts = [f"{key.replace('_', ' ')} {safe(value)}" for row in component["manifests"]
                 for key, value in row.items() if key not in {"path", "ecosystem"}]
        label = ", ".join(safe(name) for name in component["languages"]) or "no classified sources"
        lines.append(f"- **{safe(component['path'])}** · {label}" + (f" · {', '.join(facts)}" if facts else ""))
    lines.extend([f"- CI definitions observed · {len(registry['ci_definitions'])}",
                  f"- Files requiring classification review · {len(inventory_data['review_paths'])}",
                  "", "## Language recommendations", "",
                  "| Component and role | Language | Verdict | Why | Benefit | Cost or validation needed |",
                  "| --- | --- | --- | --- | --- | --- |"])
    for row in registry["recommendations"]:
        label = ROLES[row["role"]][0]
        lang = safe(row["language"])
        if row["primary_sources"]:
            lang = f"[{lang}]({row['primary_sources'][0]})"
        reason = safe(row["reason"])
        if len(row["primary_sources"]) > 1:
            reason += f" [Host API]({row['primary_sources'][1]})"
        if row.get("goal"):
            reason += f" Goal · {safe(row['goal']['need'])}"
        lines.append(f"| {safe(row['component'])} · {label} | {lang} | **{row['verdict']}** | "
                     f"{reason} | {safe(row['benefit'])} | {safe(row['cost'])} |")
        if row["evidence_paths"]:
            rendered_paths = []
            for path in row["evidence_paths"]:
                link = evidence[path]["url"]
                rendered_paths.append(f"[{safe(path)}]({link})" if link else safe(path))
            lines[-1] = lines[-1][:-2] + " Evidence · " + ", ".join(rendered_paths) + " |"
    if not registry["recommendations"]:
        lines.append("| — | — | — | No language role could be inferred. Supply a project goal to compare a new component. | — | — |")
    outside = registry["catalog"]["profiles_outside_detected_roles"]
    lines.extend(["", "Profiles screened out by component role · " + (", ".join(outside) or "none"),
                  "", "## Refresh and owner decisions", "",
                  f"Comparison · {registry['refresh']['state']}",
                  f"Changed tracked paths · {len(registry['refresh']['changed_paths'])}",
                  f"Recommendations to revisit · {len(registry['refresh']['recommendations_for_review'])}", ""])
    lines.extend(f"- Review {safe(row['component'])} · {ROLES[row['role']][0]} · {safe(row['language'])}"
                 for row in registry["refresh"]["recommendations_for_review"])
    lines.extend(f"- {safe(row['component'])} · {safe(row['language'])} · {row['action']} · "
                 f"{row['status']} · {safe(row['reason'])}"
                 for row in registry["approved_decisions"])
    lines.extend(["", "## Evidence limits", "",
                  "This report uses tracked source, manifest signals and a bundled comparison catalog. "
                  "A CI definition shows intended coverage. Runtime, performance and platform claims require separate validation.",
                  "The linked primary documentation is catalog evidence. This run did not fetch the links or execute target code.", ""])
    return "\n".join(lines)


def write_reports(registry, output, template_source):
    output.mkdir(parents=True, exist_ok=True)
    files = {"code-stack.json": json_text(registry, indent=2) + "\n", "REPORT.md": render_report(registry)}
    receipt = {
        "receipt_version": 1, "result": "pass", "template_version": VERSION,
        "template_commit": template_source, "source_commit": registry["source_commit"],
        "source_repository": registry["source_repository"], "source_ref": registry["source_ref"],
        "tracked_entries": registry["tracked_entries"], "evidence_paths_bound": len(registry["evidence"]),
        "recommendations": len(registry["recommendations"]), "runtime_validated": False,
        "external_links_fetched": 0,
        "outputs_sha256": {name: hashlib.sha256(body.encode("utf-8")).hexdigest()
                           for name, body in files.items()},
    }
    files["receipt.json"] = json_text(receipt, indent=2) + "\n"
    with tempfile.TemporaryDirectory(dir=output) as stage:
        for name, body in files.items():
            (Path(stage) / name).write_bytes(body.encode("utf-8"))
        for name in files:
            os.replace(Path(stage) / name, output / name)
    print("CODE_STACK_REVIEW_RECEIPT " + json_text(receipt))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="existing Git repository or bare clone")
    parser.add_argument("--ref", default="HEAD", help="commit, branch or tag (default HEAD)")
    parser.add_argument("--out", type=Path, required=True, help="directory for the generated report, registry and receipt")
    parser.add_argument("--project", help="display name and portable project identity")
    parser.add_argument("--context", type=Path, help="optional JSON file of project goals")
    parser.add_argument("--previous", type=Path, help="previous generated code-stack.json")
    parser.add_argument("--approve", type=Path, help="optional JSON array of explicit owner decisions")
    parser.add_argument("--template-commit", help="full source SHA of this template, when known")
    args = parser.parse_args()
    try:
        if args.template_commit and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", args.template_commit):
            raise ValueError("--template-commit must be a full Git SHA")
        registry = build_registry(args.repo, args.ref, args.project, read_json(args.context),
                                  read_json(args.previous), read_json(args.approve) if args.approve else [])
        write_reports(registry, args.out, args.template_commit)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Code Stack review failed: {error}\n")


if __name__ == "__main__":
    main()
