# Graphify — Instructions archive map

This is **Archivewright's dedicated instructions-version graph** for Blender-Agent. Its purpose is to distinguish the persistent instructions branch, its version folders, and release lineage from the application's own source-code/version graph.

- Canonical editable map: [versions.json](versions.json).
- Human-readable topology: [versions.mmd](versions.mmd).
- Runner validation: [instructions-archive.yml](../.github/workflows/instructions-archive.yml).
- Repo: https://github.com/vixttha/Blender-Agent

The graph is a Git-tracked handoff manifest, **not an output from Graphify MCP**. Use `$graphify` when accessible to index actual code and version history; preserve the Graphify tool version, extraction scope, exact source SHA, artifact checksum, and real workflow/MCP receipt separately. Never mark `mcp_verified=true` unless a Graphify invocation actually succeeds.

The standard public-runner job validates the manifest against real version folders, derives a checksum, and prints the graph and SHA-bound receipt into Actions logs and the job summary without credentials or a paid Graphify account. The runner's graph validation is **not** an MCP invocation.

## Update contract

Each new `vX.Y.Z/` folder gets a unique version node and a `contains` link from the permanent branch. Successive versions get a `supersedes` link only when a new version is explicitly accepted; candidates may have `proposes-successor` links instead. Never mutate accepted snapshots or invent run URLs. `main` is the engineering baseline, not an automatic target for instructions-archive merges.
