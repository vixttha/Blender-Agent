# Blender-Agent Code Stack audit

**Audited release:** [Blender-Agent v0.0.2 pre-release](https://github.com/vixttha/Blender-Agent/releases/tag/v0.0.2)  
**Pinned application:** [cb945bd8531ee425615c1968612ab6503849369d](https://github.com/vixttha/Blender-Agent/commit/cb945bd8531ee425615c1968612ab6503849369d)  
**Template kit:** [Code Stack v0.0.2 · 53418d6](https://github.com/vixttha/Blender-Agent/tree/53418d6c0fdfc821dc1778c4325e8a3082f7d38c/v0.0.2)

The first foundation audit covered [25788c0](https://github.com/vixttha/Blender-Agent/commit/25788c01234841693ce0605053798a39cda7ba9a). The [comparison to the published release](https://github.com/vixttha/Blender-Agent/compare/25788c01234841693ce0605053798a39cda7ba9a...cb945bd8531ee425615c1968612ab6503849369d) contains README and changelog changes only. The [earlier audit](https://github.com/vixttha/Blender-Agent/blob/816f0780c1ce1e2865056a2c48f487a6e8589bb1/AUDIT.md) and its [runner receipt](https://github.com/vixttha/Blender-Agent/actions/runs/44438533595) remain available.

## Observed stack

| Layer | Choice | Source |
| --- | --- | --- |
| CLI and MCP host | Python 3.11+, common core, optional MCP installation | [Package manifest](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/pyproject.toml) · [Architecture](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/docs/ARCHITECTURE.md) |
| Blender worker | Python using Blender’s bpy and bmesh APIs | [Worker](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/src/blender_agent/blender_worker.py) |
| Process boundary | JSON job input and results | [Host](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/src/blender_agent/jobs.py) · [Worker](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/src/blender_agent/blender_worker.py) |
| Packaging, CI, documentation | TOML, YAML, embedded Bash, and Markdown | [Package](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/pyproject.toml) · [CI](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/.github/workflows/ci.yml) · [README](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/README.md) |

See [registry](code-stack.json) for role-specific evidence references and the [proposal record](PROPOSALS.md) for conditional technologies.

## Evidence and freshness

The [Code Stack workflow](https://github.com/vixttha/Blender-Agent/actions/workflows/code-stack.yml) emits a JSON receipt in the job summary and the audit log. It records the target SHA, template SHA, checkout and run identifiers, inventory counts, and separate comparisons to fetched main and release refs. Evidence checks cover structure, tracked paths, declared source binding, and configured literal fragments. Recorded human review and application runtime checks have their own evidence.

The [application CI](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759) passed all seven jobs at the published release SHA. The [Blender 4.5 format job](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759/job/135274042289) covers a Linux format roundtrip. The [MCP Windows job](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759/job/135274041918) and [MCP Ubuntu job](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759/job/135274042347) cover launch and read-only inspection. A full MCP-triggered Blender operation and material-bearing OBJ export remain outside that evidence.
