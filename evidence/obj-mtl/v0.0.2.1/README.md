# OBJ/MTL export evidence for Blender-Agent v0.0.2.1

This candidate map records [PR #17](https://github.com/vixttha/Blender-Agent/pull/17)
at source commit [`d788600`](https://github.com/vixttha/Blender-Agent/commit/d7886009b5121fc8a94f4f56d8209c3d04800d54).
The checkpoint is part of the v0.0.3 development series. The accepted application
release snapshots remain in the [version archive](../../../versions/README.md).

- [Source manifest](manifest.json)
- [Graphify evidence graph](graph.json)
- [Deterministic verification receipt](receipt.json)

## What the evidence covers

| Behavior | Exact source and regression | Executed evidence |
| --- | --- | --- |
| Publish the matching MTL and return its path. Blender re-import preserves the assigned material and red color. | [MCP material roundtrip](https://github.com/vixttha/Blender-Agent/blob/d7886009b5121fc8a94f4f56d8209c3d04800d54/tests/test_mcp_smoke.py#L103) | [Blender 4.5.0 on Ubuntu](https://github.com/vixttha/Blender-Agent/actions/runs/44449976785/job/135311249138) |
| Reject an existing destination OBJ or MTL independently, preserving its bytes and leaving no partial output. | [MCP collision assertions](https://github.com/vixttha/Blender-Agent/blob/d7886009b5121fc8a94f4f56d8209c3d04800d54/tests/test_mcp_smoke.py#L131) | [Blender 4.5.0 on Ubuntu](https://github.com/vixttha/Blender-Agent/actions/runs/44449976785/job/135311249138) |
| Reject a missing staged MTL. If OBJ publication raises, remove the newly written MTL or restore its previous contents after explicit overwrite. | [Publication regressions](https://github.com/vixttha/Blender-Agent/blob/d7886009b5121fc8a94f4f56d8209c3d04800d54/tests/test_jobs.py#L44) | [Python matrix and logs](https://github.com/vixttha/Blender-Agent/actions/runs/44449976785) |
| Protect a source MTL referenced by either a single-line or continued `mtllib` directive when CLI overwrite is requested. | [Source-preservation regression](https://github.com/vixttha/Blender-Agent/blob/d7886009b5121fc8a94f4f56d8209c3d04800d54/tests/test_jobs.py#L86) | [Clean-wheel Blender 4.5.0 test](https://github.com/vixttha/Blender-Agent/actions/runs/44450065811/job/135311543740) |

## Application verification

The [PR CI run](https://github.com/vixttha/Blender-Agent/actions/runs/44449976785)
passed all seven jobs on standard GitHub-hosted runners. The PR base
was `42c1ce618543374ed4dd5c8bcac5d437835c4e57`. The four Python jobs and the
Blender job ran on synthetic merge
`42e9f120c8b2e5cb1c5de0e5244e6afffc378974`. Its tree
`87a87334d452b2338ffe13597a3ab7abba25b9f8` matches the PR head tree.
The two MCP stdio jobs used the PR head directly. The [Ubuntu unit
log](https://github.com/vixttha/Blender-Agent/actions/runs/44449976785/job/135311249040)
records 45 passing tests, including the OBJ publication regressions.

For [issue #35](https://github.com/vixttha/Blender-Agent/issues/35), the
[earlier clean-wheel control](https://github.com/vixttha/Blender-Agent/actions/runs/44449803173/job/135310680232)
at `c01661e` reproduced the continued-directive overwrite.
The [repair run](https://github.com/vixttha/Blender-Agent/actions/runs/44450065811/job/135311543740)
checked out `d788600` directly. Blender loaded both fixtures, the CLI rejected
both overwrite attempts, and each source MTL retained its bytes with no
output OBJ created.

External texture files remain separate. The rollback tests exercise reported
publication errors. [Interrupted publication recovery](https://github.com/vixttha/Blender-Agent/issues/23)
and [continued face inspection](https://github.com/vixttha/Blender-Agent/issues/24)
are tracked in the [stacked checkpoint work](https://github.com/vixttha/Blender-Agent/pull/30).

## Graphify verification

The archive workflow uses the [Graphify HQ v0.0.8 kit](https://github.com/vixttha/Blender-Agent/tree/062fb633838daa42204289d889850c03e89d45eb/versions/v0.0.8),
with Graphify 0.9.109. It reads application blobs at the pinned source SHA,
checks GitHub PR membership, reads the resulting map through Graphify MCP,
and compares the graph and receipt byte for byte. The graph's `tested_by`
links identify test definitions. The job links above record test execution.
