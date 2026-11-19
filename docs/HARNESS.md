# Harness integration

## CLI (default)

Any harness that can invoke commands in an authorized workspace can use:

~~~sh
python -m pip install -e .
blender-agent --workspace ./workspace inspect input/mesh.stl
blender-agent --workspace ./workspace create uv_sphere output/sphere.glb
~~~

Create workspace/input and workspace/output before running. Blender operations require Blender 4.1+ on the executing machine.

## MCP stdio (optional)

~~~sh
python -m pip install -e ".[mcp]"
blender-agent-mcp
~~~

Configure the harness to launch the blender-agent-mcp command with environment variables BLENDER_AGENT_WORKSPACE (absolute directory) and optionally BLENDER_AGENT_BLENDER (executable path/name).

Example conceptual configuration (adapt to the target harness):

~~~json
{
  "command": "blender-agent-mcp",
  "env": {
    "BLENDER_AGENT_WORKSPACE": "/absolute/path/to/workspace",
    "BLENDER_AGENT_BLENDER": "blender"
  }
}
~~~

The tools are inspect_model, create_primitive, convert_model and repair_mesh. MCP tools do not support overwrite or arbitrary code execution.

The optional adapter currently targets the MCP Python SDK v1 API range mcp>=1.12,<2. This range is intentional; upgrading to SDK v2 needs compatibility work.

## Limits

- A chat model or harness without a connected runtime cannot operate a user's Blender installation.
- No remote network service is exposed by default.
- A shared memory system is not yet implemented; each invocation uses the supplied workspace.
- Treat software capabilities as verified only after testing in the specific host and Blender version.
