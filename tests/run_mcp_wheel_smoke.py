"""Build an installable wheel and run the MCP smoke test in an isolated environment."""

import argparse
import os
import platform
import subprocess
import sys
import tempfile
import tomllib
import venv
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blender", type=Path)
    parser.add_argument("--mcp-mode", choices=("minimum", "resolver"), default="minimum")
    args = parser.parse_args()
    blender = args.blender.resolve(strict=True) if args.blender is not None else None

    tests = Path(__file__).resolve().parent
    project = tomllib.loads((tests.parent / "pyproject.toml").read_text(encoding="utf-8"))
    specifier, = project["project"]["optional-dependencies"]["mcp"]
    minimum = specifier.removeprefix("mcp>=").split(",", 1)[0]
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        environment = root / "environment"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        wheels = root / "wheels"

        subprocess.run(
            [python, "-m", "pip", "wheel", "--no-deps", "--wheel-dir", wheels, tests.parent],
            cwd=root, check=True,
        )
        wheel, = wheels.glob("blender_agent-*.whl")
        requirements = [f"{wheel}[mcp]"]
        if args.mcp_mode == "minimum":
            requirements.append(f"mcp=={minimum}")
        subprocess.run(
            [python, "-m", "pip", "install", *requirements],
            cwd=root, check=True,
        )
        subprocess.run([python, "-m", "pip", "check"], cwd=root, check=True)
        print(
            f"MCP wheel: {wheel.name} ({args.mcp_mode}), Python {platform.python_version()}, {platform.platform()}",
            flush=True,
        )
        subprocess.run([python, "-m", "pip", "freeze"], cwd=root, check=True)

        command = [python, tests / "test_mcp_smoke.py"]
        if blender is not None:
            command.extend(["--blender", blender])
        subprocess.run(command, cwd=root, check=True)


if __name__ == "__main__":
    main()
