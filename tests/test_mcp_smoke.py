"""Actual MCP stdio initialization, discovery and invocation test.

Run only in the optional-MCP CI job with pip install -e ".[mcp]".
"""
import asyncio
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

async def smoke():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    with tempfile.TemporaryDirectory() as directory:
        workspace = Path(directory)
        (workspace / "mesh.obj").write_text(
            "v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n", encoding="utf-8"
        )
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "blender_agent.mcp_server"],
            env={**os.environ, "BLENDER_AGENT_WORKSPACE": str(workspace)},
        )
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await asyncio.wait_for(session.initialize(), timeout=20)
                available = await asyncio.wait_for(session.list_tools(), timeout=20)
                names = {tool.name for tool in available.tools}
                assert names == {"inspect_model", "create_primitive",
                                 "convert_model", "repair_mesh"}, names
                result = await asyncio.wait_for(
                    session.call_tool("inspect_model", {"path": "mesh.obj"}),
                    timeout=20,
                )
                assert not result.isError, result
                payload = result.structuredContent
                if payload is None:
                    payload = json.loads(result.content[0].text)
                assert payload["faces"] == 1, payload
                failure = await asyncio.wait_for(
                    session.call_tool("inspect_model", {"path": "../outside.obj"}),
                    timeout=20,
                )
                assert failure.isError, failure
                print("MCP stdio handshake, discovery, invocation and error response: PASS")


if __name__ == "__main__":
    asyncio.run(smoke())
