| BLENDER-001 | Implemented, case failed | On PR #60 checkout `f85385ae0e8928061c860272567ad694b7d98261`, the [Blender 4.1 Ubuntu](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44477142669/job/135400322393), [Blender 4.5 Ubuntu](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44477142669/job/135400322637) and [Blender 4.5 Windows](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44477142669/job/135400322194) jobs recorded the known case failure. The [two-scene test](../tests/test_mcp_smoke.py#L237) and [fixture](../tests/blender_linked_fixture.py#L72) are available for the repair. |nted | The [catalog job for PR #60](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44477142547/job/135400321689) passed on synthetic checkout `f85385ae0e8928061c860272567ad694b7d98261`. |nder-Agent Refinement Toolkit Test Vault plan

## Current work

The project Test Vault adopts the [starter shipped in Lydite v0.0.4](https://github.com/vixttha/Lydite-Test-Vault-Template/tree/87d25d80d3154d295052412b64b29a0f0f152c27/starter). Starter acceptance covers the catalog, case-plan-bound receipts and preservation of the existing project cases. The [upstream release run](https://github.com/vixttha/Lydite-Test-Vault-Template/actions/runs/44506598515) covers the template's adoption rehearsal. Project results come from this repository's public workflows.

The next application test task is **BLENDER-001** for [issue #55](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/55). The existing fixture reproduced the multi-scene geometry mismatch on all three real Blender jobs in PR #60. The planned repair owns the next case-specific pass.

## Test languages

| Priority | Language and runtime | What it should prove | First case or observable result |
|---|---|---|---|
| 1 | Python 3.11 and 3.12 with `unittest` on the host, plus Blender's bundled Python for `bpy` and `bmesh` | BART CLI and MCP contracts, mesh behavior, publication and release evidence. The host drives the installed wheel and the real MCP client. Blender Python sets up and reads Blender data. | For BLENDER-001, use the existing two-scene fixture, compare the MCP counts with the active mesh, read the STL independently, and confirm the source BLEND bytes are preserved. Follow with Windows cancellation and asymmetric format checks. |
| 2 | PowerShell on public Windows | Windows-native invocation, argument handling, filesystem paths, exit propagation and the Blender setup contract. | Extend the current Windows harness where needed. Launch the installed command from a working directory with spaces, pass a workspace path with spaces, and check exit status and output location. Keep the Windows MCP cancellation assertions in Python. |
| 3 | Bash on public Ubuntu | The documented Linux shell walkthrough and shell-specific setup behavior. | Reuse the existing README walkthrough and checksum-verified Blender setup. Check that an invalid download or failed CLI command surfaces a failing exit status and cannot produce a success receipt. |
| Conditional | JavaScript with Node.js | Independent MCP interoperability when a JavaScript client is a supported target, or a format assertion where a separate parser adds evidence. | Define a client or parser contract first. An independent MCP client would start the installed stdio launcher, discover the tools and check one structured success and one documented rejection. |

**First implementation order.** Start with the existing Python fixture for #55. Add a PowerShell or Bash case only when it asserts behavior owned by that shell. Reuse the existing public jobs. Each case should specify its stable ID, runtime, assertion source, command, expected result, and evidence location. Use the case catalog and existing `tests/` now. Evaluate Lydite's [native language inventory](https://github.com/vixttha/Lydite-Test-Vault-Template/blob/87d25d80d3154d295052412b64b29a0f0f152c27/docs/testing.md#get-the-inventory) once a real assertion can be registered without copying canonical project tests. YAML configures the jobs and JSON records metadata and evidence.

## Case status and evidence

| Case | Implementation status | Latest relevant evidence |
|---|---|---|
| DOCS-001 | Implemented | The [push run on the fixture commit](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44466137486) skipped the catalog job. |
| PYTHON-001 | Existing coverage | The four Python matrix jobs passed on [`38e8f63`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44462288861). |
| MCP-001 | Existing coverage | The material and collision checks ran on [Linux](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44462288861/job/135351712270) and [Windows](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44462288861/job/135351712224) at `38e8f63`. The branch's case-summary additions await a run. |
| BLENDER-001 | Draft test committed | The [two-scene test](../tests/test_mcp_smoke.py#L237) and [fixture](../tests/blender_linked_fixture.py#L72) exist on `9d29da0`. A run that exercises the fixture is pending. |
| MCP-002 | Planned extension | The [active-cancellation check](../tests/test_mcp_smoke.py#L432) runs on POSIX. Its Windows counterpart is tracked in [#47](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/47). |
| RUNTIME-001 | Partial coverage | The [compatibility matrix](../docs/HARNESS.md#harness-integration) exercises the installed wheel and pinned Blender builds. The maintained-runtime and build-minimum checks are tracked in [#45](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/45) and [#49](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/49). |
| OBJ-001 | Existing coverage to map | The [job tests](../tests/test_jobs.py) cover interruption, retry, locks, and rollback. Map those results to the outstanding acceptance criteria in [#23](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/23) before adding fixtures. |
| GEOMETRY-001 | Planned extension | The [existing roundtrips](../.github/workflows/ci.yml#L160-L201) use a centered cube. The asymmetric fixture is planned. |
| GEOMETRY-002 | Planned | The worker implements a UV sphere and cylinder. The proposed cases verify their real outputs. |
| RELEASE-001 | Planned extension | Existing verifier tests cover commit and workflow identity and unsuccessful results. The required-job identity cases belong to [#51](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/51). |
| RECEIPT-001 | Planned adoption | The starter includes a [receipt verifier](verify_receipts.py). Blender-Agent Refinement Toolkit-specific evidence retention is tracked in [#52](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/52). |

Earlier push evidence above comes from `38e8f63c3fe2e372784276acdbb602cb7409b100`. PR #60 used head `2ada505088aacb7fb9451cb96ecd1d111175970b` and base `9d29da099785003ad2d3f97f34b9ff04dffb5a70`. The live application baseline reviewed for this update is [`3e7f9e02e61739825b56bcafecebbd0221cc9657`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/commit/3e7f9e02e61739825b56bcafecebbd0221cc9657). Its [own CI run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44478268534) is separate from Test Vault evidence.

## Next run for BLENDER-001

1. Use the exact candidate checkout with the existing installed-wheel MCP Blender jobs on standard public Ubuntu and Windows runners.
2. Convert the synthetic two-scene BLEND to STL over MCP. The expected scene response is one object, three vertices, and one face. Read back the artifact separately and expect one triangle. Compare the source bytes before and after conversion.
3. Record the actual counts. The draft fixture allows the smoke job to continue on the known file-wide signature of two objects, eleven vertices, and seven faces with one exported triangle. Record that signature as a **case failure** even when the job is green. A different failure needs its own diagnosis.
4. Verify the repair on its own checkout when it is ready. The same fixture must then pass, and a geometry mismatch must fail the job.

## Remaining build order

1. **Windows cancellation.** Adapt the existing scheduling fixture to coordinate with a real Windows Blender process. Observe the start of the request before cancellation and use a successful follow-up request to demonstrate recovery.
2. **Runtime and recovery.** Reuse the wheel build and job recovery tests. Map existing results to [#15](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/15) and [#23](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/23) before adding targeted checks.
3. **Geometry discovery.** Use unequal dimensions and an off-axis landmark so a swapped or mirrored axis is observable. Use one fixture across the formats whose geometry contracts support the same assertions. For sphere and cylinder cases, specify dimensions independently of the worker's reported values and allow for mesh tessellation.
4. **Evidence integrity.** Add required-job identities to the scoped release verifier cases and check that the Vault rejects missing, stale, or nonpassing receipts. Keep publication approval separate.

## Updating status

Keep the case ID stable from proposal through execution. Link the assertion when code exists. Record pass, fail, skip, or blocked for the case itself and attach the exact checkout SHA, event, run and attempt, job link, platform, and relevant runtime. For a PR run, also record the PR head and base and identify a synthetic merge checkout when used. Keep previous receipts when a run is repeated. Update the current phase after the corresponding work actually occurs.
