# Blender-Agent

**Open, harness-neutral tools for Blender and 3D assets.**

Blender-Agent v0.0.1 is a usable pre-alpha foundation for command-line and Model Context Protocol (MCP) workflows. It is not yet a fully autonomous 3D artist or production platform.

## Capability status

| Capability | Status | Important limit |
| --- | --- | --- |
| Inspect STL and OBJ | Implemented | Basic counts, bounds, bytes and SHA-256; not printability certification |
| Inspect GLB, FBX and BLEND | Metadata only | Detailed inspection requires Blender |
| Create primitives | Blender required | Cube, UV sphere and cylinder |
| Convert assets | Blender required | STL, OBJ, GLB, FBX and BLEND |
| Repair basic mesh problems | Blender required | Merge nearby vertices and recalculate normals on a copy |
| CLI | Implemented | Usable by any harness able to invoke a command |
| MCP | Optional | Stdio tools; MCP Python SDK v1 adapter |
| Sculpting, worlds, rigs, animation, game and print validation | Planned | Not shipped |
| AI 3D generation, memory and generated skills | Planned | Not shipped |

## Quick start

Python 3.11+ is required. Blender operations need Blender 4.1+ installed in the environment where commands execute. The Python inspector works without Blender.

~~~sh
python -m pip install -e .
blender-agent version
blender-agent skills
blender-agent --workspace ./workspace inspect input/model.stl
blender-agent --workspace ./workspace create cube output/cube.stl --size 1
blender-agent --workspace ./workspace convert input/model.stl output/model.glb
blender-agent --workspace ./workspace repair input/model.stl output/cleaned.stl
~~~

Create the workspace and its input/output directories beforehand. Paths must stay within the workspace; source files cannot be overwritten. For a custom Blender location, pass --blender /path/to/blender.

For MCP-capable harnesses:

~~~sh
python -m pip install -e ".[mcp]"
blender-agent-mcp
~~~

Set BLENDER_AGENT_WORKSPACE to an absolute workspace directory and optionally BLENDER_AGENT_BLENDER to the executable. See [harness integration](docs/HARNESS.md).

## Quality and safety

- Keep source files unchanged by default; run jobs through a fixed, static Blender worker.
- Reject paths that escape the configured workspace, including symlink traversal.
- Disable automatic execution in the Blender subprocess; never run arbitrary model-authored Python.
- Write new artifacts to temporary locations and promote them only after successful execution and basic output checks.
- Validate target requirements separately. Structural counts do not prove printability, game readiness or visual quality.
- Do not auto-promote generated skills without review and repeatable tests.

## Architecture, skills and development

Read [architecture](docs/ARCHITECTURE.md), [skill policy](docs/SKILL_POLICY.md), [harness integration](docs/HARNESS.md), and [roadmap](docs/ROADMAP.md). Current specialist manifests are under [skills](skills).

Unit checks:

~~~sh
python -m pip install -e .
python -m compileall -q src
python -m unittest discover -s tests -v
~~~

The public CI workflow tests pure Python on GitHub-hosted Linux and Windows runners. Real Blender integration and cross-harness acceptance are **separate, currently unverified gates**.

See [contributing](CONTRIBUTING.md), [security](SECURITY.md), and [changelog](CHANGELOG.md).

## License

MIT; see [LICENSE](LICENSE).

An independent project; not affiliated with or endorsed by the Blender Foundation.
