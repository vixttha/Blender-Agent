# Harness integration

The same core functions back the CLI and optional MCP stdio server. A compatible harness must have an authorized runtime and workspace access. No standalone ChatGPT conversation can operate a user's desktop Blender unless a suitable tool integration exists.

## Command-line bridge

~~~sh
python -m pip install -e .
blender-agent --workspace ./workspace inspect input/mesh.stl
blender-agent --workspace ./workspace create cube output/cube.stl
~~~

## MCP stdio bridge

~~~sh
python -m pip install -e ".[mcp]"
~~~

A generic host configuration (adapt to the host's schema):

~~~json
{
  "command": "blender-agent-mcp",
  "env": {
    "BLENDER_AGENT_WORKSPACE": "/absolute/path/to/workspace",
    "BLENDER_AGENT_BLENDER": "blender"
  }
}
~~~

The adapter exposes inspect_model, create_primitive, convert_model, and repair_mesh. It does not expose arbitrary code execution, overwrite parameters, AI image generation, memory, or autonomous task scheduling.

MCP startup requires an existing workspace configured by `BLENDER_AGENT_WORKSPACE` or an explicit CLI flag. With `blender-agent --workspace DIR --blender PATH --timeout SECONDS mcp`, the flags take precedence over the environment. The default Blender timeout is 180 seconds, and the supported range is 1 to 900 seconds.

Each MCP server runs one Blender job at a time while it continues to respond to inspection and protocol requests. The Blender timeout starts when the job runs.

Cancelling a queued request prevents it from publishing. An active Blender process may run until it finishes or reaches its timeout. The worker checks cancellation immediately before publication, which is the commit point. A cancellation received after that check lets publication finish, including any OBJ material-file update. The worker holds its slot until staging is cleaned up.

The optional dependency supports the MCP SDK v1 API range `mcp>=1.12,<2`. Public CI on Linux and Windows starts the installed `blender-agent-mcp` command from a separate working directory, initializes a real stdio session, checks each tool's input schema, and verifies workspace isolation and read-only inspection. Individual MCP hosts may require different launch configuration.

The Ubuntu jobs also run all four tools over MCP stdio with Blender 4.1.0 and 4.5.0. They check an STL → GLB → STL cube roundtrip, verify that repair welds a split edge, and confirm that in-place edits and overwrites are rejected while the existing files retain their original bytes.

| Public check | Configuration | Coverage |
| --- | --- | --- |
| Python tests | Python 3.11 and 3.12 on Ubuntu and Windows | Unit and negative-path tests |
| MCP stdio | Python 3.12 and MCP SDK 1.30.0 on Ubuntu and Windows | Built wheel, installed launchers, discovery, configuration, and inspection |
| Blender workflow | Python 3.12, MCP SDK 1.30.0, and Blender 4.1.0 and 4.5.0 on Ubuntu 24.04 | CLI roundtrips and built-wheel MCP jobs with real Blender |

CI records the interpreter patch version, platform, and installed MCP dependencies. The public MCP extra still declares the SDK v1 API range. Blender 4.1 is the worker's minimum version check. Other Blender versions, Blender execution on Windows or macOS, and named desktop MCP hosts need separate verification. Default output publication requires hard-link support on the workspace filesystem.

OBJ exports publish the matching MTL beside the OBJ and return its path in `material_library`. Keep both files together when moving the asset. External texture images remain separate. MCP and default CLI calls protect both destination names. Explicit CLI `--overwrite` applies to both output files while protecting the source model and its material libraries.

OBJ publication uses a small hidden lock file and a temporary recovery journal in the output directory. After an interruption between the MTL and OBJ writes, retry the same command with the same overwrite setting. Blender-Agent recovers its own incomplete publication when it can verify the files. If a destination changed independently, it leaves the files and journal in place for manual recovery. A hard interruption can leave a hidden staging directory.

When saving a loaded Blender project as a new BLEND file, Blender-Agent anchors relative external references to the original project before saving. The resulting project uses absolute references to those resources, so the files must remain accessible at those paths. The save leaves the source project and external files intact.

Repairs process each shared editable mesh datablock once and report that count in `geometry.repaired_mesh_datablocks`. Repair rejects a project that requires editing a read-only mesh datablock.

## Trust and limits

- Users configure the allowed workspace; keep it away from hostile or untrusted concurrent filesystem writers.
- Source files are preserved; existing outputs are not overwritten by MCP.
- Blender 4.1+ is required for 3D operations; Blender 4.5 is exercised in CI.
- Inputs and output are capped in size and errors/streamed logs are bounded.
- This is not a remote server or OS sandbox, and cannot execute with permissions a hosting harness does not grant.
