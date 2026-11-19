# Blender-Agent v0.0.2

[Graphify map](graph.json) · [Source receipt](receipt.json) · [All versions](../README.md)

**Source commit:** 2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b

**Candidate only — NOT an approved or published Blender-Agent release.**

Approval, an immutable release tag, and promotion into the approved catalog are pending.

## Feature traceability

- **Atomic output publication** · [Documentation](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md#L1) · [Changelog](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md#L5) · [test_atomic_no_overwrite_even_when_destination_appears_late](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_jobs.py#L99) · [test_parallel_writers_exactly_one_wins](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_jobs.py#L108)
- **Blender process and file limits** · [Documentation](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md#L1) · [Changelog](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md#L7) · [test_log_output_cap_terminates_noisy_process](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_jobs.py#L134) · [test_subprocess_timeout_is_enforced](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_jobs.py#L139) · [test_oversized_output_never_promoted](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_jobs.py#L90) · [test_input_size_cap](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_jobs.py#L83)
- **MCP stdio host integration** · [Documentation](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/HARNESS.md#L1) · [Changelog](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md#L9) · [smoke](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_mcp_smoke.py#L14)
- **Structural mesh inspection** · [Documentation](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/asset-inspection/SKILL.md#L1) · [Changelog](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md#L8) · [test_obj_valid_positive_and_negative_references](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_inspect.py#L81) · [test_obj_bad_face_reference](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_inspect.py#L94) · [test_empty_binary_stl_rejected](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_inspect.py#L64) · [test_empty_obj_rejected](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/tests/test_inspect.py#L69)

## CHANGELOG.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md

- [Changelog](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md#changelog)
- [\[Unreleased\] — v0.0.2 candidate](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md#unreleased--v002-candidate)
- [v0.0.1 — original pre-alpha foundation candidate (not separately released)](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/CHANGELOG.md#v001--original-pre-alpha-foundation-candidate-not-separately-released)

## README.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md

- [Blender-Agent](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md#blender-agent)
- [Capability status](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md#capability-status)
- [Quick start](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md#quick-start)
- [Security and resource limits](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md#security-and-resource-limits)
- [Architecture and roadmap](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md#architecture-and-roadmap)
- [License](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/README.md#license)

## docs/ARCHITECTURE.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md

- [Architecture — v0.0.2 candidate](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md#architecture--v002-candidate)
- [Safety invariants](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md#safety-invariants)
- [Validation and support](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md#validation-and-support)
- [Future B+C architecture](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md#future-bc-architecture)

## docs/HARNESS.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/HARNESS.md

- [Harness integration](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/HARNESS.md#harness-integration)
- [Command-line bridge](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/HARNESS.md#command-line-bridge)
- [MCP stdio bridge](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/HARNESS.md#mcp-stdio-bridge)
- [Trust and limits](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/HARNESS.md#trust-and-limits)

## docs/ROADMAP.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ROADMAP.md

- [Capability roadmap](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ROADMAP.md#capability-roadmap)

## docs/SKILL_POLICY.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/SKILL_POLICY.md

- [Specialist skill system](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/SKILL_POLICY.md#specialist-skill-system)
- [Hierarchical specialist library (selected architecture B)](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/SKILL_POLICY.md#hierarchical-specialist-library-selected-architecture-b)
- [Dynamic skill generation (selected architecture C; not implemented in v0.0.1)](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/SKILL_POLICY.md#dynamic-skill-generation-selected-architecture-c-not-implemented-in-v001)

## skills/asset-conversion/SKILL.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/asset-conversion/SKILL.md

- [Asset conversion](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/asset-conversion/SKILL.md#asset-conversion)

## skills/asset-inspection/SKILL.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/asset-inspection/SKILL.md

- [Asset inspection](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/asset-inspection/SKILL.md#asset-inspection)

## skills/mesh-repair/SKILL.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/mesh-repair/SKILL.md

- [Mesh repair](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/mesh-repair/SKILL.md#mesh-repair)

## skills/procedural-primitives/SKILL.md

Source document at the pinned release commit:

https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/procedural-primitives/SKILL.md

- [Procedural primitives](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/skills/procedural-primitives/SKILL.md#procedural-primitives)

[Review the source PR](https://github.com/vixttha/Blender-Agent/pull/1)
