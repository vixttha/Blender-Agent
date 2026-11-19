# Blender-Agent Refinement Toolkit cases

The [test plan](PLAN.md) records implementation status, runner evidence, and upcoming work for these cases.

| Case | Area | Priority | Suggested implementation | Expected outcome |
|---|---|---|---|---|
| DOCS-001 | Catalog | P0 | Python standard library | The validator accepts a well-formed catalog and exits successfully. |
| PYTHON-001 | Host runtime | P0 | Existing Python 3.11 and 3.12 CI matrix on Linux and Windows | The package installs, source compiles, and unit and negative-path checks pass. |
| MCP-001 | OBJ material and preservation | P0 | Existing installed-wheel MCP roundtrip and collision fixtures | Blender re-import preserves the assigned `AuditRed` color and both source files. An existing OBJ or MTL is preserved and its missing counterpart stays absent. |
| BLENDER-001 | Multi-scene geometry | P0 | Existing two-scene Blender fixture and installed-wheel MCP conversion | The response reports the active triangle as one object, three vertices and one face. The exported STL contains one triangle and the source BLEND stays byte-identical. |
| MCP-002 | Windows active cancellation | P0 | Real Blender and installed MCP wheel on Windows | Cancellation before publication leaves the destination absent. After the worker exits or reaches its timeout, a subsequent job succeeds. |
| RUNTIME-001 | Compatibility | P0 | Existing clean-wheel harness and public compatibility matrix | Declared configurations under review start the documented entry points and pass their assigned smoke cases. The actual runtime versions and Blender binary digest are recorded. |
| OBJ-001 | Interrupted publication | P1 | Existing job recovery tests and scoped exact-run evidence | Retry restores a consistent OBJ and MTL pair, preserves unrelated files, and respects an active publisher's lock. |
| GEOMETRY-001 | Format roundtrip | P1 | Asymmetric synthetic mesh and format-specific read-back | Format-appropriate checks preserve expected scale, axis orientation, bounds, and topology within stated tolerances. |
| GEOMETRY-002 | Primitive creation | P1 | UV sphere and cylinder through the existing real Blender smoke harness | Both outputs contain finite coordinates and mesh faces and match the requested dimensions within stated tolerances. |
| RELEASE-001 | Release evidence verification | P1 | Synthetic required-job results in the existing verifier tests | An omitted, skipped, or failing required job is rejected. Complete successful results for the approved checkout pass verification. |
| RECEIPT-001 | Test evidence integrity | P1 | Synthetic receipts and the existing receipt verifier | Missing, stale, or nonpassing required receipts fail the case. Matching receipts for the tested checkout and run attempt pass. |
