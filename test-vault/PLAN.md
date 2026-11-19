# Blender-Agent Test Vault plan

## Current work

**Planning.** The next case is **BLENDER-001** for [issue #55](https://github.com/vixttha/Blender-Agent/issues/55). Its test code is already in the branch. Its first real Blender result is pending.

## Case status and evidence

| Case | Implementation status | Latest relevant evidence |
|---|---|---|
| DOCS-001 | Implemented | The [push run on the fixture commit](https://github.com/vixttha/Blender-Agent/actions/runs/44466137486) skipped the catalog job. |
| PYTHON-001 | Existing coverage | The four Python matrix jobs passed on [`38e8f63`](https://github.com/vixttha/Blender-Agent/actions/runs/44462288861). |
| MCP-001 | Existing coverage | The material and collision checks ran on [Linux](https://github.com/vixttha/Blender-Agent/actions/runs/44462288861/job/135351712270) and [Windows](https://github.com/vixttha/Blender-Agent/actions/runs/44462288861/job/135351712224) at `38e8f63`. The branch's case-summary additions await a run. |
| BLENDER-001 | Draft test committed | The [two-scene test](../tests/test_mcp_smoke.py#L237) and [fixture](../tests/blender_linked_fixture.py#L72) exist on `9d29da0`. A run that exercises the fixture is pending. |
| MCP-002 | Planned extension | The [active-cancellation check](../tests/test_mcp_smoke.py#L432) runs on POSIX. Its Windows counterpart is tracked in [#47](https://github.com/vixttha/Blender-Agent/issues/47). |
| RUNTIME-001 | Partial coverage | The [compatibility matrix](../docs/HARNESS.md#harness-integration) exercises the installed wheel and pinned Blender builds. The maintained-runtime and build-minimum checks are tracked in [#45](https://github.com/vixttha/Blender-Agent/issues/45) and [#49](https://github.com/vixttha/Blender-Agent/issues/49). |
| OBJ-001 | Existing coverage to map | The [job tests](../tests/test_jobs.py) cover interruption, retry, locks, and rollback. Map those results to the outstanding acceptance criteria in [#23](https://github.com/vixttha/Blender-Agent/issues/23) before adding fixtures. |
| GEOMETRY-001 | Planned extension | The [existing roundtrips](../.github/workflows/ci.yml#L160-L201) use a centered cube. The asymmetric fixture is planned. |
| GEOMETRY-002 | Planned | The worker implements a UV sphere and cylinder. The proposed cases verify their real outputs. |
| RELEASE-001 | Planned extension | Existing verifier tests cover commit and workflow identity and unsuccessful results. The required-job identity cases belong to [#51](https://github.com/vixttha/Blender-Agent/issues/51). |
| RECEIPT-001 | Planned adoption | The starter includes a [receipt verifier](verify_receipts.py). Blender-Agent-specific evidence retention is tracked in [#52](https://github.com/vixttha/Blender-Agent/issues/52). |

The completed application evidence above comes from the push checkout `38e8f63c3fe2e372784276acdbb602cb7409b100`. The live application baseline reviewed for this plan is [`7febadd`](https://github.com/vixttha/Blender-Agent/commit/7febadd1d18bd15967e9eed6223098268dadfe2f). Its [own CI run](https://github.com/vixttha/Blender-Agent/actions/runs/44469831772) is separate from the Test Vault candidate.

## First test run

1. Use the exact candidate checkout with the existing installed-wheel MCP Blender jobs on standard public Ubuntu and Windows runners.
2. Convert the synthetic two-scene BLEND to STL over MCP. The expected scene response is one object, three vertices, and one face. Read back the artifact separately and expect one triangle. Compare the source bytes before and after conversion.
3. Record the actual counts. The draft fixture allows the smoke job to continue on the known file-wide signature of two objects, eleven vertices, and seven faces with one exported triangle. Record that signature as a **case failure** even when the job is green. A different failure needs its own diagnosis.
4. Verify the repair on its own checkout when it is ready. The same fixture must then pass, and a geometry mismatch must fail the job.

## Remaining build order

1. **Windows cancellation.** Adapt the existing scheduling fixture to coordinate with a real Windows Blender process. Observe the start of the request before cancellation and use a successful follow-up request to demonstrate recovery.
2. **Runtime and recovery.** Reuse the wheel build and job recovery tests. Map existing results to [#15](https://github.com/vixttha/Blender-Agent/issues/15) and [#23](https://github.com/vixttha/Blender-Agent/issues/23) before adding targeted checks.
3. **Geometry discovery.** Use unequal dimensions and an off-axis landmark so a swapped or mirrored axis is observable. Use one fixture across the formats whose geometry contracts support the same assertions. For sphere and cylinder cases, specify dimensions independently of the worker's reported values and allow for mesh tessellation.
4. **Evidence integrity.** Add required-job identities to the scoped release verifier cases and check that the Vault rejects missing, stale, or nonpassing receipts. Keep publication approval separate.

## Updating status

Keep the case ID stable from proposal through execution. Link the assertion when code exists. Record pass, fail, skip, or blocked for the case itself and attach the exact checkout SHA, event, run and attempt, job link, platform, and relevant runtime. For a PR run, also record the PR head and base and identify a synthetic merge checkout when used. Keep previous receipts when a run is repeated. Update the current phase after the corresponding work actually occurs.
