# v0.0.1 — repository verification evidence

This file archives **observed** public GitHub Actions evidence for the candidate instructions. It is not an approval, a Graphify MCP receipt, a ChatGPT.com settings change, or proof that Blender itself ran.

## Verified public-runner pass

- Repository: https://github.com/vixttha/Blender-Agent
- Branch: `chatgpt-project-instructions`
- Exact tested commit: [`f87e1a18cf7f5efc393e503b398d97e5850ae5ac`](https://github.com/vixttha/Blender-Agent/commit/f87e1a18cf7f5efc393e503b398d97e5850ae5ac)
- Run: https://github.com/vixttha/Blender-Agent/actions/runs/44433809322
- Job: `validate / public Ubuntu / exact SHA` — **success** (6 of 6 steps including job setup/completion)
- Policy: `PUBLIC_RUNNER_POLICY=PASS` with `RUNNER_KIND=github-hosted`
- Exact checkout: `CHECKED_OUT_SHA=f87e1a18cf7f5efc393e503b398d97e5850ae5ac`
- Validator: `ARCHIVE_VALIDATION=PASS`, `EXACT_SHA=f87e1a18cf7f5efc393e503b398d97e5850ae5ac`
- Source graph SHA-256: `4c2750a87f9bd5fe326b10f272b6fe56e2a753864cb238ff0a546ae3404e10da`
- Graph topology: 3 nodes / 2 links
- Runner: standard GitHub-hosted Ubuntu; no marketplace actions, paid or self-hosted runners.

## Diagnosed failure and repair

The initial candidate [`421f899`](https://github.com/vixttha/Blender-Agent/commit/421f8990626c7f2a690195e25f81a9020e7ffde5) produced [failed workflow run 44433660949](https://github.com/vixttha/Blender-Agent/actions/runs/44433660949) with no job scheduled. A workflow configuration repair moved the runner context into step-level environments. The corrected candidate was then checked successfully as recorded above. The failed attempt remains in GitHub history.

## Independent checks still unverified

- **Graphify MCP:** No Graphify tool invocation or MCP-generated graph has been verified. `graphify/versions.json` is a tracked handoff map, verified only for internal consistency.
- **ChatGPT.com Project settings:** Not changed or verified by GitHub CI. Installation, settings read-back, and fresh-chat smoke need separate actual evidence.
- **Blender runtime:** Not exercised. This is a documentation/CI archive, not an application feature test.
- **Owner approval / merge:** No acceptance or merge to `main` has been recorded.

Use a new exact-SHA run for any later change and do not present this pass as validation of an untested commit.
