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

The optional dependency supports the MCP SDK v1 API range `mcp>=1.12,<2`. Public CI on Linux and Windows starts the installed `blender-agent-mcp` command from a separate working directory, initializes a real stdio session, checks each tool's input schema, and verifies workspace isolation and read-only inspection. Individual MCP hosts may require different launch configuration.

The Ubuntu job also runs all four tools over MCP stdio with Blender 4.5.0. It checks an STL → GLB → STL cube roundtrip, verifies that repair welds a split edge, and confirms that in-place edits and overwrites are rejected while the existing files retain their original bytes.

OBJ exports publish the matching MTL beside the OBJ and return its path in `material_library`. Keep both files together when moving the asset. External texture images remain separate. MCP and default CLI calls protect both destination names. Explicit CLI `--overwrite` applies to both output files while protecting the source model and its material libraries.

## Trust and limits

- Users configure the allowed workspace; keep it away from hostile or untrusted concurrent filesystem writers.
- Source files are preserved; existing outputs are not overwritten by MCP.
- Blender 4.1+ is required for 3D operations; Blender 4.5 is exercised in CI.
- Inputs and output are capped in size and errors/streamed logs are bounded.
- This is not a remote server or OS sandbox, and cannot execute with permissions a hosting harness does not grant.
