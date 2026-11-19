# Blender-Agent

Inspect, create, convert, and repair 3D assets from a terminal or an MCP host. Blender-Agent is an independent Python toolkit that runs locally. Inspection runs without Blender. Creation, conversion, and repair use headless Blender.

**Documentation preview for v0.0.3.** The commands below use the published v0.0.2 pre-release. [Get v0.0.2](https://github.com/vixttha/Blender-Agent/releases/tag/v0.0.2) · [Follow v0.0.3](https://github.com/vixttha/Blender-Agent/pull/30)

[Quick start](#quick-start) · [Capabilities](#capabilities) · [MCP setup](#mcp-setup) · [Compatibility](#compatibility) · [Troubleshooting](#troubleshooting)

![Wireframe cube beside a solid orange cube on a neutral background](assets/wireframe-cube.webp)

*Concept illustration of mesh geometry. The toolkit operates through CLI and MCP.*

## Quick start

Install Git and Python 3.11 or newer.

```sh
git clone --branch v0.0.2 --single-branch https://github.com/vixttha/Blender-Agent.git
cd Blender-Agent
python -m venv .venv
```

Activate the environment on macOS or Linux:

```sh
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the package and create a directory for the demo:

```sh
python -m pip install .
blender-agent version
mkdir readme-demo
```

Save this sample as `readme-demo/triangle.obj`:

```obj
v 0 0 0
v 1 0 0
v 0 1 0
f 1 2 3
```

```sh
blender-agent --workspace readme-demo inspect triangle.obj
```

The version command reports `0.0.2`. The inspection reports **3 vertices, 1 face**, bounds from `[0, 0, 0]` to `[1, 1, 0]`, and a SHA-256 digest.

![A solid triangle beside a wireframe triangle with three marked vertices](assets/triangle-inspection.webp)

*Concept illustration for the sample. The CLI reports the actual values as JSON.*

### Run a headless Blender job

Install Blender 4.1 or newer. The verified Blender runner uses **4.5.0 on Ubuntu**. Put the executable on your command path or pass `--blender` with its path before the operation.

```sh
blender-agent --workspace readme-demo create cube cube.stl
blender-agent --workspace readme-demo convert cube.stl cube.glb
blender-agent --workspace readme-demo repair cube.stl repaired.stl
```

The input stays in place. Choose fresh output names when repeating the Blender commands. The CLI can explicitly replace a separate destination for convert and repair with `--overwrite`. MCP keeps overwrite disabled.

## Capabilities

| Operation | Result in v0.0.2 | Needs Blender |
| --- | --- | --- |
| Inspect STL or OBJ | Size, digest, bounds, and basic mesh counts | No |
| Inspect GLB, FBX, or BLEND | File metadata and digest | No |
| Create | Cube, UV sphere, or cylinder | Yes |
| Convert | Read and write STL, OBJ, GLB, FBX, and BLEND | Yes |
| Repair | Weld nearby vertices and recalculate face normals in a separate output | Yes |

Geometry checks establish counts and bounds for the tested samples. Material and animation fidelity, printability, and game-engine readiness require validation in the destination tool. [Architecture](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/docs/ARCHITECTURE.md) · [Roadmap](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/docs/ROADMAP.md)

## MCP setup

Install the optional adapter in the same environment:

```sh
python -m pip install ".[mcp]"
```

Example stdio host configuration. Replace the workspace placeholder with an existing absolute path. If your host cannot resolve `blender-agent-mcp`, use the full path to the executable in your virtual environment.

```json
{
  "command": "blender-agent-mcp",
  "env": {
    "BLENDER_AGENT_WORKSPACE": "/absolute/path/to/workspace",
    "BLENDER_AGENT_BLENDER": "blender"
  }
}
```

The installed MCP launcher exposes `inspect_model`, `create_primitive`, `convert_model`, and `repair_mesh`. The release checks cover the real stdio handshake, tool schemas, and workspace-bounded inspection. [Release harness guide](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/docs/HARNESS.md)

## Compatibility

| Area | Evidence |
| --- | --- |
| Python CLI | Python 3.11 and 3.12 on Linux and Windows |
| Headless Blender | Blender 4.5.0 on Ubuntu. Cube creation, STL roundtrips through OBJ, GLB, FBX and BLEND, and mesh repair |
| MCP stdio in v0.0.2 | Launcher, schemas, and workspace-bounded inspection on Linux and Windows. [Tagged source CI](https://github.com/vixttha/Blender-Agent/actions/runs/44438741759) · [Release quick-start check](https://github.com/vixttha/Blender-Agent/actions/runs/44438934108/job/135274667346) |
| MCP on main at `42c1ce6` | All four tool calls with Blender 4.5.0 on Ubuntu, including repair and source preservation. Windows exercises launcher startup, schemas, and workspace-bounded inspection. [Main CI](https://github.com/vixttha/Blender-Agent/actions/runs/44441784614) · [Ubuntu Blender job](https://github.com/vixttha/Blender-Agent/actions/runs/44441784614/job/135284120753) · [Windows stdio job](https://github.com/vixttha/Blender-Agent/actions/runs/44441784614/job/135284121183) |

Named host integrations, macOS runner coverage, and universal format fidelity require their own checks.

## Troubleshooting

- **Blender cannot be found.** Confirm the executable path and pass `--blender` for the CLI or `BLENDER_AGENT_BLENDER` in your host environment.
- **MCP starts in the wrong directory.** Set `BLENDER_AGENT_WORKSPACE` explicitly to an existing absolute path.
- **The destination already exists or its parent is missing.** Use a fresh output inside the workspace and create its parent directory before running the job.
- **Inspect rejects a large STL or OBJ.** Detailed inspection is capped at 128 MiB per input. Blender jobs cap the source and published output at 512 MiB each, with a default timeout of 180 seconds.
- **The format opens but the result looks different.** Check materials, textures, rigging, and animation in the target tool. The roundtrip checks use a geometric cube fixture.

Use a trusted workspace whose files and concurrent writers you control. The worker disables Blender auto-execution. Blender still runs with your account permissions. [Security and reporting](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/SECURITY.md)

## Project links

[Changelog](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/CHANGELOG.md) · [Contributing](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/CONTRIBUTING.md) · [Issues](https://github.com/vixttha/Blender-Agent/issues) · [Specialist skill guides](https://github.com/vixttha/Blender-Agent/tree/cb945bd8531ee425615c1968612ab6503849369d/skills) · [Release documentation graph](https://github.com/vixttha/Blender-Agent/blob/5526238af9b510092db336d01b26a42c1ef82548/versions/v0.0.2/README.md) · [MIT License](https://github.com/vixttha/Blender-Agent/blob/cb945bd8531ee425615c1968612ab6503849369d/LICENSE)
