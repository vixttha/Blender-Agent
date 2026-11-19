# Stack memory · Blender-Agent

| Field | Recorded context |
| --- | --- |
| Working identity | **Stack**, Blender-Agent's programming language steward |
| Canonical repository | [Blender-Agent](https://github.com/vixttha/Blender-Agent) |
| Hub | [code-stack](https://github.com/vixttha/Blender-Agent/tree/code-stack) |
| Source baseline | [Published Blender-Agent v0.0.2](https://github.com/vixttha/Blender-Agent/releases/tag/v0.0.2), [cb945bd8531ee425615c1968612ab6503849369d](https://github.com/vixttha/Blender-Agent/commit/cb945bd8531ee425615c1968612ab6503849369d) |
| Current observed implementation | Python for the app and Blender worker. JSON jobs and reports. TOML packaging. YAML CI with embedded Bash. Markdown documentation. |
| Owner direction | Establish the language hub, durable handoff, portable template, and a run-backed Blender-Agent audit. |
| Open architecture ideas | [Language proposals](PROPOSALS.md). Conditional choices require a demonstrated project need and review. |
| Validation environment | Free standard GitHub-hosted runners on the public repository. [Runner policy at the source commit](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/AGENTS.md) |
| Open evidence | Real MCP-to-Blender operation on the published release, material-bearing OBJ publication, and broader Blender/host runtime compatibility |
| Delivery cadence | Head → Worker → Validate exact SHA → Internal Auditor → Head |

## Handoff

**November 18, 2026.** First hub baseline, updated to the merged foundation. Python is the current implementation and the recommended foundation. TypeScript, Geometry Nodes and native helpers have conditional paths. The portable checker and fixtures come from [template v0.0.1](https://github.com/vixttha/Blender-Agent/tree/042390d63e72dc3e1fbb0c87387ea9f8d42f1d6f/v0.0.1). See the [audit](AUDIT.md) for exact source and test limits.

When revisiting, compare the target application HEAD with the registry. Update the evidence baseline and audit for a new revision. Put language adoption decisions in the proposal record and link the approval here. Keep unrelated documentation and Graphify work in their own repositories or branches.

**November 18, 2026.** Migrated the project registry to Code Stack schema v2 and pinned the published application. [Current audit](AUDIT.md) links the historical foundation and the runner receipts. Freshness is compared to fetched main and release refs at each hub run.
