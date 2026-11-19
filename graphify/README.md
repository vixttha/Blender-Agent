# Graphify for Blender-Agent project instructions

[Instructions lineage manifest](versions.json) · [Mermaid lineage](versions.mmd) · [Archive workflow](../.github/workflows/instructions-archive.yml) · [Software Graphify HQ](https://github.com/vixttha/Blender-Agent/tree/graphify-hq)

The lineage manifest is a manually maintained catalog of ChatGPT instructions versions. Public GitHub-hosted Ubuntu builds a searchable graph of the active instructions, setup guide and acceptance checks using the pinned Graphify HQ generator and dependencies. The runner verifies graph statistics and document lookups using the read-only Graphify MCP process and records the tested commit, event, source documents, tooling revision, graph checksum and run URL. Software releases and product PR candidates use Graphify HQ’s catalog.

For a new instructions version, update the catalog and lineage, point `active_version` to the candidate, and keep its documents in a new version folder. Use a `proposes-successor` link until maintainer acceptance. To preserve a version, set `frozen_at` to the full commit that contains its exact directory and leave that folder intact. Keep ChatGPT connector access and installed-settings evidence explicit in their respective receipts.
