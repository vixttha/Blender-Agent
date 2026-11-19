# Blender-Agent — ChatGPT Project Instructions Archive

**Permanent workspace:** `chatgpt-project-instructions`  
**Repository:** https://github.com/vixttha/Blender-Agent  
**Scope:** versioned, reusable ChatGPT.com project instructions; not the application's product README.

This branch is the long-lived instructions library. It is intentionally separate from `main`, so instruction revisions do not interrupt Blender-Agent feature delivery. Start with the [v0.0.1 instructions](v0.0.1/CHATGPT_PROJECT_INSTRUCTIONS.md), then see its [release notes and setup](v0.0.1/README.md) and [acceptance criteria](v0.0.1/ACCEPTANCE.md).

## Steward identity

**Archivewright — Blender-Agent Instructions Steward** is a working role for curating, validating, and archiving these instructions. The name is not an authenticated person, independent auditor, new coordinator, or source of merge authority. Head, Worker, Validate, and Internal Auditor are sequential functions in one lane.

## Version catalog

| Version | Status | Instructions | Acceptance |
| --- | --- | --- | --- |
| [v0.0.1](v0.0.1/) | Candidate — installation and fresh-chat smoke unverified | [Copy-ready instructions](v0.0.1/CHATGPT_PROJECT_INSTRUCTIONS.md) | [Checklist](v0.0.1/ACCEPTANCE.md) |

Every version has its own folder. Preserve accepted versions immutably; revise a new version folder instead of silently overwriting an accepted one. A candidate is not accepted merely because CI succeeds. `main` stays untouched until a separate, explicitly approved integration is required.

## One-lane delivery loop

**Head (select one scoped feature) → Worker (implement by reusing architecture) → Validate (public GitHub-hosted runner, exact SHA) → Internal Auditor (verify and repair only demonstrated gaps) → Head (request approval, integrate once, archive, move forward).**

These are delivery controls, not restrictions on overall ambition. The project can complete many features in succession. Do not convert optional checks, unavailable plugins, or speculative risks into arbitrary blocks.

## Free public-runner validation

This branch contains [self-contained Actions CI](.github/workflows/instructions-archive.yml). It uses a standard `ubuntu-latest` GitHub-hosted runner, the public repository, Python's standard library, read-only permissions, and no marketplace actions, paid runners, self-hosted workers, credentials, or outside services.

The workflow validates archive structure, owner-independent wording, manifest links, scoped workflow rules, and the Graphify handoff map. It prints a SHA-bound verification receipt and graph summary to the GitHub Actions log and job summary. See [Graphify handoff](graphify/README.md).

**Important:** CI evidence is separate from saving text in ChatGPT Project settings. A fresh-chat smoke test and any Graphify MCP operation must be recorded as independently verified events, never assumed from a file or passing workflow.

## Continue the archive

1. Create `v0.0.2/` (or the next version) with instructions, README, and acceptance criteria.
2. Add its node and links to `graphify/versions.json`; preserve existing accepted nodes.
3. Run the branch's public-runner workflow on its exact candidate commit, audit outcomes, and record the run URL and SHA.
4. Seek explicit acceptance for the new version, update the catalog/status, and preserve history.

**Public hygiene:** No personal information, private links, tokens, or names of individual creators appear in this archive.
