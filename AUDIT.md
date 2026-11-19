# Foundation stack audit

**Review date:** November 18, 2026 · **Application candidate:** v0.0.2 · **Evidence baseline:** [`2f621fbd`](https://github.com/vixttha/Blender-Agent/commit/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b)

The application source is the open [foundation PR #1](https://github.com/vixttha/Blender-Agent/pull/1). The default branch at [`a834da94`](https://github.com/vixttha/Blender-Agent/tree/a834da944ff6572a5db431214f941548b03a41ae) contains the title README. The source baseline is an in-review candidate.

## Observed stack

| Component | Observed choice | Evidence and scope |
| --- | --- | --- |
| Package | Python 3.11+, setuptools; empty core dependency list; optional MCP SDK range `>=1.12,<2` | [Packaging](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/pyproject.toml) |
| Entry points | CLI and installed MCP stdio launcher call the Python core | [Architecture](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md) · [MCP adapter](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/mcp_server.py) |
| Host to Blender | Fixed Blender subprocess and JSON job/result boundary | [Job runner](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/jobs.py) |
| Geometry | Blender's Python runtime uses `bpy` and `bmesh` | [Worker](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/blender_worker.py) · [Blender API overview](https://docs.blender.org/api/main/info_overview.html) |
| Delivery | YAML workflows, embedded Bash where needed, TOML packaging, Markdown documentation | [CI](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/.github/workflows/ci.yml) · [Docs](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md) |

The source tree contains 13 tracked Python files across product and tests. The Git tree supplies candidate scope and the source checks distinguish Python code from supporting files. Existing archive branches are delivery infrastructure outside this application snapshot.

## Prior application verification

- [Foundation run 44436263213](https://github.com/vixttha/Blender-Agent/actions/runs/44436263213) passed four Python jobs on Linux and Windows, two real MCP stdio jobs on Linux and Windows, and the Linux Blender 4.5.0 job. The [Python log](https://github.com/vixttha/Blender-Agent/actions/runs/44436263213/job/135265802380) records 41 tests. The [Windows MCP log](https://github.com/vixttha/Blender-Agent/actions/runs/44436263213/job/135265802296) records the installed launcher handshake, schema checks and isolation. The [Blender log](https://github.com/vixttha/Blender-Agent/actions/runs/44436263213/job/135265801967) records the real-format geometry roundtrip.
- The run identifies source head `2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b`. The Linux unit and Blender jobs tested GitHub's PR merge checkout `0d01c98`, and the Windows MCP log records a direct checkout of the candidate head. The Code Stack job reads the exact candidate SHA directly.
- The roundtrips cover sample STL, OBJ, GLB, FBX and BLEND geometry and a basic repair. Production material fidelity, UI host compatibility and Blender versions or operating systems outside the real Blender test remain unverified. The MCP checks exercise inspection. A full MCP-to-Blender operation remains an open verification item.

## Findings and decision context

1. **Python fits the required Blender interface.** Keeping both entrypoints on the same core reduces duplicate validation. The process boundary lets Blender use its own embedded Python. Geometry calls can reuse Blender instead of adding a competing implementation. [Worker](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/blender_worker.py) · [Blender API overview](https://docs.blender.org/api/main/info_overview.html)
2. **Multi-file export needs a focused check.** Blender can write an MTL file with a material-bearing OBJ. The runner promotes one file from the temporary workspace. Validate this path with a material-bearing fixture before promising material fidelity. [Output publication](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/jobs.py) · [Blender OBJ documentation](https://docs.blender.org/manual/en/4.4/files/import_export/obj.html)
3. **The evidence supports scoped growth.** TypeScript has a clear possible browser role. A native helper has an engineering case only when a representative workload attributes material cost to work we control. Neither appears in the audited application inventory. See [proposals](PROPOSALS.md).

The [registry](code-stack.json) contains the source and upstream evidence for each recorded technology. The branch [workflow](.github/workflows/code-stack.yml) rechecks the inventory and evidence links by ID. External sources remain a human research responsibility, and the application results above are from their own workflow.
