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

## Execution modes

The verifier selects its mode from the execution context.

| Context | Runner and behavior |
| --- | --- |
| Local checkout | Run `python tools/verify_archive.py` from the template root with CPython 3.12 on Linux x86-64. Archive checks require the pinned Git history and use the historical repository identity from the catalog. |
| Public GitHub repository | Standard GitHub-hosted Ubuntu runs verification automatically on template-branch pushes and pull requests. |
| Private or internal GitHub repository | A trusted template-branch push runs on a self-hosted Linux x64 runner labeled `graphify-hq` when repository variable `GRAPHIFY_PRIVATE_SELF_HOSTED` is `true`. Configure that runner and restrict who can push to the branch before enabling the variable. |

Private pull requests do not execute on the self-hosted runner. GitHub Actions uses
the event payload to identify repository visibility. Unknown visibility stops verification.
Candidate graph and receipt payloads are emitted in public Actions logs only. For a
local candidate, use `--candidate-output PATH` to retain both files and
`--repository OWNER/REPO` if the checkout has no GitHub origin.

### Candidate publication recovery

On the supported Linux filesystem, the candidate takes a process-scoped lock
on the output directory and stages both evidence files before replacement.
A publish or `--check` on that directory automatically rolls back an interrupted
replacement before proceeding. Use the CLI to recover the pair before reading
it after an interrupted write.
