# Proposals

These are research or conditional proposals. Record owner decisions with the scope, date and review link after approval.

| ID | Proposal | Benefit | Cost or downside | Evidence and adoption trigger |
| --- | --- | --- | --- | --- |
| [CS-001](#cs-001--version-the-job-boundary) | Version the Python job and result boundary | Easier CLI and MCP parity, fixture replay and future adapters | Compatibility surface to maintain | Reuse the existing job JSON and prove one full MCP-to-Blender operation |
| [CS-002](#cs-002--browser-asset-viewer) | TypeScript browser asset viewer | Typed state and a shareable GLB preview | Browser, build and runtime-contract maintenance | Approve an interface workflow and verify preview fidelity and failure states |
| [CS-003](#cs-003--measure-before-native-code) | Native mesh helper | Can accelerate an isolated CPU-heavy operation | Platform wheels, interop and maintenance | Profile a representative operation and show measured end-to-end gain |
| [CS-004](#cs-004--editable-procedural-modeling) | Reusable Geometry Nodes assets | Artist-editable procedural models | Node-group version and fixture maintenance | Approve one parametric modeling feature with repeatable outputs |

## CS-001 · Version the job boundary

**Status:** proposed. Explore adding explicit request/result types to the shared Python core while preserving the existing CLI/MCP contract. Compare against simply adding one operation and its tests first. Validate default behavior, failed inputs and result parity on free public runners. Keep earlier accepted input and result readers working so the change can be backed out without losing assets. [Existing job runner](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/25788c01234841693ce0605053798a39cda7ba9a/src/blender_agent/jobs.py)

## CS-002 · Browser asset viewer

**Status:** conditional. Consider TypeScript with HTML/CSS for an approved preview workflow. Compare an existing GLB viewer with a custom viewer before adopting rendering infrastructure. Check asset loading, accessibility, errors and the Python boundary in browser tests. The viewer can ship independently, so rollback removes the client layer. [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/intro.html) · [Khronos glTF registry](https://registry.khronos.org/glTF/)

## CS-003 · Measure before native code

**Status:** conditional. Profile Blender startup, import/export, and application-owned geometry processing separately on representative synthetic assets. Compare the Python implementation and available Blender primitives before choosing a native helper. Evaluate Rust/PyO3 for an isolated kernel, C++ only for a specific library fit, and Cython for a narrow typed Python loop when it reduces complexity. Record fidelity, speed, peak memory, install behavior and required wheels per supported platform. Retain a fall-back implementation until the native path meets the agreed criteria. [PyO3 distribution guide](https://pyo3.rs/main/building-and-distribution) · [CGAL manual](https://doc.cgal.org/latest/Manual/index.html) · [Cython overview](https://docs.cython.org/en/latest/src/quickstart/overview.html)

## CS-004 · Editable procedural modeling

**Status:** conditional. Pilot one reviewed parameterized model as a Python operation, compare a Geometry Nodes group with a direct Blender API implementation, and test editability, parameter edges, version compatibility, and resulting geometry. Keep the operation narrow enough to remove the node group without affecting unrelated file handling. [Geometry Nodes manual](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/introduction.html)
