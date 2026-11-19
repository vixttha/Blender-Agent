"""Exercise the installed MCP launcher with an optional real Blender roundtrip."""
import argparse
import asyncio
import hashlib
import json
import math
import os
import shutil
import struct
import sysconfig
import tempfile
from pathlib import Path


async def call_tool(session, name, **arguments):
    result = await session.call_tool(name, arguments)
    assert not result.isError, (name, arguments, result)
    payload = result.structuredContent
    if payload is None:
        payload = json.loads(result.content[0].text)
    assert isinstance(payload, dict), (name, payload)
    return payload


async def expect_error(session, name, message, **arguments):
    result = await session.call_tool(name, arguments)
    assert result.isError, (name, arguments, result)
    assert any(
        content.type == "text" and message in content.text
        for content in result.content
    ), (name, arguments, result)


async def publish(session, workspace, tool, operation, *, output, **arguments):
    payload = await call_tool(session, tool, output=output, **arguments)
    assert payload["ok"] is True and payload["operation"] == operation, payload
    assert Path(payload["output"]) == Path(output), payload
    content = (workspace / output).read_bytes()
    assert 0 < len(content) == payload["size_bytes"], payload
    geometry = payload["geometry"]
    assert geometry["mesh_objects"] == 1 and geometry["faces"] > 0, payload
    return content, geometry


async def blender_roundtrip(session, workspace):
    workflow = (
        ("create_primitive", "create", "cube.stl", {"kind": "cube", "size": 1.0}),
        ("convert_model", "convert", "cube.glb", {"source": "cube.stl"}),
        ("convert_model", "convert", "roundtrip.stl", {"source": "cube.glb"}),
        ("repair_mesh", "repair", "repaired.stl", {"source": "roundtrip.stl"}),
    )
    snapshots = {}
    for tool, operation, output, arguments in workflow:
        content, _ = await publish(
            session, workspace, tool, operation, output=output, **arguments,
        )
        snapshots[output] = content

    for name, content in snapshots.items():
        info = await call_tool(session, "inspect_model", path=name)
        assert info["name"] == name and info["size_bytes"] == len(content), info
        assert info["sha256"] == hashlib.sha256(content).hexdigest(), info
        if name.endswith(".stl"):
            assert info["format"] == "stl" and info["triangles"] == 12, info
            for key, expected in (("min", -0.5), ("max", 0.5)):
                bounds = info["bounds"][key]
                assert len(bounds) == 3 and all(
                    math.isclose(value, expected, rel_tol=0, abs_tol=0.005)
                    for value in bounds
                ), (name, info)
        else:
            assert info["format"] == "glb" and content.startswith(b"glTF"), info

    # Two adjacent triangles whose shared edge is split by less than the weld distance.
    seam = b"v 0 0 0\nv 1 0 0\nv 0 1 0\nv 1.00005 0 0\nv 0.00005 1 0\nv 1 1 0\nf 1 2 3\nf 4 6 5\n"
    (workspace / "split-edge.obj").write_bytes(seam)
    snapshots["split-edge.obj"] = seam
    _, before = await publish(
        session, workspace, "convert_model", "convert", source="split-edge.obj", output="split-edge.stl",
    )
    _, after = await publish(
        session, workspace, "repair_mesh", "repair", source="split-edge.obj", output="welded.stl",
    )
    assert before["vertices"] == 6 and after["vertices"] == 4, (before, after)
    assert before["faces"] == after["faces"] == 2, (before, after)

    await expect_error(
        session, "repair_mesh", "Source files cannot be modified in place.",
        source="roundtrip.stl", output="roundtrip.stl",
    )
    await expect_error(
        session, "create_primitive", "Destination already exists",
        kind="cube", size=2.0, output="repaired.stl",
    )
    for name, content in snapshots.items():
        assert (workspace / name).read_bytes() == content, name

    print("MCP workflow: all four tools, STL → GLB → STL geometry, and repair passed.")
    print("MCP repair: split-edge fixture welded 6 vertices to 4 and kept both faces.")
    print("MCP file safety: in-place repair and destination overwrite denied; original bytes unchanged.")


async def obj_material_roundtrip(session, workspace):
    source = b"mtllib source.mtl\no Triangle\nv 0 0 0\nv 1 0 0\nv 0 1 0\nusemtl AuditRed\nf 1 2 3\n"
    material = b"newmtl AuditRed\nKd 1.0 0.0 0.0\n"
    (workspace / "source.obj").write_bytes(source)
    (workspace / "source.mtl").write_bytes(material)

    output = await call_tool(session, "convert_model", source="source.obj", output="red model.obj")
    assert output["material_library"] == "red model.mtl", output
    obj = (workspace / "red model.obj").read_bytes()
    mtl = (workspace / "red model.mtl").read_bytes()
    assert b"mtllib red model.mtl" in obj.splitlines() and b"usemtl AuditRed" in obj.splitlines(), obj
    assert b"newmtl AuditRed" in mtl.splitlines(), mtl

    # Convert the published OBJ with Blender, then read the material assigned in the resulting GLB.
    glb, _ = await publish(
        session, workspace, "convert_model", "convert", source="red model.obj", output="color.glb",
    )
    size, kind = struct.unpack_from("<I4s", glb, 12)
    assert glb[:4] == b"glTF" and kind == b"JSON"
    scene = json.loads(glb[20:20 + size])
    primitive, = scene["meshes"][0]["primitives"]
    restored = scene["materials"][primitive["material"]]
    color = restored["pbrMetallicRoughness"]["baseColorFactor"]
    assert restored["name"] == "AuditRed", restored
    assert len(color) == 4 and all(
        math.isclose(channel, expected, abs_tol=0.001)
        for channel, expected in zip(color, (1.0, 0.0, 0.0, 1.0))
    ), restored

    for suffix, missing_suffix in ((".obj", ".mtl"), (".mtl", ".obj")):
        existing = workspace / f"collision{suffix}"
        existing.write_bytes(b"keep existing destination")
        await expect_error(
            session, "convert_model", "Destination already exists",
            source="source.obj", output="collision.obj",
        )
        assert existing.read_bytes() == b"keep existing destination"
        assert not (workspace / f"collision{missing_suffix}").exists()
        existing.unlink()

    assert (workspace / "source.obj").read_bytes() == source
    assert (workspace / "source.mtl").read_bytes() == material
    print("MCP OBJ materials: Blender re-import preserved the assigned AuditRed color.")
    print("MCP OBJ collisions: existing OBJ and MTL preserved, with no partial output.")


async def smoke(blender):
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
        env = {**os.environ, "BLENDER_AGENT_WORKSPACE": str(workspace)}
        if blender is not None:
            env["BLENDER_AGENT_BLENDER"] = str(blender.resolve(strict=True))
        params = StdioServerParameters(
            command=launcher,
            cwd=host_directory,
            env=env,
        )
        timeout = 180 if blender is not None else 60
        async with asyncio.timeout(timeout), stdio_client(params) as (reader, writer):
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

                await expect_error(
                    session, "inspect_model", "Path must remain inside the configured workspace.",
                    path="../outside.obj",
                )
                payload = await call_tool(session, "inspect_model", path="mesh.obj")
                assert payload["faces"] == 1, payload
                assert source.read_text(encoding="utf-8") == mesh
                print("Installed MCP launcher handshake, tool schemas and workspace isolation: PASS")
                if blender is not None:
                    await blender_roundtrip(session, workspace)
                    await obj_material_roundtrip(session, workspace)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blender", type=Path, help="Path to a real Blender executable for the roundtrip")
    asyncio.run(smoke(parser.parse_args().blender))
