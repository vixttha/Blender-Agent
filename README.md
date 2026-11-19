# Blender-Agent Refinement Toolkit ChatGPT Project Instructions

Use the [v0.0.2 instructions](v0.0.2/CHATGPT_PROJECT_INSTRUCTIONS.md) with [setup](v0.0.2/README.md), [acceptance checks](v0.0.2/ACCEPTANCE.md), and the [verification record](v0.0.2/VERIFICATION.md). These files live on the permanent `chatgpt-project-instructions` branch of [Blender-Agent Refinement Toolkit](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit). The [MIT license](LICENSE) covers the archive template and tooling.

## Version catalog

| Version | Status | Instructions | Verification |
| --- | --- | --- | --- |
| [v0.0.2](v0.0.2/) | Candidate | [Copy-ready instructions](v0.0.2/CHATGPT_PROJECT_INSTRUCTIONS.md) | [Receipt and settings status](v0.0.2/VERIFICATION.md) |
| [v0.0.1](v0.0.1/) | Candidate | [Copy-ready instructions](v0.0.1/CHATGPT_PROJECT_INSTRUCTIONS.md) | [Historical verification](v0.0.1/VERIFICATION.md) |

**Archivewright — Blender-Agent Refinement Toolkit Instructions Steward** curates this archive. Head selects one scoped feature, Worker implements it using existing architecture, Validate runs exact-commit checks on free public GitHub-hosted runners, Internal Auditor verifies findings and repairs demonstrated gaps, and Head records maintainer approval before integrating once and archiving the evidence. Work can continue across successive features.

Each version has its own folder. For a new candidate, update the version catalog and [lineage map](graphify/versions.json). Pin accepted folders to immutable source commits in the lineage manifest. The historical v0.0.1 folder already has a preservation pin. Use a new version for changes to any frozen folder. Record public-runner evidence against the exact tested SHA. Keep saved settings and fresh-chat evidence private where it contains project or account details.

[Archive validation workflow](.github/workflows/instructions-archive.yml) · [Graphify guide](graphify/README.md) · [Application engineering branch](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/main)
