---
name: asset-inspection
description: Read-only inspection of basic STL and OBJ structure and other supported asset metadata.
---

# Asset inspection

Use blender-agent inspect PATH or the MCP inspect_model tool. The source must resolve within the configured workspace.

Implemented: SHA-256 and file size for STL, OBJ, GLB, FBX and BLEND; basic STL triangle counts and bounds; OBJ vertices/faces and bounds.

A successful inspection is not proof of watertightness, wall thickness, rig correctness, collision validity or visual quality.

Test with python -m unittest discover -s tests -v.
