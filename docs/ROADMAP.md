# Capability roadmap

Planned scope is broader than the v0.0.1 implementation.

| Department | v0.0.1 status | Later acceptance target |
| --- | --- | --- |
| Game assets | Not implemented | Engine-ready meshes, UVs, LODs, collision and validated exports |
| STL / 3D printing | Limited inspect and repair | Dimensions, wall thickness, watertightness, slicer test and printer profile |
| File engineering | Foundation implemented | Batch operations, validation, reproducible repairs |
| Organic sculpting | Not implemented | Anatomy-aware workflows and verified topology |
| World creation | Not implemented | Modular procedural environments and performance checks |
| Rigging / animation | Not implemented | Deformation, animation and engine export checks |

Cross-cutting future work: verified Blender integration matrix, AI-assisted generation, isolated shared memory, dynamic skill proposal testing, and host-specific integration acceptance.

The next gate after Python tests is real Blender integration on an exact build. Do not advertise this version as production-ready until those checks pass.
