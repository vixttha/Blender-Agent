# README HQ and homepage review

Solo source audit. The upstream [version index](https://github.com/vixttha/README-HQ/blob/f50e3749dab90ddfe35894284d1660097a1fb1a8/versions/README.md) identifies v0.0.6 at `f50e3749dab90ddfe35894284d1660097a1fb1a8`. [Draft PR #68](https://github.com/vixttha/README-HQ/pull/68) contains the newer repair checkpoints, while the [standalone default branch](https://github.com/vixttha/README-HQ/blob/a7a989ffb6b664df86aae0ea01053ea2fc0a4405/README.md) still has its initial homepage. The standalone working branch still serves the versioned archive and technique library.

The BART workspace previously recorded template v0.0.1 and stopped homepage history at v0.0.2. Its v0.0.4 rebrand draft already matches the homepage at [`3e7f9e02e61739825b56bcafecebbd0221cc9657`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md). Recover both public snapshots and keep the v0.0.5 draft independent of the published software version.

## Acceptance checks

- Preserve the historical README and artwork bytes and the frozen v0.0.1 template.
- Verify the documented clone against the published v0.0.3 tag at `7febadd1d18bd15967e9eed6223098268dadfe2f`. On public Linux and Windows runners, install cleanly, inspect the triangle, and compare CLI and MCP geometry and digest.
- Resolve application links, view both images at their GitHub destination, and preserve descriptive alternative text.
- Review product and agent naming, release versus development status, capability bounds, and the documented native BLEND trust boundary. The README updates the homepage portion of [issue #56](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/56). That issue also covers security guidance.
- Keep template adoption on `readme-hq` and homepage publication in a separate PR to `main`.
