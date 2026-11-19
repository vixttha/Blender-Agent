# Agent operating rules

This public toolkit must remain reusable by people and multiple AI harnesses.

1. Keep personal and identifying information, private project data, and secrets out of repository content, examples and logs.
2. Use the neutral project name Blender-Agent. An alternate product identity remains under review and is not approved for publication.
3. Read README.md, docs/ARCHITECTURE.md, docs/SKILL_POLICY.md and SECURITY.md before editing execution boundaries.
4. Never overwrite original input files. Reject filesystem escapes and require explicit authorization for destructive output changes.
5. Do not expose arbitrary shell or Python execution to an agent. Add reviewed, narrowly scoped operations instead.
6. Separate actual tests from simulations. Never call a model print-ready or game-ready based solely on structural inspection.
7. Keep the core harness-independent; adapters must reuse the same underlying functions.
8. Work on a branch, submit a reviewable PR and check exact-commit CI evidence. No automatic merger or release from an agent review alone.
9. Keep dependencies minimal and do not check in generated or private asset files.
10. Use public, standard GitHub-hosted runners for CI. Do not require paid runners or personal machines.

The current v0.0.1 scope is inspection, limited repair and conversion, primitives, CLI and optional MCP. Dynamic skill generation, complex modeling, game and print validation are roadmap items.
