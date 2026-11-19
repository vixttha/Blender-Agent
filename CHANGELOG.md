# Changelog

## v0.0.2.2 — v0.0.3 development checkpoint

- Resolve the Blender executable against the launch directory before entering the configured workspace (#18).

## v0.0.2.1 — v0.0.3 development checkpoint

- Preserve the matching MTL file when publishing an OBJ. CLI and MCP results include its workspace-relative path.
- Exercise create, convert, repair, and inspect through MCP with Blender, including a colored OBJ roundtrip and separate OBJ and MTL collision checks.

## v0.0.2 — audited pre-alpha foundation

- Repair the default output overwrite race using atomic no-clobber publication; add simultaneous-writer negative regression tests.
- Recheck workspace containment before output publication and document remaining filesystem threat assumptions.
- Bound Blender process logs, runtime and file sizes; add oversized-input/output and timeout tests.
- Validate structural OBJ face references and strengthen malformed STL/OBJ inputs.
- Verify the installed MCP launcher, handshake, tool schemas and workspace isolation on free GitHub-hosted Linux and Windows runners.
- Expand real Blender format roundtrips and verify mesh geometry, not only output existence.
- Correct version number and prior documentation claims; keep the six-audit-finding evidence explicit.

## v0.0.1 — original pre-alpha foundation candidate (not separately released)

- Python CLI, optional MCP stdio adapter, STL/OBJ inspection, Blender primitive creation, conversion and limited repair.
- Four starter skill documents, README, security and contribution guidance, public-runner CI.
- No general-purpose autonomous modeling, shared memory, or dynamic skill execution.
