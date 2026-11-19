# Code Stack Template version history

This is the comparison index for the template. Each version folder contains its complete portable kit. For MCP navigation, use the graph for the exact version you are inspecting.

| Area | [v0.0.1](v0.0.1/) | [v0.0.2](v0.0.2/) |
| --- | --- | --- |
| Registry | Schema v1 and literal source checks | Schema v2 with typed evidence, tracked source bindings and review status |
| Checkout | Audits a pinned Git commit | Also compares the pin with fetched live and release refs |
| Output | File inventory, counts and optional JSON report | Adds a compact JSON receipt to CI logs and the job summary |
| Detection | Groups tracked files by type and flags ambiguous paths | Adds common executable shebangs, generated and vendored categories, and explicit review of mixed formats |
| Installation | Portable kit with a sample registry | Adds [migration guidance](v0.0.2/MIGRATION.md), a [copyable CI workflow](v0.0.2/workflow.example.yml), and a copied-install test |
| Graphify | [Graph](graphify/v0.0.1/graph.json) · [Receipt](graphify/v0.0.1/receipt.json) | [Graph](graphify/v0.0.2/graph.json) · [Receipt](graphify/v0.0.2/receipt.json) |

## v0.0.2

The revised auditor explains which evidence it checks structurally, reports drift while retaining the audited pin, and makes the runner setup portable. Use the [migration guide](v0.0.2/MIGRATION.md) to convert an existing registry. A schema v1 registry can continue to use the archived v0.0.1 kit. See [the version review PR](https://github.com/vixttha/Blender-Agent/pull/9) for merge status and CI.

## v0.0.1

The initial template provides the Stack role and memory, a proposal form, a registry example and tests for the pinned-commit auditor. It remains available as a reproducible version.

## Adding a version

Add the actual kit under its version number, update this comparison and the root index, and pin the kit’s source commit in the [graph catalog](graphify/catalog.json). Include that version’s verified map and receipt. The [graph guide](graphify/README.md) explains how the public runner checks the archive.
