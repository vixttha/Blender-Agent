# Architecture

## Components

~~~text
Any compatible harness -> CLI / MCP -> Shared Python Core
                                      |-- Workspace path boundary
                                      |-- Read-only inspector
                                      |-- Blender job runner
                                            -> Fixed Blender Python worker
                                            -> New output + geometry summary
~~~

The CLI uses only the standard library. The optional MCP adapter uses a bounded compatible Python SDK dependency. No cloud API, remote computer or proprietary model is required by the core.

## Execution boundary

Jobs accept a workspace root, enumerate supported operations, verify source and output paths, start a fixed worker with Blender in background/factory mode and automatic scripting disabled, then move a successful temporary file into place. A source cannot be overwritten in place.

Supported worker operations are primitive creation, import/export conversion and limited mesh cleanup. The worker counts objects, vertices, faces, boundary edges and nonmanifold edges. Counts are diagnostics, **not** geometry certification.

## Multiple harnesses

The same core functions back command-line calls and optional MCP stdio tools. Future bridges must reuse these functions, not copy validation rules. A hosting harness needs permission to execute the command and access its configured workspace. Connecting to a remote Blender GUI is not included in v0.0.1.

## Skill architecture

The agreed design is a hierarchy of permanent specialist skills plus dynamically proposed candidates. v0.0.1 ships four documented foundation skills. Generated skill execution, promotion and shared cross-project memory are **not implemented**. See SKILL_POLICY.md.

## Validation boundary

Python unit tests cover parsing, basic path controls and orchestration. Blender-version compatibility, material fidelity, slicer outcomes, and game-engine imports must be validated separately with real applications. Never infer those from passing unit tests.
