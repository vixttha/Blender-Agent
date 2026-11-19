# Blender-Agent — Graphify HQ

This is the permanent, independent version-mapping branch for the public Blender-Agent project.

**Workspace:** graphify-hq  
**Application source:** [main](https://github.com/vixttha/Blender-Agent/tree/main)  
**Scope:** version discovery, reproducible graphs, provenance, and read-only Graphify MCP checks.

This branch is intentionally sparse. It is not the Blender add-on/runtime, a distribution branch, or a replacement for the public project's README on main. Do not merge this entire branch into main.

## Start here

| Area | Purpose |
| --- | --- |
| [Version catalog](catalog/versions.json) | Approved Blender-Agent releases and their immutable source commits. |
| [Version archive](versions/README.md) | One graph, navigable outline, and evidence receipt per approved release. |
| [Release candidates](candidates/README.md) | Provisional source-pinned maps; never treated as approved releases. |
| [Graphify workflow guide](tools/graphify/README.md) | How to build, query, review, and reproduce each version map. |
| [Public-runner validation](.github/workflows/graphify-hq.yml) | Read-only verification on standard GitHub-hosted Ubuntu runners. |
| [Security and operating rules](SECURITY.md) | No credentials, local execution requirements, or public personal details. |

## Version lifecycle

1. Approve and tag a Blender-Agent release on main or an explicitly reviewed source commit. A release tag alone does not constitute approval.
2. Record its full 40-character source SHA, matching release tag, and public Markdown source paths in catalog/versions.json. The catalog starts empty; no releases have been assumed.
3. Generate its version folder under versions/vX.Y.Z. The folder contains README.md, graph.json, and receipt.json. Do not overwrite a previously accepted snapshot to hide a discrepancy.
4. Let GitHub Actions rebuild the committed graph and verify Graphify MCP read-back, document provenance, and deterministic byte equality.
5. Review the exact branch commit and CI evidence before calling that version archived.

The version graph is a documentation and version-discovery aid, not a claim that code has passed release or gameplay tests. A version's acceptance requires independent release evidence.

## Permanent branch rules

- Maintain graphify-hq as its own long-lived branch; keep the main branch untouched unless a separate change is expressly approved.
- Preserve previously approved per-version snapshots. Amend using a new reviewed change with an auditable explanation.
- Use standard **free public-repository GitHub-hosted runners**; do not require self-hosted, local, or paid runners.
- Graphify MCP runs in a short-lived, read-only subprocess in CI. It must not receive write credentials.
- Store no personal information, credentials, private repositories, machine-specific paths, or invented version history.
- The checked-in workflow validates artifacts but never automatically creates a release, promotes a tag, merges branches, or writes to the repository.

**Current archive:** no approved Blender-Agent versions have been registered. The proposed v0.0.1 foundation has a separate candidate catalog, pending validation and release approval.
