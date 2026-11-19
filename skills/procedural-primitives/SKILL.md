---
name: procedural-primitives
description: Generate a cube, UV sphere, or cylinder with a fixed Blender operation.
---

# Procedural primitives

Use blender-agent create cube output/cube.stl --size 1. Other valid kinds are uv_sphere and cylinder.

The cube uses side length, sphere uses diameter, and cylinder uses diameter and height. Values are Blender scene units; STL does not encode physical units.

This is simple primitive generation, not text-to-3D, sculpting or character design. Check exports in the target application.
