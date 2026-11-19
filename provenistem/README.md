# Graphify HQ Ideas and Features

Use this tracker when planning Graphify HQ work. [Ideas](ideas/INDEX.md) capture questions and possible improvements. [Features](features/INDEX.md) track buildable capabilities and link them to ideas, source, and validation evidence.

Graphify HQ helps developers use the graph before and during a change. Start from a feature or question, follow links to code, documentation, and tests, then check the relevant source. Capture an idea when a connection suggests an improvement. Write or update a feature record when it becomes an actionable capability. Use GitHub issues for defects and pull requests and CI for implementation and test results.

## Start here

- [Use Graphify before implementing a change](ideas/records/IDEA-000001.json)
- [Produce a graph-guided implementation brief](features/records/FEAT-000003.json)
- [Track public, local, and private execution](features/records/FEAT-000002.json)

## Branch audit

The [November 19 branch audit](audits/2026-11-19-branch-audit.md) lists all 185 inspected branch heads and the evidence behind IDEAs 000005 through 000014 and FEATs 000005 through 000014.

## Graphify HQ v0.0.8 repair checkpoints

These are planned Graphify HQ checkpoints. Each maps to one audit repair and its GitHub issue. Record the exact implementation commit and public GitHub Actions evidence when each checkpoint is validated.

| Checkpoint | GitHub issue | Work |
| --- | --- | --- |
| `v0.0.8.1` | [BART #66](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/66) | Preserve historical receipt identity across the BART rename and verify live PR provenance under the current repository identity. |
| `v0.0.8.2` | [BART #75](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/75) | Keep the previous graph and receipt consistent if replacement fails. |
| `v0.0.8.3` | [AlderVale #159](https://github.com/vixttha/AlderVale-Pact-of-Ten/issues/159) | Restore the pinned First Spark verifier and dependency lock in the intended merge tree. |
| `v0.0.8.4` | [Lydite #12](https://github.com/vixttha/Lydite-Test-Vault-Template/issues/12) | Rebuild historical maps from a clean checkout. The fix passed in [Lydite draft PR #22](https://github.com/vixttha/Lydite-Test-Vault-Template/pull/22). Lydite tracks this repair as `v0.0.3.11`. |
| `v0.0.8.5` | [Lydite #17](https://github.com/vixttha/Lydite-Test-Vault-Template/issues/17) | Detect executable-bit drift when archived file bytes match. |

[AlderVale #160](https://github.com/vixttha/AlderVale-Pact-of-Ten/issues/160) is a separate enhancement to link First Spark graph evidence to reward and save implementation. It is outside the five repair checkpoints.

Use the next unused IDEA or FEAT ID when adding a record and update the corresponding index. Distinguish proposed work, implementation, test results, and release decisions. Cite the exact Git commit for source evidence and link the run for claims about testing.
