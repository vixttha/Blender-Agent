# Graphify for Blender-Agent Refinement Toolkit project instructions

[Instructions lineage manifest](versions.json) · [Mermaid lineage](versions.mmd) · [Archive workflow](../.github/workflows/instructions-archive.yml) · [Software Graphify HQ](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/graphify-hq)

The lineage manifest is a manually maintained catalog of ChatGPT instructions versions. Public GitHub-hosted Ubuntu builds a searchable graph of the active instructions, setup guide and acceptance checks using the pinned Graphify HQ generator and dependencies. The runner verifies graph statistics and document lookups using the read-only Graphify MCP process and records the tested commit, event, source documents, tooling revision, graph checksum and run URL. Software releases and product PR candidates use Graphify HQ’s catalog.

For a new instructions version, update the catalog and lineage, point `active_version` to the candidate, and keep its documents in a new version folder. Use a `proposes-successor` link until maintainer acceptance. To preserve a version, set `frozen_at` to the full commit that contains its exact directory and leave that folder intact. Keep ChatGPT connector access and installed-settings evidence explicit in their respective receipts.

## v0.0.3 instructions graph

[Generated graph](instructions/v0.0.3/graph.json) · [Source and MCP receipt](instructions/v0.0.3/receipt.json) · [Verification record](../v0.0.3/VERIFICATION.md)

The [Instructions HQ push job](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44490625604/job/135445009998) generated this snapshot from [`b63b7b68495abcce76dfbc4341aa149ea15e0049`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/commit/b63b7b68495abcce76dfbc4341aa149ea15e0049) using Graphify 0.9.109. The runner verified 19 nodes, 20 edges, and read-only lookups for the instructions, setup guide, and acceptance checks.

## v0.0.2 instructions graph

[Generated graph](instructions/v0.0.2/graph.json) · [Graphify source and MCP receipt](instructions/v0.0.2/receipt.json) · [Verification history](../v0.0.2/VERIFICATION.md)

The archive verifies the committed graph checksum and its three source blobs. If the active candidate documents change before acceptance, keep the prior snapshot in Git history and remove the stale candidate snapshot from the new commit. The public-runner workflow then emits a fresh graph and receipt for archival without requiring artifact storage.
