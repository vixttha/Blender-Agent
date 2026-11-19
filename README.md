# Blender-Agent Refinement Toolkit — Graphify HQ

This is the permanent, independent version-mapping branch for the public Blender-Agent Refinement Toolkit project.

**Workspace:** graphify-hq  
**Application source:** [main](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/main)  
**Scope:** version discovery, reproducible graphs, provenance, and read-only Graphify MCP checks.

This branch is intentionally sparse. It is not the Blender add-on/runtime, a distribution branch, or a replacement for the public project's README on main. Do not merge this entire branch into main.

## Start here

| Area | Purpose |
| --- | --- |
| [Version catalog](catalog/versions.json) | Approved Blender-Agent Refinement Toolkit releases and their immutable source commits. |
| [Version archive](versions/README.md) | One graph, navigable outline, and evidence receipt per approved release. |
| [Release candidates](candidates/README.md) | Provisional source-pinned maps; never treated as approved releases. |
| [OBJ/MTL export evidence](evidence/obj-mtl/v0.0.2.1/README.md) | Feature map for the v0.0.2.1 candidate, including exact source, regressions, and public Blender results. |
| [Graphify workflow guide](tools/graphify/README.md) | How to build, query, review, and reproduce each version map. |
| [Public-runner validation](.github/workflows/graphify-hq.yml) | Read-only verification on standard GitHub-hosted Ubuntu runners. |
| [Security and operating rules](SECURITY.md) | No credentials, local execution requirements, or public personal details. |

## Version lifecycle

1. Approve and tag a Blender-Agent Refinement Toolkit release on main or an explicitly reviewed source commit. A release tag alone does not constitute approval.
2. Record its full 40-character source SHA, matching release tag, and public Markdown source paths in catalog/versions.json.
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

**Current archive:** [Blender-Agent v0.0.3](versions/v0.0.3/README.md) maps the [published pre-release](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/releases/tag/v0.0.3) at [`7febadd`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/commit/7febadd1d18bd15967e9eed6223098268dadfe2f). See the [application CI](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44469831772) and [publication run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44470636744). The [v0.0.2 release](versions/v0.0.2/README.md), [v0.0.3 candidate at `38e8f63`](candidates/v0.0.3/README.md), and earlier foundation candidate remain available as historical snapshots.

**Current application candidate:** [Blender-Agent v0.0.3](candidates/v0.0.3/README.md) maps [main at `38e8f63`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/commit/38e8f63c3fe2e372784276acdbb602cb7409b100). The [exact-commit public CI run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44462288861) passed all nine application jobs and the read-only release-readiness job.
