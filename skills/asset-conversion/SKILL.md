---
name: asset-conversion
description: Convert supported asset formats through the fixed headless Blender worker.
---

# Asset conversion

Use blender-agent convert SOURCE DESTINATION. Blender 4.1+ must be available. Supported import/export extensions: STL, OBJ, GLB, FBX, BLEND.

The output must be different from the source and inside the workspace. The destination folder must exist.

Conversions can lose materials, animation, exact units or metadata. Validate in the intended destination application. Real Blender integration is a separate acceptance gate.
