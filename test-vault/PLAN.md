# Graphify HQ first test plan

**Status: Proposed.** This plan defines 12 cases. Reusable Python checks already exist in the Graphify kit and the BART recovery draft. The Vault's [case catalog](cases.md) starts empty until project test work begins.

## Python · unittest

Owns Graphify behavior and on-disk recovery. Use the real evidence builder and Graphify MCP for the graph cases. Reuse the publication tests already in BART #79 when that candidate is available on the test checkout.

| Case ID | Behavior | Fixture and action | Expected result |
| --- | --- | --- | --- |
| `GHQ-PY-001` | Graph generation and MCP readback | Pin a tiny Git fixture with one feature, a unique known source line, and an expected relationship. Run the builder and query the resulting graph through Graphify MCP. | The generated graph reports the pinned source commit. The feature reaches the expected relationship and source path and line. The receipt records successful MCP verification. |
| `GHQ-PY-002` | Deterministic rebuild | Build the same pinned fixture twice in separate temporary output directories using the same locked dependencies. | The two graph files have identical bytes, as do the two receipts. The regular CLI check also accepts the first build. |
| `GHQ-PY-003` | Recover an interrupted replacement | Use the existing #79 fixture with a previously verified pair. Kill the writer after the graph replacement, then exercise a normal check and a publish retry. Include a second interruption during recovery using #79's existing case. | The next check restores the previous graph and receipt byte for byte. An interrupted rollback can be repeated. A retry publishes a matching new pair and the next run can acquire the lock. |
| `GHQ-PY-004` | Recover an interrupted first publish | Use #79's empty-output fixture. Kill the first writer after the graph replacement, then check and retry. | Recovery removes the incomplete output. The check reports missing evidence, and retry produces a complete pair without manual cleanup. |

[Pinned Graphify v0.0.8 kit](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/6af3c2025be3f51e02dca4e4502088c526aae6d1/versions/v0.0.8) · [BART #79 recovery tests](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/d227b202c7cce1b86a1ee06596d709f3dfee1039/candidate/test_evidence_map.py) · [Lydite Python guide](https://github.com/vixttha/Lydite-Test-Vault-Template/blob/fe7b00aa17862d7a01dfd15481594be837bc6d9f/languages/python/GUIDE.md)

## Bash · Git and workflow integration

Owns the workflow's Git fetch, archive extraction, shell quoting, and failure propagation. Exercise the actual fetch-and-extract step or a shared entry point used by that step. Use disposable Git remotes with known commit objects so these cases can run on an ordinary public Ubuntu runner.

| Case ID | Behavior | Fixture and action | Expected result |
| --- | --- | --- | --- |
| `GHQ-SH-001` | Use exact requested Git pins | Create a bare remote with distinguishable old and new commits. Give the step valid full SHAs for the source and the kit or provenance input. Put the branch tip at the newer commit. | The requested source object is available, and the extracted kit and verifier bytes match their pinned commits even though the branch tip points elsewhere. |
| `GHQ-SH-002` | Quote checkout and staging paths | Run the same workflow step with spaces in the checkout path and runner temporary directory while keeping all pins valid. | The step succeeds and the expected files appear under the intended temporary path with their exact contents. |
| `GHQ-SH-003` | Stop on a missing pin | Use a syntactically valid full SHA absent from the temporary remote. Record digests of a sentinel graph and receipt in the existing archive before running the step. | The real step exits nonzero. It produces no extracted kit for the failed attempt, and the previous archive's graph and receipt digests still match. |

[Pinned OBJ/MTL workflow](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/2680e03a3d1a7216666554c5baca43b2ec93b944/.github/workflows/obj-mtl-evidence.yml) · [Lydite Bash guide](https://github.com/vixttha/Lydite-Test-Vault-Template/blob/fe7b00aa17862d7a01dfd15481594be837bc6d9f/languages/bash/GUIDE.md)

## JavaScript · node:test

Owns the exported data contract at the consumer boundary. Read the raw JSON files without importing the Python builder. Use the Python-generated pair for the valid case and mutate isolated copies for rejected inputs.

| Case ID | Behavior | Fixture and action | Expected result |
| --- | --- | --- | --- |
| `GHQ-JS-001` | Accept a valid exported pair | Read the actual graph and receipt produced by GHQ-PY-001. Supply the expected source SHA from the fixture manifest. | Both files parse. The graph's built-at commit and receipt's source commit match the pin. Receipt node and edge counts match the graph arrays. The graph digest matches, node IDs are unique, and every link endpoint exists. |
| `GHQ-JS-002` | Reject a stale source commit | Keep the valid graph bytes and receipt digest. Change only the receipt's source commit to a different full SHA. | The consumer rejects the pair for a source commit mismatch. |
| `GHQ-JS-003` | Reject a stale graph digest | Make a semantically harmless change to the graph bytes, such as appending a newline. Keep the original receipt. | The consumer rejects the pair for a digest mismatch even though both files still parse. |
| `GHQ-JS-004` | Reject a dangling edge | Change one existing edge endpoint to a nonexistent node ID. Recompute the digest in the copied receipt and keep the edge count the same. | The consumer rejects the pair for a missing edge endpoint. |
| `GHQ-JS-005` | Reject a duplicate node ID | Append a duplicate of an existing node. Update the copied receipt's node count and digest, and keep the links valid. | The consumer rejects the pair for a duplicate node ID even though the digest, counts, and reachability checks are otherwise satisfied. |

[Pinned graph and receipt example](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/6af3c2025be3f51e02dca4e4502088c526aae6d1/graphify/v0.0.8) · [Lydite JavaScript guide](https://github.com/vixttha/Lydite-Test-Vault-Template/blob/fe7b00aa17862d7a01dfd15481594be837bc6d9f/languages/javascript/GUIDE.md)

## Implementation order and evidence

1. Register and reuse the existing Python checks first, starting with graph readback and interrupted replacement. Before adding new Python code, confirm whether the graph builder and #79 already supply the required assertions on the target checkout.
2. Add the three Bash workflow cases. Use a separate temporary Git fixture so no checkout, real remote, or committed archive gets modified.
3. Add the JavaScript consumer suite. Keep fixture mutations outside the frozen Graphify v0.0.8 archive. Bind GHQ-JS-001 to the Python-produced graph using Lydite with required check IDs `python-build` and `node-consume`. Share the exact `graph.json` bytes, with `receipt.json` as the consumer's companion input.

Use a standard GitHub-hosted Ubuntu runner with the pinned kit dependencies. Record the case ID, command, exact checkout SHA, run ID and attempt, runner/runtime, outcome, and evidence digest when the case uses shared bytes. Keep the tested checkout SHA separate from the source commit described in the graph. [Lydite run receipt contract](https://github.com/vixttha/Lydite-Test-Vault-Template/blob/fe7b00aa17862d7a01dfd15481594be837bc6d9f/starter/test-vault/evidence.md) · [Graphify HQ checkpoint tracker](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/provenistem/graphify-hq/provenistem)
