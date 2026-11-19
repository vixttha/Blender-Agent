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

Each checkpoint passed its targeted public-runner checks and is in draft review. Checks covered the original failure, the exact proposed patch and repository state, and the recorded CI results.

| Checkpoint | GitHub issue | Draft and head | Public validation |
| --- | --- | --- | --- |
| `v0.0.8.1` | [BART #66](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/66) | [Template #77](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/77) `070f560` · [OBJ/MTL #78](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/78) `2680e03` | [Template run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44500410227) rebuilt the frozen v0.0.8 archive. The [OBJ/MTL run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44500007115) rebuilt the graph and resolved live PR #17 through the current repository name. |
| `v0.0.8.2` | [BART #75](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/75) | [Draft #79](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/79) `0f7e0c6` | [Public run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44500465829) passed 19 candidate tests, including receipt write failure, retry and concurrent publication rejection. |
| `v0.0.8.3` | [AlderVale #159](https://github.com/vixttha/AlderVale-Pact-of-Ten/issues/159) | [Draft #157](https://github.com/vixttha/AlderVale-Pact-of-Ten/pull/157) `8e0b402` | [Public run](https://github.com/vixttha/AlderVale-Pact-of-Ten/actions/runs/44499692409) built and read back First Spark on the proposed merge `9eb79bb` and rehearsed publication. |
| `v0.0.8.4` | [Lydite #12](https://github.com/vixttha/Lydite-Test-Vault-Template/issues/12) | [Draft #22](https://github.com/vixttha/Lydite-Test-Vault-Template/pull/22) `c5b02ca` | [Public run](https://github.com/vixttha/Lydite-Test-Vault-Template/actions/runs/44499987938) fetched pinned source commits, rebuilt three archived maps, and rejected byte drift. Lydite tracks this as `v0.0.3.11`. |
| `v0.0.8.5` | [Lydite #17](https://github.com/vixttha/Lydite-Test-Vault-Template/issues/17) | [Draft #32](https://github.com/vixttha/Lydite-Test-Vault-Template/pull/32) `3b26628` | [Public run](https://github.com/vixttha/Lydite-Test-Vault-Template/actions/runs/44500407187) rejected a Git mode-only change while a clean checkout reproduced all three maps. |

The BART template drafts stack as [#74](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/74) → [#77](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/77) → [#79](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/79). The OBJ/MTL draft [#78](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/78) targets the application evidence branch. Lydite [#32](https://github.com/vixttha/Lydite-Test-Vault-Template/pull/32) is stacked on [#22](https://github.com/vixttha/Lydite-Test-Vault-Template/pull/22).

[AlderVale #160](https://github.com/vixttha/AlderVale-Pact-of-Ten/issues/160) is a separate enhancement to link First Spark graph evidence to reward and save implementation. It is outside the five repair checkpoints.

Use the next unused IDEA or FEAT ID when adding a record and update the corresponding index. Distinguish proposed work, implementation, test results, and release decisions. Cite the exact Git commit for source evidence and link the run for claims about testing.
