"""Optional MCP stdio adapter; the core is usable without MCP or an LLM."""

import os

from .inspect import inspect_asset
from .jobs import execute


def main() -> int:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError('Install the MCP extra: pip install -e ".[mcp]"') from exc

    server = FastMCP("blender-agent")
    workspace = os.environ.get("BLENDER_AGENT_WORKSPACE", ".")
    executable = os.environ.get("BLENDER_AGENT_BLENDER", "blender")

    @server.tool()
    def inspect_model(path: str) -> dict:
        """Read-only structural inspection of an STL, OBJ, or other supported asset."""
        return inspect_asset(path, workspace)

    @server.tool()
    def create_primitive(kind: str, output: str, size: float = 1.0) -> dict:
        """Make a cube, UV sphere or cylinder as STL/OBJ/GLB/FBX/BLEND."""
        return execute("create", workspace=workspace, blender=executable,
                       kind=kind, output=output, size=size)

    @server.tool()
    def convert_model(source: str, output: str) -> dict:
        """Convert a model with Blender without overwriting the source."""
        return execute("convert", workspace=workspace, blender=executable,
                       source=source, output=output)

    @server.tool()
    def repair_mesh(source: str, output: str) -> dict:
        """Merge near-duplicate vertices and recalculate face normals in a copy."""
        return execute("repair", workspace=workspace, blender=executable,
                       source=source, output=output)

    server.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
