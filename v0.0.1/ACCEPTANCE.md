# v0.0.1 acceptance matrix

This matrix separates **repository CI**, **Graphify MCP**, and **actual ChatGPT.com behavior**. Do not merge the categories into a single PASS.

| Check | Method | Acceptance |
| --- | --- | --- |
| Archive layout | Public GitHub Actions `instructions-archive.yml` | Branch README, version README, copy-ready text, matrix, and Graphify map exist |
| Sequence | CI content and dependency assertions | Head → Worker → Validate → Internal Auditor → Head, one active Worker |
| Scope quality | Source inspection | Acceptance criteria, architecture reuse, demonstrated-only repairs, no artificial feature freezes |
| Runner and cost | CI policy and workflow review | Public visibility; standard GitHub-hosted runner; no paid/self-hosted/local CI or required credentials |
| Exact evidence | Actions job log and summary | Actual checkout SHA equals `github.sha`; report run URL and emitted receipt |
| Graphify handoff | CI graph consistency | Nodes/links agree with version folders, no false MCP verification claim |
| Graphify MCP | Actual Graphify invocation when available | Explicit verified source SHA and receipt, or mark unavailable, never fake completion |
| ChatGPT.com settings | Open saved Project settings after installation | Text is installed and matches this candidate; owner-controlled/manual unless supported |
| Fresh-chat smoke | New project chat after installation | Reads real GitHub main SHA, proposes one scoped feature, no unapproved writes |
| Merge gate | Maintainer review | Explicit approval before merging; do not use CI PASS as merge authorization |

## Receipt format

Each automated check must report the **tested commit SHA**, run URL, workflow/event, runner, status, and artifact graph checksum; otherwise label it **unverified**. If re-run after any change, preserve the old failure and attach the new run to the **new** SHA. Do not claim a real Blender runtime test if only markdown/schema checks ran.

## Release decision

`v0.0.1` remains **candidate** until the saved-settings/fresh-chat checks and maintainer acceptance have occurred. A green archive workflow validates the *files*, not an installation or release. No PR or merge to `main` is implied.
