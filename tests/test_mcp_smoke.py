"""Actual MCP stdio initialization, discovery and invocation test.

Run only in the optional-MCP CI job with pip install -e ".[mcp]".
"""
import asyncio
import json
import os
import shutil
import sysconfig
import tempfile
from pathlib import Path


async def smoke():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    launcher = shutil.which("blender-agent-mcp", path=sysconfig.get_path("scripts"))
    assert launcher, "The installed blender-agent-mcp console script is missing"
    required_arguments = {
        "inspect_model": {"path"},
        "create_primitive": {"kind", "output"},
        "convert_model": {"source", "output"},
        "repair_mesh": {"source", "output"},
    }
    with tempfile.TemporaryDirectory() as directory:
        host_directory = Path(directory)
        workspace = host_directory / "asset workspace"
        workspace.mkdir()
        mesh = "v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n"
        source = workspace / "mesh.obj"
        source.write_text(mesh, encoding="utf-8")
        (host_directory / "outside.obj").write_text(mesh, encoding="utf-8")
        params = StdioServerParameters(
            command=launcher,
            cwd=host_directory,
            env={**os.environ, "BLENDER_AGENT_WORKSPACE": str(workspace)},
        )
        async with asyncio.timeout(60), stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                initialized = await session.initialize()
                assert initialized.serverInfo.name == "blender-agent", initialized
                assert initialized.capabilities.tools is not None, initialized
                available = await session.list_tools()
                schemas = {tool.name: tool.inputSchema for tool in available.tools}
                assert set(schemas) == set(required_arguments), schemas
                for name, expected in required_arguments.items():
                    assert set(schemas[name]["required"]) == expected, schemas[name]
                    assert "overwrite" not in schemas[name]["properties"], schemas[name]

                failure = await session.call_tool("inspect_model", {"path": "../outside.obj"})
                assert failure.isError, failure
                assert any(
                    content.type == "text"
                    and "Path must remain inside the configured workspace." in content.text
                    for content in failure.content
                ), failure

                result = await session.call_tool("inspect_model", {"path": "mesh.obj"})
                assert not result.isError, result
                payload = result.structuredContent
                if payload is None:
                    payload = json.loads(result.content[0].text)
                assert payload["faces"] == 1, payload
                assert source.read_text(encoding="utf-8") == mesh
                print("Installed MCP launcher handshake, tool schemas and workspace isolation: PASS")


if __name__ == "__main__":
    asyncio.run(smoke())
