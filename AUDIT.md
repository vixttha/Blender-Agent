# Foundation stack audit

**Review date:** November 18, 2026 · **Application foundation:** v0.0.2 · **Evidence baseline:** [`25788c0`](https://github.com/vixttha/Blender-Agent/commit/25788c01234841693ce0605053798a39cda7ba9a)

The audit is pinned to the first application merge on `main`. [Foundation PR #1](https://github.com/vixttha/Blender-Agent/pull/1) integrated the v0.0.2 pre-alpha foundation. The audited commit identifies the merged source; a release tag or package publication is a separate event.

## Observed stack

| Component | Observed choice | Evidence and scope |
| --- | --- | --- |
| Package | Python 3.11+, setuptools; empty core dependency list; optional MCP SDK range `>=1.12,<2` | [Packaging](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/pyproject.toml) |
| Entry points | CLI and installed MCP stdio launcher call the Python core | [Architecture](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/docs/ARCHITECTURE.md) · [MCP adapter](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/src/blender_agent/mcp_server.py) |
| Host to Blender | Fixed Blender subprocess and JSON job/result boundary | [Job runner](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/src/blender_agent/jobs.py) |
| Geometry | Blender's Python runtime uses `bpy` and `bmesh` | [Worker](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/src/blender_agent/blender_worker.py) · [Blender API overview](https://docs.blender.org/api/main/info_overview.html) |
| Delivery | YAML workflows, embedded Bash where needed, TOML packaging, Markdown documentation | [CI](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/.github/workflows/ci.yml) · [Docs](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/README.md) |

The source tree contains 13 tracked Python files across product and tests. The Git tree supplies application scope and the source checks distinguish Python code from supporting files. Existing archive branches are delivery infrastructure outside this application snapshot.

## Prior application verification

- [Foundation run 44438182077](https://github.com/vixttha/Blender-Agent/actions/runs/44438182077) passed four Python jobs on Linux and Windows, two real MCP stdio jobs on Linux and Windows, and the Linux Blender 4.5.0 job. The [Python log](https://github.com/vixttha/Blender-Agent/actions/runs/44438182077/job/135272183050) records 41 tests. The [Windows MCP log](https://github.com/vixttha/Blender-Agent/actions/runs/44438182077/job/135272183469) records the installed launcher handshake, schema checks and isolation. The [Blender log](https://github.com/vixttha/Blender-Agent/actions/runs/44438182077/job/135272182580) records the real-format geometry roundtrip.
- The foundation run was triggered by the application merge on `main`. The hub checks that same commit as a separate, detached source checkout.
- The roundtrips cover sample STL, OBJ, GLB, FBX and BLEND geometry and a basic repair. Production material fidelity, UI host compatibility and Blender versions or operating systems outside the real Blender test remain unverified. The MCP checks exercise inspection. A full MCP-to-Blender operation remains an open verification item.

## Findings and decision context

1. **Python fits the required Blender interface.** Keeping both entrypoints on the same core reduces duplicate validation. The process boundary lets Blender use its own embedded Python. Geometry calls can reuse Blender instead of adding a competing implementation. [Worker](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/src/blender_agent/blender_worker.py) · [Blender API overview](https://docs.blender.org/api/main/info_overview.html)
2. **Multi-file export needs a focused check.** Blender can write an MTL file with a material-bearing OBJ. The runner promotes one file from the temporary workspace. Validate this path with a material-bearing fixture before promising material fidelity. [Output publication](https://github.com/vixttha/Blender-Agent/blob/25788c01234841693ce0605053798a39cda7ba9a/src/blender_agent/jobs.py) · [Blender OBJ documentation](https://docs.blender.org/manual/en/4.4/files/import_export/obj.html)
3. **The evidence supports scoped growth.** TypeScript has a clear possible browser role. A native helper has an engineering case only when a representative workload attributes material cost to work we control. Neither appears in the audited application inventory. See [proposals](PROPOSALS.md).

The [original pre-merge audit run](https://github.com/vixttha/Blender-Agent/actions/runs/44438395299) preserves the earlier candidate check. The merge uses the same tracked file tree.

The [registry](code-stack.json) contains the source and upstream evidence for each recorded technology. The branch [workflow](.github/workflows/code-stack.yml) rechecks the inventory and evidence links by ID. External sources remain a human research responsibility, and the application results above are from their own workflow.
