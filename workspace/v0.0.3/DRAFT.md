# Blender-Agent

Blender-Agent is a pre-alpha Python toolkit for inspecting 3D assets and running a small set of headless Blender operations. Use it from the command line or connect a compatible host through the optional Model Context Protocol (MCP) adapter.

**Current pre-release: v0.0.2.** The quick start installs from the published tag. [Release notes](https://github.com/vixttha/Blender-Agent/releases/tag/v0.0.2)

[Quick start](#quick-start) · [Capabilities](#capabilities) · [MCP setup](#mcp-setup) · [Testing and contributing](#testing-and-contributing)

## Quick start

Install Git and Python 3.11 or newer. The first example runs without Blender.

```sh
git clone --branch v0.0.2 --depth 1 https://github.com/vixttha/Blender-Agent.git
cd Blender-Agent
python -m venv .venv
```

Activate the virtual environment with `source .venv/bin/activate` on macOS or Linux, or `.\.venv\Scripts\Activate.ps1` in PowerShell. Then install the package and inspect a sample triangle:

```sh
python -m pip install .
blender-agent version
python -c "from pathlib import Path; p = Path('readme-demo'); p.mkdir(); (p / 'triangle.obj').write_text('v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n', encoding='utf-8')"
blender-agent --workspace readme-demo inspect triangle.obj
```

`blender-agent version` reports `0.0.2`. The inspection reports three vertices, one face, bounds from `[0, 0, 0]` to `[1, 1, 0]`, and a SHA-256 digest. The sample command expects a fresh `readme-demo` directory. To try your own asset, put it inside that workspace and pass its filename to `inspect`.

### Create, convert, and repair with Blender

The worker requires Blender 4.1 or newer. The headless smoke test uses Blender 4.5.0 on Ubuntu. Put `blender` on your command path or pass `--blender` with the executable path before the operation name.

```sh
blender-agent --workspace readme-demo create cube cube.stl --size 1
blender-agent --workspace readme-demo convert cube.stl cube.glb
blender-agent --workspace readme-demo repair cube.stl cube-repaired.stl
```

If a destination already exists, choose a new output name. Convert and repair can replace a separate output only when the CLI is given `--overwrite`. Use a dedicated workspace with trusted inputs and keep backups of important assets.

## Capabilities

| Operation | v0.0.2 scope |
| --- | --- |
| Inspect STL and OBJ | Python reports file size, SHA-256, bounds, and basic geometry counts. |
| Inspect GLB, FBX, and BLEND | Python reports file metadata only. |
| Create | Headless Blender creates a cube, UV sphere, or cylinder. |
| Convert | The Blender worker has readers and writers for STL, OBJ, GLB, FBX, and BLEND. Public CI checks STL roundtrips through OBJ, GLB, FBX, and BLEND. |
| Repair | Blender merges nearby vertices and recalculates face normals, then writes a separate output. |

The worker uses a fixed operation set and starts Blender with automatic script execution disabled. Blender runs with your account’s permissions. Use a workspace whose contents and concurrent access you control. The worker caps captured logs at 256 KiB and published output at 512 MiB. Detailed STL and OBJ inspection is limited to 128 MiB per input. Geometry counts and cleanup give you diagnostics. Printability, game-engine imports, and material or animation fidelity require checks in the destination tool. [Architecture](https://github.com/vixttha/Blender-Agent/blob/v0.0.2/docs/ARCHITECTURE.md) · [Roadmap](https://github.com/vixttha/Blender-Agent/blob/v0.0.2/docs/ROADMAP.md)

## MCP setup

Install the optional adapter in the repository’s activated environment:

```sh
python -m pip install ".[mcp]"
```

Configure your host to launch `blender-agent-mcp` over stdio. Use the executable from the virtual environment if your host has a separate command path. Set `BLENDER_AGENT_WORKSPACE` to the absolute path of an existing workspace and optionally set `BLENDER_AGENT_BLENDER` to your Blender executable.

The adapter exposes `inspect_model`, `create_primitive`, `convert_model`, and `repair_mesh`. See the validation table below for the workflows exercised on each platform. Compatibility depends on the host. [Harness configuration](https://github.com/vixttha/Blender-Agent/blob/v0.0.2/docs/HARNESS.md)

## Testing and contributing

Run the Python suite from the source checkout:

```sh
python -m unittest discover -s tests -v
```

| Source | Public GitHub Actions coverage |
| --- | --- |
| Published `v0.0.2` | Python 3.11 and 3.12 on Linux and Windows. MCP stdio startup, tool schemas, and inspection on both platforms. CLI roundtrips and mesh repair with Blender 4.5.0 on Ubuntu. [Tagged source CI](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759) · [Release quick-start check](https://github.com/vixttha/Blender-Agent/actions/runs/44438934108/job/135274667346) |
| `main` at `42c1ce6` | Adds real Blender 4.5.0 create, convert, repair, and inspect calls through MCP stdio on Ubuntu. Windows covers MCP stdio startup, tool schemas, and workspace-bounded inspection. [Main CI](https://github.com/vixttha/Blender-Agent/actions/runs/44441784614) · [Ubuntu Blender job](https://github.com/vixttha/Blender-Agent/actions/runs/44441784614/job/135284120753) · [Windows MCP job](https://github.com/vixttha/Blender-Agent/actions/runs/44441784614/job/135284121183) |

Individual MCP hosts and other Blender format combinations still need their own verification.

If you find a bug, include the source revision, OS, Python and Blender versions, file format, command, and expected and actual results. A small synthetic asset helps reproduce file-specific behavior. [GitHub Issues](https://github.com/vixttha/Blender-Agent/issues) · [Contributing](https://github.com/vixttha/Blender-Agent/blob/v0.0.2/CONTRIBUTING.md) · [Security](https://github.com/vixttha/Blender-Agent/blob/v0.0.2/SECURITY.md) · [Changelog](https://github.com/vixttha/Blender-Agent/blob/v0.0.2/CHANGELOG.md)

## License

Blender-Agent is an independent project distributed under the [MIT License](https://github.com/vixttha/Blender-Agent/blob/v0.0.2/LICENSE).
