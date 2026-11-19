# Changelog

## v0.0.2.7 — v0.0.3 development checkpoint

- Require successful Blender operations and mesh faces, validate staged STL and OBJ files within the inspection limit, and label scene geometry and staged artifact metadata (#14).

## v0.0.2.6 — v0.0.3 development checkpoint

- Accept continued OBJ polygons while rejecting incomplete continuation records and retaining input limits (#24).

## v0.0.2.5 — v0.0.3 development checkpoint

- Stream ASCII STL counts and bounds, detect file changes during inspection, and clarify temporary export disk use (#13).

## v0.0.2.4 — v0.0.3 development checkpoint

- Require setuptools 77.0.3 or later and verify an MIT-licensed wheel built with the minimum backend (#25).

## v0.0.2.3 — v0.0.3 development checkpoint

- Require an explicit MCP workspace and honor the CLI workspace, Blender executable, and timeout flags (#12).

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
