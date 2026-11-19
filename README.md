# Graphify HQ Template

This is the permanent Blender-Agent branch for maintaining the reusable Graphify
HQ template. Use `graphify-hq-template` as the base for template pull requests.
The [Blender-Agent release graphs](https://github.com/vixttha/Blender-Agent/tree/graphify-hq)
have their own archive.

[Latest kit: v0.0.8](versions/v0.0.8/) · [Version catalog](graphify/catalog.json)

| Version | Graphify | Self-graph | Verification receipt |
| --- | --- | --- | --- |
| v0.0.8 | 0.9.109 | [Graph](graphify/v0.0.8/graph.json) | [Receipt](graphify/v0.0.8/receipt.json) |

The kit maps its own implementation, documentation, changes, test definitions,
and CI files. The [archive workflow](.github/workflows/graphify-hq-template.yml)
runs the test suite, rebuilds the graph and receipt from their pinned source
commit, and queries the rebuilt graph through Graphify MCP.

Use a new version folder when changing a published kit. Keep each archived
graph, receipt, and source pin together in the version catalog.
