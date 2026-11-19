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

The optional dependency supports the MCP SDK v1 API range `mcp>=1.12,<2`. Public CI on Linux and Windows starts the installed `blender-agent-mcp` command from a separate working directory, initializes a real stdio session, checks each tool's input schema, and verifies workspace isolation and read-only inspection. Individual MCP hosts may require different launch configuration.

## Trust and limits

- Users configure the allowed workspace; keep it away from hostile or untrusted concurrent filesystem writers.
- Source files are preserved; existing outputs are not overwritten by MCP.
- Blender 4.1+ is required for 3D operations; Blender 4.5 is exercised in CI.
- Inputs and output are capped in size and errors/streamed logs are bounded.
- This is not a remote server or OS sandbox, and cannot execute with permissions a hosting harness does not grant.
