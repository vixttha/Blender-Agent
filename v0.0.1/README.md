# v0.0.1 — First ChatGPT Project Instructions candidate

**Status:** candidate; repository validation and actual ChatGPT.com installation are separate.  
**Repository:** https://github.com/vixttha/Blender-Agent  
**Archive branch:** `chatgpt-project-instructions`  
**Working steward:** Archivewright — Instructions Steward.

## Contents

- [CHATGPT_PROJECT_INSTRUCTIONS.md](CHATGPT_PROJECT_INSTRUCTIONS.md) — copy-ready instructions for the Blender-Agent ChatGPT.com Project.
- [ACCEPTANCE.md](ACCEPTANCE.md) — evidence checklist and fresh-chat smoke tests.
- [../graphify/versions.json](../graphify/versions.json) — version lineage and graph handoff.

## Install / trial

In the **Blender-Agent ChatGPT.com Project**, open its settings and paste the contents of `CHATGPT_PROJECT_INSTRUCTIONS.md` into Project instructions. Save the settings. Then start a **fresh project chat** and ask: "Inspect the live Blender-Agent main SHA, choose the next scoped feature, and explain which zero-cost public GitHub-hosted checks you would run. Do not write or merge yet." Verify the answer against the repo and [ACCEPTANCE.md](ACCEPTANCE.md).

The repository connection is not the same as the Project settings control: adding this file to GitHub does **not** automatically install it in ChatGPT.com. Record any installation or smoke test only after it actually happens.

## First-version decisions

- One lane: Head → Worker → Validate → Internal Auditor → Head.
- One active Worker, clear criteria, reuse existing architecture, only confirmed repairs.
- Free standard GitHub-hosted **public** runners and exact-SHA receipts.
- Graphify when actually connected; source map always available in branch.
- Head requests explicit maintainer approval before merge or release.
- Keep project completion flexible: no artificial feature freezes or paid dependencies.

Supersede through a new `vX.Y.Z/` folder instead of overwriting an accepted archive.
