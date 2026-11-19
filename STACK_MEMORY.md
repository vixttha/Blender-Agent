# Stack memory · Blender-Agent

| Field | Recorded context |
| --- | --- |
| Working identity | **Stack**, Blender-Agent's programming language steward |
| Canonical repository | [Blender-Agent](https://github.com/vixttha/Blender-Agent) |
| Hub | [code-stack](https://github.com/vixttha/Blender-Agent/tree/code-stack) |
| Source baseline | [Foundation PR #1](https://github.com/vixttha/Blender-Agent/pull/1), [`2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b`](https://github.com/vixttha/Blender-Agent/commit/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b), application v0.0.2 candidate |
| Current observed implementation | Python for the app and Blender worker. JSON jobs and reports. TOML packaging. YAML CI with embedded Bash. Markdown documentation. |
| Owner direction | Establish the language hub, durable handoff, portable template, and a run-backed Blender-Agent audit. |
| Open architecture ideas | [Language proposals](PROPOSALS.md). Conditional choices require a demonstrated project need and review. |
| Validation environment | Free standard GitHub-hosted runners on the public repository. [Runner policy at the source commit](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/AGENTS.md) |
| Open evidence | Real MCP-to-Blender operation, material-bearing OBJ publication, and broader Blender/host runtime compatibility |
| Delivery cadence | Head → Worker → Validate exact SHA → Internal Auditor → Head |

## Handoff

**November 18, 2026.** First hub baseline. Python is the current implementation and the recommended foundation. TypeScript, Geometry Nodes and native helpers have conditional paths. The portable checker and fixtures come from [template v0.0.1](https://github.com/vixttha/Blender-Agent/tree/042390d63e72dc3e1fbb0c87387ea9f8d42f1d6f/v0.0.1). See the [audit](AUDIT.md) for exact source and test limits.

When revisiting, compare the target application HEAD with the registry. Update the evidence baseline and audit for a new revision. Put language adoption decisions in the proposal record and link the approval here. Keep unrelated documentation and Graphify work in their own repositories or branches.
