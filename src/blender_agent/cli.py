"""CLI accessible to any harness able to execute a command."""

import argparse
import json
import os
import sys

from . import __version__
from .inspect import inspect_asset
from .jobs import DEFAULT_TIMEOUT, PRIMITIVES, execute

SKILLS = [
    {"id": "asset-inspection", "status": "implemented"},
    {"id": "asset-conversion", "status": "implemented-with-blender"},
    {"id": "mesh-repair", "status": "implemented-with-blender-limited"},
    {"id": "procedural-primitives", "status": "implemented-with-blender"},
]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="blender-agent")
    parser.add_argument("--workspace", default=os.environ.get("BLENDER_AGENT_WORKSPACE"))
    parser.add_argument("--blender", default=os.environ.get("BLENDER_AGENT_BLENDER", "blender"))
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("version", help="Display the package version")
    sub.add_parser("skills", help="List shipped skills and their implementation status")
    inspect = sub.add_parser("inspect", help="Read-only structural file inspection")
    inspect.add_argument("source")
    create = sub.add_parser("create", help="Create a primitive using headless Blender")
    create.add_argument("kind", choices=sorted(PRIMITIVES))
    create.add_argument("output")
    create.add_argument("--size", type=float, default=1.0)
    for operation in ("convert", "repair"):
        command = sub.add_parser(operation, help=f"{operation.capitalize()} using headless Blender")
        command.add_argument("source")
        command.add_argument("output")
        command.add_argument("--overwrite", action="store_true")
    sub.add_parser("mcp", help="Run optional MCP stdio server")
    args = parser.parse_args(argv)
    workspace = args.workspace if args.workspace is not None else "."
    try:
        if args.command == "version":
            result = {"version": __version__}
        elif args.command == "skills":
            result = {"skills": SKILLS}
        elif args.command == "inspect":
            result = inspect_asset(args.source, workspace=workspace)
        elif args.command == "mcp":
            from .mcp_server import main as start_mcp
            return start_mcp(workspace=args.workspace, blender=args.blender, timeout=args.timeout)
        else:
            result = execute(
                args.command, workspace=workspace, blender=args.blender,
                timeout=args.timeout, source=getattr(args, "source", None),
                output=args.output, kind=getattr(args, "kind", None),
                size=getattr(args, "size", 1.0),
                overwrite=getattr(args, "overwrite", False),
            )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
