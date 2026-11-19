"""Public-runner audit of active cancellation with the v0.0.3 worker and real Blender."""

import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


GATE = """import os
import time
from pathlib import Path

Path(os.environ['V03_STARTED']).touch()
deadline = time.monotonic() + 45
while not Path(os.environ['V03_RELEASE_GATE']).is_file():
    if time.monotonic() >= deadline:
        raise RuntimeError('Diagnostic fixture timed out waiting for the client')
    time.sleep(0.05)
"""

HOST = """import json
import os
from pathlib import Path

from blender_agent import jobs
from blender_agent.mcp_server import main

run_blender = jobs._run_blender

def observed_blender(command, cwd, timeout):
    job = json.loads(Path(command[-1]).read_text(encoding='utf-8'))
    if Path(job['output']).stem == 'cancelled':
        script = command.index('--python')
        command = [*command[:script], '--python', os.environ['V03_GATE_SCRIPT'], *command[script:]]
    return run_blender(command, cwd, timeout)

jobs._run_blender = observed_blender
raise SystemExit(main(workspace=os.environ['V03_WORKSPACE'], blender=os.environ['BLENDER_BIN'], timeout=60))
"""


async def call(session, name, arguments):
    result = await session.call_tool(name, arguments)
    assert not result.isError, result
    data = result.structuredContent or json.loads(result.content[0].text)
    return data


async def check(root, blender, suffix):
    work = root / "workspace"
    work.mkdir()
    (work / "triangle.obj").write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n", encoding="ascii")
    host, gate_script = root / "host.py", root / "blender_gate.py"
    host.write_text(HOST, encoding="utf-8")
    gate_script.write_text(GATE, encoding="utf-8")
    started, gate = root / "started", root / "continue"
    env = {**os.environ, "BLENDER_BIN": str(blender), "V03_WORKSPACE": str(work),
           "V03_STARTED": str(started), "V03_RELEASE_GATE": str(gate), "V03_GATE_SCRIPT": str(gate_script)}
    parameters = StdioServerParameters(command=sys.executable, args=[str(host)], cwd=root, env=env)
    async with asyncio.timeout(75), stdio_client(parameters) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            request_id = session._request_id
            cancelled_file = "cancelled." + suffix
            interrupted = asyncio.create_task(
                call(session, "create_primitive", {"kind": "cube", "output": cancelled_file})
            )
            try:
                async with asyncio.timeout(20):
                    while not started.exists():
                        if interrupted.done():
                            interrupted.result()
                            raise AssertionError("Blender call finished before its gate")
                        await asyncio.sleep(0.05)
                info = await asyncio.wait_for(call(session, "inspect_model", {"path": "triangle.obj"}), 5)
                assert info["faces"] == 1 and not interrupted.done()
                print(f"V03_CANCEL {suffix}: real Blender paused; MCP inspection replied", flush=True)
                await session.send_notification(types.ClientNotification(
                    types.CancelledNotification(params=types.CancelledNotificationParams(requestId=request_id)),
                ))
                await asyncio.wait_for(session.send_ping(), 5)
            finally:
                if not interrupted.done():
                    interrupted.cancel()
                await asyncio.gather(interrupted, return_exceptions=True)
                gate.touch()
            subsequent = await call(session, "create_primitive", {"kind": "cube", "output": "next." + suffix})
            assert subsequent["ok"] and (work / ("next." + suffix)).is_file()
            assert not (work / cancelled_file).exists()
            assert not (work / "cancelled.mtl").exists()
            assert not any(p.is_dir() for p in work.glob(".blender-agent-*"))
    print(f"V03_CANCEL {suffix}: no cancelled output or sidecar; subsequent job passed; staging cleaned", flush=True)


def main():
    blender = Path(sys.argv[1]).resolve(strict=True)
    for suffix in ("stl", "obj"):
        with tempfile.TemporaryDirectory(prefix="bart-cancel-") as directory:
            asyncio.run(check(Path(directory), blender, suffix))


if __name__ == "__main__":
    main()
