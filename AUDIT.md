# Blender-Agent Code Stack audit

**Audited release:** [Blender-Agent v0.0.2 pre-release](https://github.com/vixttha/Blender-Agent/releases/tag/v0.0.2)  
**Pinned application:** [cb945bd8531ee425615c1968612ab6503849369d](https://github.com/vixttha/Blender-Agent/commit/cb945bd8531ee425615c1968612ab6503849369d)  
**Regular review kit:** [Code Stack v0.0.3](https://github.com/vixttha/Blender-Agent/tree/8dd56cdd53897b5a78f3a59d9ca2549f1c08f885/v0.0.3) · [Settings](language-review.json) · [Graphify receipt](https://github.com/vixttha/Blender-Agent/blob/ba2ce5c3c9d07602593078d4c97f89b6cdc6643b/graphify/v0.0.3/receipt.json)

## Regular language reviews

The [hub workflow](https://github.com/vixttha/Blender-Agent/actions/workflows/code-stack.yml) uses the application branch tip available when the runner checks it out. It records the exact hub, application, release and template commits. It generates two review packages, `release` and `current`, each with `REPORT.md`, a generated schema 3 `code-stack.json`, and `receipt.json`. The current report appears in the job summary. The packages are downloadable for three days. The workflow checks the source pins and the output checksums.

Hub pushes and pull requests trigger the workflow. To refresh after application changes alone, rerun the latest successful push workflow for the current hub commit while GitHub offers the rerun. That run fetches the application branch tip again. Use the [portable command](https://github.com/vixttha/Blender-Agent/blob/8dd56cdd53897b5a78f3a59d9ca2549f1c08f885/v0.0.3/AUDIT.md) for any other source ref.

The published release is the default comparison. When there are explicit owner decisions, generate the approved schema 3 registry with the template’s approval input and record it through a hub PR as `approved-code-stack.json`. Later runs carry forward its approvals and compare the current application against that snapshot. The release package continues to be generated independently. A generated recommendation is a proposal for review.

## Published release record

The first foundation audit covered [25788c0](https://github.com/vixttha/Blender-Agent/commit/25788c01234841693ce0605053798a39cda7ba9a). The [comparison to the published release](https://github.com/vixttha/Blender-Agent/compare/25788c01234841693ce0605053798a39cda7ba9a...cb945bd8531ee425615c1968612ab6503849369d) contains README and changelog changes only. The [earlier audit](https://github.com/vixttha/Blender-Agent/blob/816f0780c1ce1e2865056a2c48f487a6e8589bb1/AUDIT.md) and its [runner receipt](https://github.com/vixttha/Blender-Agent/actions/runs/44438533595) remain available.

## Observed stack

| Layer | Choice | Source |
| --- | --- | --- |
| CLI and MCP host | Python 3.11+, common core, optional MCP installation | [Package manifest](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/pyproject.toml) · [Architecture](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/docs/ARCHITECTURE.md) |
| Blender worker | Python using Blender’s bpy and bmesh APIs | [Worker](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/src/blender_agent/blender_worker.py) |
| Process boundary | JSON job input and results | [Host](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/src/blender_agent/jobs.py) · [Worker](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/src/blender_agent/blender_worker.py) |
| Packaging, CI, documentation | TOML, YAML, embedded Bash, and Markdown | [Package](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/pyproject.toml) · [CI](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/.github/workflows/ci.yml) · [README](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/README.md) |

See the authored [release registry](code-stack.json) for role-specific evidence references and the [proposal record](PROPOSALS.md) for conditional technologies.

## Evidence and freshness

The authored release registry and legacy audit remain available with the [v0.0.2 receipt](https://github.com/vixttha/Blender-Agent/actions/runs/44444682274). The v0.0.3 review receipts support inventory and draft language recommendations. Use the application checks below for runtime behavior and compatibility.

The [application CI](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759) passed all seven jobs at the published release SHA. The [Blender 4.5 format job](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759/job/135274042289) covers a Linux format roundtrip. The [MCP Windows job](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759/job/135274041918) and [MCP Ubuntu job](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759/job/135274042347) cover launch and read-only inspection. A full MCP-triggered Blender operation and material-bearing OBJ export remain outside that evidence.

[The main snapshot at 42c1ce6](https://github.com/vixttha/Blender-Agent/commit/42c1ce618543374ed4dd5c8bcac5d437835c4e57) adds a [public-runner Blender 4.5 test through MCP](https://github.com/vixttha/Blender-Agent/actions/runs/44441784614/job/135284120753) covering create, convert, repair, and inspect. The release audit retains `cb945bd` as its source. The regular language review reports the [changes since the release](https://github.com/vixttha/Blender-Agent/compare/cb945bd8531ee425615c1968612ab6503849369d...42c1ce618543374ed4dd5c8bcac5d437835c4e57) separately from release-tag freshness.
