---
name: mesh-repair
description: Run limited mesh cleanup on a copy without guaranteeing print readiness.
---

# Mesh repair

Use blender-agent repair SOURCE DESTINATION with Blender 4.1+.

The currently supported operation merges near-duplicate vertices at a fixed 0.0001 scene-unit distance, then recalculates face normals. It neither fills holes nor checks wall thickness.

Do not declare the result watertight, printer-ready or game-ready. Validate with a slicer, dimensional checks and application-specific tests where needed.
