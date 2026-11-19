# Blender-Agent

**Open, harness-neutral tools for Blender and 3D assets.**

Blender-Agent v0.0.2 is a pre-alpha foundation for CLI and Model Context Protocol (MCP) workflows. It is not yet a fully autonomous 3D artist. v0.0.1 was the initial foundation candidate; this version addresses its six audit findings. Neither candidate is a production release.

## Capability status

| Capability | Status | Important limit |
| --- | --- | --- |
| STL / OBJ inspection | Implemented | Bounded, read-only structural metrics; not printability certification |
| GLB, FBX, BLEND inspection | Metadata only | File hash/size; detailed inspection requires Blender |
| Create primitives | Blender required | Cube, UV sphere, cylinder |
| Convert assets | Blender required | STL, OBJ, GLB, FBX, BLEND |
| Repair basic meshes | Blender required | Weld nearby vertices and recalculate normals on a copy |
| CLI | Implemented | Harnesses capable of invoking authorized commands |
| MCP | Optional | Tested using a real stdio MCP client; host-specific support not guaranteed |
| Sculpting, worlds, rigs, animation, game and printing validation | Planned | Not shipped |
| AI model generation, persistent memory, dynamic skill execution | Planned | Not shipped |

## Quick start

Python 3.11+ is required. Blender 4.1+ is required for operations involving Blender; v0.0.2 public CI tests Blender 4.5.0 on Linux. The Python inspector works without Blender.

Create the workspace and its input/output directories before running these commands.

~~~sh
python -m pip install -e .
blender-agent version
blender-agent skills
blender-agent --workspace ./workspace inspect input/model.stl
blender-agent --workspace ./workspace create cube output/cube.stl --size 1
blender-agent --workspace ./workspace convert input/model.stl output/model.glb
blender-agent --workspace ./workspace repair input/model.stl output/cleaned.stl
~~~

Paths must remain in the workspace. The source is never modified in place, and outputs cannot overwrite existing files by default. Use --blender /path/to/blender when Blender is not on PATH.

For compatible MCP hosts:

~~~sh
python -m pip install -e ".[mcp]"
blender-agent-mcp
~~~

Set BLENDER_AGENT_WORKSPACE to an absolute workspace directory; optionally set BLENDER_AGENT_BLENDER. See [harness integration](docs/HARNESS.md).

## Security and resource limits

- Workspace paths are checked with resolved symlinks. This is **not** a security sandbox; protect the workspace from hostile concurrent filesystem mutations.
- Output publication without overwrite uses atomic no-clobber hard-link creation, preventing competing writers from silently overwriting a destination.
- Creating or modifying existing files still requires explicit authorization. MCP tools have no overwrite option.
- Fixed Blender worker; factory startup and automatic scripting disabled; no model-generated Python execution.
- Bounded Blender execution time (1–900 seconds), captured logs (256 KiB), source size (512 MiB), and generated output (512 MiB).
- Detailed structural STL/OBJ inspection has a 128 MiB input limit and rejects malformed references/coordinates.
- A structural summary does not certify printability, watertightness, visual quality, or game readiness.

## Architecture and roadmap

See [architecture](docs/ARCHITECTURE.md), [specialist skill policy](docs/SKILL_POLICY.md), [harness integration](docs/HARNESS.md), and [capability roadmap](docs/ROADMAP.md). Four starter skill documents live under [skills](skills).

Local checks:

~~~sh
python -m pip install -e .
python -m compileall -q src
python -m unittest discover -s tests -p "test_*.py" -v
~~~

MCP integration tests require the optional extra:

~~~sh
python -m pip install -e ".[mcp]"
python tests/test_mcp_smoke.py
~~~

Public CI uses free standard GitHub-hosted Linux and Windows runners and a separate Blender 4.5 smoke job. The Blender 4.5 check includes real roundtrips for supported formats and geometry bounds; other Blender versions and printers/game engines are not certified.

See [contributing](CONTRIBUTING.md), [security](SECURITY.md), and [changelog](CHANGELOG.md).

## License

MIT; see [LICENSE](LICENSE).

An independent community project, not affiliated with or endorsed by the Blender Foundation.
