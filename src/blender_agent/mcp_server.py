"""Optional MCP stdio adapter; the core is usable without MCP or an LLM."""

import os
import sys

from .inspect import inspect_asset
from .jobs import DEFAULT_TIMEOUT, execute, validate_timeout
from .paths import root_path


def main(*, workspace: str | None = None, blender: str | None = None, timeout: int = DEFAULT_TIMEOUT) -> int:
    workspace = workspace if workspace is not None else os.environ.get("BLENDER_AGENT_WORKSPACE")
    if not workspace:
        print("Set BLENDER_AGENT_WORKSPACE or pass --workspace before the mcp subcommand.", file=sys.stderr)
        return 2
    try:
        root = root_path(workspace)
        validate_timeout(timeout)
    except (ValueError, OSError) as exc:
        print(f"Invalid MCP configuration. {exc}", file=sys.stderr)
        return 2
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError('Install the MCP extra: pip install -e ".[mcp]"') from exc

    server = FastMCP("blender-agent")
    executable = blender if blender is not None else os.environ.get("BLENDER_AGENT_BLENDER", "blender")

    @server.tool()
    def inspect_model(path: str) -> dict:
        """Read-only structural inspection of an STL, OBJ, or other supported asset."""
        return inspect_asset(path, root)

    @server.tool()
    def create_primitive(kind: str, output: str, size: float = 1.0) -> dict:
        """Make a cube, UV sphere or cylinder as STL/OBJ/GLB/FBX/BLEND."""
        return execute("create", workspace=root, blender=executable, timeout=timeout,
                       kind=kind, output=output, size=size)

    @server.tool()
    def convert_model(source: str, output: str) -> dict:
        """Convert a model with Blender without overwriting the source."""
        return execute("convert", workspace=root, blender=executable, timeout=timeout,
                       source=source, output=output)

    @server.tool()
    def repair_mesh(source: str, output: str) -> dict:
        """Merge near-duplicate vertices and recalculate face normals in a copy."""
        return execute("repair", workspace=root, blender=executable, timeout=timeout,
                       source=source, output=output)

    server.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
