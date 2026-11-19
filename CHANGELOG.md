# Changelog

## [Unreleased] — v0.0.2 candidate

- Repair the default output overwrite race using atomic no-clobber publication; add simultaneous-writer negative regression tests.
- Recheck workspace containment before output publication and document remaining filesystem threat assumptions.
- Bound Blender process logs, runtime and file sizes; add oversized-input/output and timeout tests.
- Validate structural OBJ face references and strengthen malformed STL/OBJ inputs.
- Add real MCP stdio handshake, discovery, tool call and failure tests on free GitHub-hosted Linux and Windows runners.
- Expand real Blender format roundtrips and verify mesh geometry, not only output existence.
- Correct version number and prior documentation claims; keep the six-audit-finding evidence explicit.

## v0.0.1 — original pre-alpha foundation candidate (not separately released)

- Python CLI, optional MCP stdio adapter, STL/OBJ inspection, Blender primitive creation, conversion and limited repair.
- Four starter skill documents, README, security and contribution guidance, public-runner CI.
- No general-purpose autonomous modeling, shared memory, or dynamic skill execution.
