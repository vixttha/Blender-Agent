# Graphify HQ branch audit · November 19, 2026

The audit covers Graphify source, workflows, published maps, receipts, and ways to use them in development. Every listed branch head was checked for tracked Graphify paths. Selected builders, manifests, graph relationships, and CI jobs received a deeper review. This was a source and evidence audit of Graphify use across the repos.

GitHub shows three repositories in this scope. [Graphify HQ's reusable kit](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/6af3c2025be3f51e02dca4e4502088c526aae6d1) and [this tracker](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/ae9e55cd388de4b605945cd2a3871d55a2838e95) are branches of BART and are included in its count. Graphify HQ remains archived at **v0.0.8** with Graphify engine **0.9.109**. The source for the self-map is `062fb633838daa42204289d889850c03e89d45eb`. [Kit catalog](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/6af3c2025be3f51e02dca4e4502088c526aae6d1/graphify/catalog.json) · [Generation run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44453058234)

| Repository | Branch heads checked | Heads with matching tracked files | Without matching tracked files |
| --- | ---: | ---: | ---: |
| AlderVale | 135 | 94 | 41 |
| BART, including Graphify HQ | 47 | 24 | 23 |
| Lydite | 3 | 3 | 0 |
| **Total** | **185** | **121** | **64** |

## Findings

### Graphify HQ and BART

- The shared kit, tracker, and runner draft are separate from the application graph archive. [BART draft #74](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/74) passed the standard public runner at `2780136a546bbaf88ba3e6d679c31343e9bd32f3` and has documented local replay and simulated private-event checks. Live private scheduling is unverified. [Public runner](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44480392682)
- The application archive distinguishes the `v0.0.3` published pre-release at `7febadd1d18bd15967e9eed6223098268dadfe2f` from the `v0.0.3` candidate at `38e8f63c3fe2e372784276acdbb602cb7409b100`. The OBJ/MTL feature graph pins `d7886009b5121fc8a94f4f56d8209c3d04800d54`, and the Code Stack and project-instruction branches carry their own maps. [BART application archive](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/2faf3674a5470c369b30f0d55b6fd5ef56e1e710) · [Code Stack template](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/ba2ce5c3c9d07602593078d4c97f89b6cdc6643b) · [Instructions archive](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/388ddccdf6d84d302ce66392942873ab6c4347aa)
- The isolated OBJ/MTL graph contains 34 nodes and 61 edges. Following `material-roundtrip` reaches the Blender worker, the job code and the smoke test. Following `destination-collisions` or `publication-rollback` reaches different assertions. A future change to export should inspect those separate behavior paths before choosing which tests to run. The map's digest, source commit and counts match its stored receipt. [OBJ/MTL map and receipt](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/2faf3674a5470c369b30f0d55b6fd5ef56e1e710/evidence/obj-mtl/v0.0.2.1)
- BART #75 tracks consistency of the graph and receipt on failed output writes. BART #66 tracks historical repository identity versus current live PR lookup. The runner draft covers archive identity for the kit, while the OBJ/MTL workflow and live PR rename handling remain tracked. [#75](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/75) · [#66](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/66)

### AlderVale

- Game `main` runs the code-only workflow. The retained `main` graph is pinned to the audited `main` head, with 1,377 nodes and 3,458 edges. The v0.0.7 kit is on the dedicated HQ branch. The published First Spark feature snapshot is pinned to `5632aec210d184552abbbc3290bc1e201f1eb9b2`. [Game workflow](https://github.com/vixttha/AlderVale-Pact-of-Ten/blob/a6c2060b8175f505cc6327ccb5658cc00a458b24/.github/workflows/graphify.yml) · [Snapshots](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/ae544b6f6fffe511374404addb53e665ffe8a5c5) · [Dedicated HQ](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/434d03bcc55d98418c27eda562c8310be68296ab)
- The archived First Spark graph connects reward behavior to its case notes, Vitest and Playwright checks. It has no `implemented_in` edge. To change reward behavior, use the tests as leads and trace the implementation before editing. Its graph digest, commit and counts match the receipt. [First Spark evidence](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/ae544b6f6fffe511374404addb53e665ffe8a5c5/features/first-spark)
- Draft #157 still expects the v0.0.7 verifier and lock. The pinned `main` tree lacks both files after rollback #158. The earlier candidate CI therefore covers a different base from the one in scope here. [Draft #157](https://github.com/vixttha/AlderVale-Pact-of-Ten/pull/157) · [Tracked issue #159](https://github.com/vixttha/AlderVale-Pact-of-Ten/issues/159)
- README HQ holds six documentation maps. Test Vault holds three template maps. The launcher branches illustrate source-pinned reports and retained semantic extraction. Character Forge carries a code-only graph check and a draft documentation map check. These solve different discovery tasks. [README HQ](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/007617884c75b9f422fc0feda031042da62962eb) · [Test Vault](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/b0092267fd64e3025cbfece18db6d4fb3b1c356c) · [Launcher-agent draft](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/b4c1c3e2f2a6a942cb93b7ab38aed8a8052b1a88) · [Character Forge workflow run](https://github.com/vixttha/AlderVale-Pact-of-Ten/actions/runs/44426856844)
- The launcher-agent's retained semantic graph has 82 nodes and 91 edges, records `host_harness_unavailable` for model usage, and can be replayed from its retained extraction. This is a reference for a developer-facing document discovery mode with source anchors and clear extraction provenance. [Launcher-agent receipt](https://github.com/vixttha/AlderVale-Pact-of-Ten/blob/b4c1c3e2f2a6a942cb93b7ab38aed8a8052b1a88/Graphify%20HQ/v0.0.1/receipt.json)

### Lydite

- The three frozen Test Vault maps are present on all three branches. Lydite's v0.0.3 receipt and the upstream AlderVale Test Vault v0.0.3 receipt agree on the graph digest and the exact source SHA. The active hardening branch changes the builder while retaining the frozen maps and receipts. [Lydite maps](https://github.com/vixttha/Lydite-Test-Vault-Template/tree/fe7b00aa17862d7a01dfd15481594be837bc6d9f/Graphify%20HQ) · [AlderVale Test Vault archive](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/b0092267fd64e3025cbfece18db6d4fb3b1c356c/Graphify%20HQ)
- Draft #22 adds pinned-source fetching and an archived-map check to CI. The exact candidate passed all five jobs, including a rebuild of all three maps and rejection of byte drift. `main` still lacks that CI check and issue #12 remains open. [Draft #22](https://github.com/vixttha/Lydite-Test-Vault-Template/pull/22) · [Candidate run](https://github.com/vixttha/Lydite-Test-Vault-Template/actions/runs/44489163985) · [#12](https://github.com/vixttha/Lydite-Test-Vault-Template/issues/12)
- I ran the candidate's archive comparison function in a disposable Git fixture. It accepted a tracked file whose mode changed from `100644` to `100755` with identical bytes. The candidate's byte-drift checks and the executable-mode gap test different behavior. [Candidate source](https://github.com/vixttha/Lydite-Test-Vault-Template/blob/fbcf265dd72cd5e626204c6d99bfa2556771b09c/tools/graphify/version_maps.py#L49-L72) · [#17](https://github.com/vixttha/Lydite-Test-Vault-Template/issues/17)

## Branch inventory

Each branch links to the commit inspected. The file count includes tracked paths containing `graphify` and files named `graph.json` or `receipt.json`. Some matches are references or inherited workflows. Equal group numbers within a repository mean the matched path, Git mode, and blob sets are identical. The group is a file-set comparison and makes no claim about the rest of each branch. `chatgpt-voice` was checked through its commit and branch metadata, which identify the canonical empty Git tree.

### BART and Graphify HQ

| Branch | Exact commit | Matching files | Group |
| --- | --- | ---: | --- |
| `audit/public-wheel-platforms` | [`1980c487b965168206a187c0b74bdc15c4d69662`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/1980c487b965168206a187c0b74bdc15c4d69662) | 0 | B01 |
| `audit/v0.0.3-interchange` | [`05e9d13be0d9e58b2c79fd8f873fdd1adab446ba`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/05e9d13be0d9e58b2c79fd8f873fdd1adab446ba) | 0 | B01 |
| `audit/v0.0.3-platform` | [`4320357402951ad544c4a75c346b9a5c74029543`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/4320357402951ad544c4a75c346b9a5c74029543) | 0 | B01 |
| `audit/v0.0.3-release-diagnostics` | [`930be5ab22888ad68c2c8c5c31c516bf03c823a2`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/930be5ab22888ad68c2c8c5c31c516bf03c823a2) | 0 | B01 |
| `BART-Brand-Identity` | [`9741c63beaa237ab6fcd3672e2dff5e49e759b5b`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/9741c63beaa237ab6fcd3672e2dff5e49e759b5b) | 0 | B01 |
| `Brand-Identity-template-v0.0.1` | [`7ba49fca6600598a1e75cffbd318b50bd881b953`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/7ba49fca6600598a1e75cffbd318b50bd881b953) | 0 | B01 |
| `chatgpt-project-instructions` | [`388ddccdf6d84d302ce66392942873ab6c4347aa`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/388ddccdf6d84d302ce66392942873ab6c4347aa) | 5 | B02 |
| `ci/archive-graphify-v0.0.2` | [`ad138c853cc203eb8f162b020f42e4858f82d9c8`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/ad138c853cc203eb8f162b020f42e4858f82d9c8) | 9 | B03 |
| `ci/automatic-release-readiness` | [`e453d14e20812344b43e4d9f35280773a79d4328`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/e453d14e20812344b43e4d9f35280773a79d4328) | 0 | B01 |
| `ci/graphify-hq-evidence` | [`4be36ddaffe55b577c36afc1933b0be3d25b4d51`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/4be36ddaffe55b577c36afc1933b0be3d25b4d51) | 14 | B04 |
| `ci/graphify-obj-mtl-evidence` | [`e9ac6bc0f16810f5da052b0ee297038fa92979dd`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/e9ac6bc0f16810f5da052b0ee297038fa92979dd) | 11 | B05 |
| `ci/graphify-v0.0.3-candidate` | [`7461324bea232859ee4139e05debc6efa4735b37`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/7461324bea232859ee4139e05debc6efa4735b37) | 13 | B06 |
| `ci/publish-v0.0.2` | [`6eb2b3da2bfea6142ba97c594128a82bfba0a751`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/6eb2b3da2bfea6142ba97c594128a82bfba0a751) | 0 | B01 |
| `ci/readme-hq-v0.0.1-validation` | [`9d989e336b4df6a38fb36ef85acef276331345b5`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/9d989e336b4df6a38fb36ef85acef276331345b5) | 1 | B07 |
| `ci/reviewed-prerelease-notes` | [`4078ba48a0d6c33d060403863198daeb0f0ff94e`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/4078ba48a0d6c33d060403863198daeb0f0ff94e) | 0 | B01 |
| `code-stack` | [`b6cc0da8873902df1dd5304cd7946d1891e953b3`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/b6cc0da8873902df1dd5304cd7946d1891e953b3) | 0 | B01 |
| `code-stack-template` | [`ba2ce5c3c9d07602593078d4c97f89b6cdc6643b`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/ba2ce5c3c9d07602593078d4c97f89b6cdc6643b) | 8 | B08 |
| `dev/v0.0.3-checkpoints` | [`19a06c5cc1a18d91a130f26877ae7d69d5b3d96a`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/19a06c5cc1a18d91a130f26877ae7d69d5b3d96a) | 0 | B01 |
| `docs/archive-public-readme-v0.0.2` | [`f4be885966003eeae8673d264e74739f3a085dcc`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/f4be885966003eeae8673d264e74739f3a085dcc) | 1 | B07 |
| `docs/bart-code-stack-identity` | [`0e0600ca104a6c772eca0b2472b713681cab9317`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/0e0600ca104a6c772eca0b2472b713681cab9317) | 0 | B01 |
| `docs/bart-graphify-identity` | [`b495949810b0b7e2f36955bc4f30eb51bcefe73d`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/b495949810b0b7e2f36955bc4f30eb51bcefe73d) | 15 | B09 |
| `docs/bart-instructions-archive-identity` | [`b25661549f2f002d932750837150fa34a517a440`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/b25661549f2f002d932750837150fa34a517a440) | 5 | B02 |
| `docs/bart-rebrand-v0.0.3.1` | [`405ed2abd46f6f6981789bcaace6d7004b140172`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/405ed2abd46f6f6981789bcaace6d7004b140172) | 0 | B01 |
| `docs/graphify-v0.0.3-release` | [`986772015577595188aa2292202868ff19ab50a8`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/986772015577595188aa2292202868ff19ab50a8) | 15 | B10 |
| `docs/instructions-v0.0.3` | [`e5834fa6182f65c4013754b94355272d44a77f18`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/e5834fa6182f65c4013754b94355272d44a77f18) | 5 | B11 |
| `docs/public-readme-v0.0.1` | [`dde71a7b4299500fb742b6e1bdbadae519fb4c29`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/dde71a7b4299500fb742b6e1bdbadae519fb4c29) | 0 | B01 |
| `docs/publish-readme-v0.0.3` | [`fa8cde00f18c53b36a587177fac2c051f6f3a2d9`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/fa8cde00f18c53b36a587177fac2c051f6f3a2d9) | 0 | B01 |
| `docs/readme-hq-v0.0.1-audit` | [`e6e3c619b70ccd5f9ba9ec5a8c9edea1fb025156`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/e6e3c619b70ccd5f9ba9ec5a8c9edea1fb025156) | 1 | B07 |
| `docs/readme-v0.0.3-refresh` | [`a69e745875532b761341f7bfab799f294e59c894`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/a69e745875532b761341f7bfab799f294e59c894) | 1 | B07 |
| `docs/readme-v0.0.3-visual` | [`01995820c9e51e2f35462c5031a33cefd7b7613d`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/01995820c9e51e2f35462c5031a33cefd7b7613d) | 1 | B07 |
| `docs/readme-v0.0.4-bart` | [`6691ae80f401ced779558d40734789948585227f`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/6691ae80f401ced779558d40734789948585227f) | 1 | B12 |
| `docs/test-vault-planning` | [`2ada505088aacb7fb9451cb96ecd1d111175970b`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/2ada505088aacb7fb9451cb96ecd1d111175970b) | 0 | B01 |
| `feat/graphify-hq-runner-modes` | [`2780136a546bbaf88ba3e6d679c31343e9bd32f3`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/2780136a546bbaf88ba3e6d679c31343e9bd32f3) | 4 | B13 |
| `feature/code-stack-hub-v0.0.2` | [`336662e3ebf2a1d0ab4d0be2de74e4d2c6442033`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/336662e3ebf2a1d0ab4d0be2de74e4d2c6442033) | 0 | B01 |
| `feature/code-stack-hub-v0.0.3` | [`045421846d1b242953f675a973dcce49e58c1aee`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/045421846d1b242953f675a973dcce49e58c1aee) | 0 | B01 |
| `feature/code-stack-template-v0.0.2` | [`eed1c0ba5e88e014a669c94f9570af23bf06ef71`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/eed1c0ba5e88e014a669c94f9570af23bf06ef71) | 6 | B14 |
| `feature/code-stack-template-v0.0.3` | [`939307edbb8425f19e9e3824f097f12cc2dab1f3`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/939307edbb8425f19e9e3824f097f12cc2dab1f3) | 8 | B08 |
| `feature/v0.0.1-foundation` | [`2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b) | 0 | B01 |
| `fix/code-stack-archive-file-modes` | [`e72ad43ff7cacb367f99bb8e3b7ead0c0deeacb0`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/e72ad43ff7cacb367f99bb8e3b7ead0c0deeacb0) | 8 | B08 |
| `fix/obj-material-export` | [`d7886009b5121fc8a94f4f56d8209c3d04800d54`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/d7886009b5121fc8a94f4f56d8209c3d04800d54) | 0 | B01 |
| `graphify-hq` | [`2faf3674a5470c369b30f0d55b6fd5ef56e1e710`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/2faf3674a5470c369b30f0d55b6fd5ef56e1e710) | 15 | B09 |
| `graphify-hq-template` | [`6af3c2025be3f51e02dca4e4502088c526aae6d1`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/6af3c2025be3f51e02dca4e4502088c526aae6d1) | 4 | B15 |
| `main` | [`3e7f9e02e61739825b56bcafecebbd0221cc9657`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/3e7f9e02e61739825b56bcafecebbd0221cc9657) | 0 | B01 |
| `provenistem/graphify-hq` | [`ae9e55cd388de4b605945cd2a3871d55a2838e95`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/ae9e55cd388de4b605945cd2a3871d55a2838e95) | 4 | B15 |
| `readme-hq` | [`a1a5010b02ee39bdea3fa3ad3aff2e0ed5c270d8`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/a1a5010b02ee39bdea3fa3ad3aff2e0ed5c270d8) | 1 | B12 |
| `test-vault` | [`83f3ca3d520c52d187868ac24e116e8286828a7a`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/83f3ca3d520c52d187868ac24e116e8286828a7a) | 0 | B01 |
| `test/mcp-blender-workflow` | [`75774592873704dbec0c4651318e3fdcfa7e79d7`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/75774592873704dbec0c4651318e3fdcfa7e79d7) | 0 | B01 |

### AlderVale: Pact of Ten

| Branch | Exact commit | Matching files | Group |
| --- | --- | ---: | --- |
| `aldervale-element-design-v1` | [`e0cc7ab3b793da2af83185986b6fae550c1e5c69`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/e0cc7ab3b793da2af83185986b6fae550c1e5c69) | 0 | A01 |
| `AlderVale-Launcher` | [`1d4b6161b926503a62c9f37e9a16ab2bdc08ee24`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1d4b6161b926503a62c9f37e9a16ab2bdc08ee24) | 9 | A02 |
| `AlderVale-test-Vault` | [`bb1d5e609e0cc0a5c1a047df81dfc6e63df704e3`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/bb1d5e609e0cc0a5c1a047df81dfc6e63df704e3) | 0 | A01 |
| `AlderVale-Test-Vault` | [`cba804a4aebcc034500a54669e77c2630f3ba565`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/cba804a4aebcc034500a54669e77c2630f3ba565) | 10 | A03 |
| `assets/aldervale-logo-production` | [`09ac1c6b16ecaf1578a80707a72f63d54318438d`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/09ac1c6b16ecaf1578a80707a72f63d54318438d) | 9 | A04 |
| `assets/logo-workmark-v1-concept` | [`ff7da44a2c344deb2d0c7f322c17dfe0ad1ef3c4`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/ff7da44a2c344deb2d0c7f322c17dfe0ad1ef3c4) | 9 | A04 |
| `assets/rowan-glb` | [`b6239518bae3f916efcc239f3198e5468967fa92`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/b6239518bae3f916efcc239f3198e5468967fa92) | 0 | A01 |
| `audit/readonly` | [`646a26f11ff2389acda4066461ebaf51b56227c9`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/646a26f11ff2389acda4066461ebaf51b56227c9) | 0 | A01 |
| `branding/logo-workmark-v1` | [`4255e26eff8ecc79200a4508a7d24bcdcc1ff663`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/4255e26eff8ecc79200a4508a7d24bcdcc1ff663) | 9 | A04 |
| `bug-library` | [`c5422c097ba97ae04d00da1b743c1e49685cb470`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/c5422c097ba97ae04d00da1b743c1e49685cb470) | 0 | A01 |
| `bug-library-ci-receipt-checks` | [`d5efd81bd9130d3e1b0de111ac3ce844c9d6d4f5`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/d5efd81bd9130d3e1b0de111ac3ce844c9d6d4f5) | 0 | A01 |
| `bug-library-claim-issue-105` | [`d4e18d88a4b5b02e8a804f490a8e33e44631cfda`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/d4e18d88a4b5b02e8a804f490a8e33e44631cfda) | 9 | A04 |
| `bug-library-claim-issue-13` | [`852ec5410dacfc956d7de3f09a9e46e460b2fe4e`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/852ec5410dacfc956d7de3f09a9e46e460b2fe4e) | 0 | A01 |
| `bug-library-claim-issue-28` | [`6e643291db6d9dc6d3df2cad0351eddea92d850c`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/6e643291db6d9dc6d3df2cad0351eddea92d850c) | 0 | A01 |
| `bug-library-claim-issue-47` | [`cc8d109056eeaeb2576d7cf43b4d2c3fa0590b76`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/cc8d109056eeaeb2576d7cf43b4d2c3fa0590b76) | 0 | A01 |
| `bug-library-claim-issue-74` | [`e725bd02e1fabef574ce59b6bf99f63c213027f2`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/e725bd02e1fabef574ce59b6bf99f63c213027f2) | 0 | A01 |
| `bug-library-claim-issue-75` | [`18e992a00a2bfff60860f0149cc6db6f3eb18bfc`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/18e992a00a2bfff60860f0149cc6db6f3eb18bfc) | 9 | A04 |
| `bug-library-v0.0.3` | [`46c504ffdbd343df825398c403d3a0417acb9e82`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/46c504ffdbd343df825398c403d3a0417acb9e82) | 0 | A01 |
| `bug-library-v0.0.4` | [`712bd55b015138a4d7ab2d64708140c46d40d117`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/712bd55b015138a4d7ab2d64708140c46d40d117) | 0 | A01 |
| `bug-library-v0.0.4-integrated` | [`3fa20bc5ed4fecc228cc3733536a589bf75df6a0`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3fa20bc5ed4fecc228cc3733536a589bf75df6a0) | 9 | A04 |
| `bug-library-v0.0.4-level-2` | [`870f81f55f70ae6367943aeb48c6e8678fb42ca7`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/870f81f55f70ae6367943aeb48c6e8678fb42ca7) | 9 | A04 |
| `bug-library-v0.0.4-standalone` | [`5cf33b6c14ee5fb03e711d876c93426531dc7526`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/5cf33b6c14ee5fb03e711d876c93426531dc7526) | 0 | A01 |
| `bug-library-v0.0.5` | [`1005eb966499413658b157f1c7dbda6bfd5137a7`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1005eb966499413658b157f1c7dbda6bfd5137a7) | 0 | A01 |
| `character-forge-hq` | [`3c9b7b1f5f4f69fadf24d14f88862f2723e5f852`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3c9b7b1f5f4f69fadf24d14f88862f2723e5f852) | 10 | A05 |
| `chatgpt-voice` | [`010ef25a2754b189fe863ec7ca368678cc7a55b8`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/010ef25a2754b189fe863ec7ca368678cc7a55b8) | 0 | A01 |
| `ci/82-signed-in-browser` | [`3646551b4c26124a679af92b5469a13e676d0c45`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3646551b4c26124a679af92b5469a13e676d0c45) | 9 | A04 |
| `ci/audit-and-verify` | [`7b8bef99bf01e84169c7436c505fb4f26d72f138`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/7b8bef99bf01e84169c7436c505fb4f26d72f138) | 0 | A01 |
| `ci/bug-library-live-claim` | [`a5f93dce940fccb32449d6ef0515838b8fdde3fe`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/a5f93dce940fccb32449d6ef0515838b8fdde3fe) | 0 | A01 |
| `ci/bug-library-v0.0.3` | [`1390361616eb65c2071ee282e69f82ab7e79f306`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1390361616eb65c2071ee282e69f82ab7e79f306) | 9 | A04 |
| `ci/fusion-progression-audit` | [`41e03ef6bca15b358ee1a998bc8759cd77edd91b`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/41e03ef6bca15b358ee1a998bc8759cd77edd91b) | 9 | A04 |
| `ci/guest-playthrough-fix-pair` | [`efe7a44d39662279e4aba48cbe33562580b25388`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/efe7a44d39662279e4aba48cbe33562580b25388) | 9 | A04 |
| `ci/issue-13-campus-quests` | [`54e9266378ebff9a9791bf6a6fe29371bcf6dc28`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/54e9266378ebff9a9791bf6a6fe29371bcf6dc28) | 9 | A04 |
| `ci/issue-47-prestige-regression` | [`6cc9aa8bad92b1c072fd2d5c650daf93cbd92b5f`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/6cc9aa8bad92b1c072fd2d5c650daf93cbd92b5f) | 9 | A04 |
| `ci/readme-v002-media` | [`6e01fd69db2021273853de4471f13a6c369517e5`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/6e01fd69db2021273853de4471f13a6c369517e5) | 9 | A04 |
| `ci/repro-74-combat-ids` | [`4f02b7f6ed1abe01d444db25bfd3d7a27f6c6513`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/4f02b7f6ed1abe01d444db25bfd3d7a27f6c6513) | 9 | A04 |
| `ci/repro-75-live-creature` | [`7c4f77e75995b03c6be8dc7dc2360276b4b9bb64`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/7c4f77e75995b03c6be8dc7dc2360276b4b9bb64) | 9 | A04 |
| `ci/repro-76-ws-rate` | [`3322dd8b4dcbf748d11568b6b9b186d371a50b94`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3322dd8b4dcbf748d11568b6b9b186d371a50b94) | 9 | A04 |
| `ci/repro-77-firestore` | [`4b266977ba85b9f16be36dacdf1616582454d7c8`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/4b266977ba85b9f16be36dacdf1616582454d7c8) | 9 | A04 |
| `ci/repro-78-mute-identity` | [`0194cf4ffbec590d09cda16f60ae046f0c83a9f7`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/0194cf4ffbec590d09cda16f60ae046f0c83a9f7) | 9 | A04 |
| `ci/software-gl` | [`9d23545064acc4bbb9bb3024a9e5a60832c7910f`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/9d23545064acc4bbb9bb3024a9e5a60832c7910f) | 0 | A01 |
| `ci/webkit-container-proof` | [`2d0a092c792e231d30b10ce8032cb14ee60954ba`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/2d0a092c792e231d30b10ce8032cb14ee60954ba) | 9 | A04 |
| `codex/aldervale-branch-integration` | [`b0a17e5522fd194ea091480e7a7dae209b767dff`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/b0a17e5522fd194ea091480e7a7dae209b767dff) | 9 | A04 |
| `codex/aldervale-integration-2026-11-16` | [`7c861791c121d46f90fe8bb5b798507406f1f865`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/7c861791c121d46f90fe8bb5b798507406f1f865) | 9 | A04 |
| `codex/aldervale-play` | [`8d9bfc0964b9204b2517714a2472019a9c5f52ef`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/8d9bfc0964b9204b2517714a2472019a9c5f52ef) | 9 | A04 |
| `codex/all-17-gameplay-repairs` | [`f64f08b2ec66b8843bce56508ca854d8d363f131`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/f64f08b2ec66b8843bce56508ca854d8d363f131) | 0 | A01 |
| `codex/all-agent-consolidation-2026-11-16` | [`3671386156177a7238d928eb66dbf228b401e46b`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3671386156177a7238d928eb66dbf228b401e46b) | 9 | A04 |
| `codex/fix-105-fusion-progression` | [`07b93506e7c8aef1c0a9188d0f37cf0f0c567a34`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/07b93506e7c8aef1c0a9188d0f37cf0f0c567a34) | 9 | A04 |
| `codex/fix-coop-resonance-69` | [`18fc2dfe3b0eab6032b58ce65c327f23ed07bdfd`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/18fc2dfe3b0eab6032b58ce65c327f23ed07bdfd) | 9 | A04 |
| `codex/fix-rare-element-decks-and-spell-unlocks` | [`ecb7e7041835a36ea25048e480bb5c1c576dc373`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/ecb7e7041835a36ea25048e480bb5c1c576dc373) | 9 | A04 |
| `codex/human-glb` | [`11768994308aee4ed150aea197f7330af5ee0376`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/11768994308aee4ed150aea197f7330af5ee0376) | 0 | A01 |
| `codex/magma-pact-prototype` | [`5f147e7b5a06e83297efbf67b1a4b5bdb38f6e9c`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/5f147e7b5a06e83297efbf67b1a4b5bdb38f6e9c) | 9 | A04 |
| `codex/main-bug-fixes-2026-11-16` | [`e13f1bf46b90e5f859c84a7211bfcc1e52b28c59`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/e13f1bf46b90e5f859c84a7211bfcc1e52b28c59) | 9 | A04 |
| `codex/resource-isolation-consolidation-2026-11-16` | [`40b12b1e611f129dc35544b9a073813651d011ea`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/40b12b1e611f129dc35544b9a073813651d011ea) | 9 | A04 |
| `codex/rowan-playable` | [`680d08b7c27f054dd6b622e9fb770ff7fd07c62e`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/680d08b7c27f054dd6b622e9fb770ff7fd07c62e) | 0 | A01 |
| `codex/rowan-run-loop` | [`27f16f367f9a5ebf01a9780532a60e1aabd2a5d5`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/27f16f367f9a5ebf01a9780532a60e1aabd2a5d5) | 9 | A04 |
| `codex/runner-validation` | [`a826e22a347caabcb85528906b7f77f3f9397444`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/a826e22a347caabcb85528906b7f77f3f9397444) | 0 | A01 |
| `codex/test-vault-candidate` | [`43743dbc436717c52053e50044cf9e0dd7d48ac8`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/43743dbc436717c52053e50044cf9e0dd7d48ac8) | 0 | A01 |
| `cursor/aldervale-cursor-v002-3081` | [`5a52e77c46461e8cfde014a224a1d920143d0079`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/5a52e77c46461e8cfde014a224a1d920143d0079) | 0 | A01 |
| `cursor/aldervale-loop-agent-3081` | [`6f4dbe16b6a46d5d5d308c70e23e55999b9bf001`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/6f4dbe16b6a46d5d5d308c70e23e55999b9bf001) | 0 | A01 |
| `cursor/aldervale-v001-wording-3081` | [`8fb7af5a35507a6d911b1a9fefe46091a30bae62`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/8fb7af5a35507a6d911b1a9fefe46091a30bae62) | 9 | A04 |
| `cursor/fix-41-42-44-c4b4` | [`24a69e61831c12928a14a385fb9a5ce827caa7a2`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/24a69e61831c12928a14a385fb9a5ce827caa7a2) | 9 | A04 |
| `cursor/fix-issue-43-lead-creature-c4b4` | [`3bf9520756a474edd1d0c54f32b24648b54784e9`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3bf9520756a474edd1d0c54f32b24648b54784e9) | 9 | A04 |
| `cursor/graphify-rerun-6052` | [`6425790db86f965aee42e949ebbcd3738c8ea167`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/6425790db86f965aee42e949ebbcd3738c8ea167) | 9 | A06 |
| `cursor/issue-28-bazaar-equipped-c4b4` | [`a7090a18d14c5c3504390ba0230eaf4d79ae90aa`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/a7090a18d14c5c3504390ba0230eaf4d79ae90aa) | 9 | A04 |
| `cursor/semgrep-weekly-scan-6bd2` | [`391d78ec8275c83eee4c488db516112c055931ff`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/391d78ec8275c83eee4c488db516112c055931ff) | 0 | A01 |
| `cursor/small-bugs-batch-2-c4b4` | [`2e6d4c310058c56912a9d48e2cb462de2b1f6472`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/2e6d4c310058c56912a9d48e2cb462de2b1f6472) | 9 | A04 |
| `cursor/smaller-issues-dorm-ratings-c4b4` | [`dcf469a25cfe46bb388ae89727b125f0bbc348aa`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/dcf469a25cfe46bb388ae89727b125f0bbc348aa) | 9 | A04 |
| `cursor/three-day-horizon-5788` | [`eeb589d4b3e64a8060cc025c96661ea6b70c39c2`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/eeb589d4b3e64a8060cc025c96661ea6b70c39c2) | 0 | A01 |
| `docs/archive-public-readme-v0.0.2` | [`019dbc5c1d831fdbd9f3f8c9d61e46355b7e5b6a`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/019dbc5c1d831fdbd9f3f8c9d61e46355b7e5b6a) | 0 | A01 |
| `docs/creator-privacy` | [`50a4416a465b7453258c6247a45437c433ab993a`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/50a4416a465b7453258c6247a45437c433ab993a) | 9 | A04 |
| `docs/graphify-hq-v0.0.7` | [`d36152f7f1763828c43994d669983c10f9314aba`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/d36152f7f1763828c43994d669983c10f9314aba) | 18 | A07 |
| `docs/owner-directed-agent-roles-2026-11-15` | [`563264a9d748f546572dd7a15b0687e08c3c61fc`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/563264a9d748f546572dd7a15b0687e08c3c61fc) | 0 | A01 |
| `docs/project-wide-audit-2026-11-16` | [`3ad84e47f9dcb67c8fece483aaec284994a551ac`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3ad84e47f9dcb67c8fece483aaec284994a551ac) | 9 | A04 |
| `docs/public-readme-v0.0.2` | [`8a527110d1370f4e2e37b0968acb222131f13b94`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/8a527110d1370f4e2e37b0968acb222131f13b94) | 0 | A01 |
| `docs/public-readme-v0.0.3` | [`bc8a13887336975e6391c2de0b69c17e951b6855`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/bc8a13887336975e6391c2de0b69c17e951b6855) | 0 | A01 |
| `docs/public-readme-v0.0.4` | [`645092e574c0137a48cd668f2aae67292a55b1ae`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/645092e574c0137a48cd668f2aae67292a55b1ae) | 23 | A08 |
| `docs/publish-public-readme-v0.0.2` | [`5efa508500e1daf2a8531e030eab221e60d3086c`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/5efa508500e1daf2a8531e030eab221e60d3086c) | 9 | A04 |
| `docs/publish-public-readme-v0.0.3` | [`2070f6a3c66df020a9812f948da2220606cd1db7`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/2070f6a3c66df020a9812f948da2220606cd1db7) | 9 | A04 |
| `docs/publish-public-readme-v0.0.4` | [`0373e5372335b41cda8dfc7987c17def392bc8e3`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/0373e5372335b41cda8dfc7987c17def392bc8e3) | 9 | A04 |
| `docs/readme-hq` | [`1666731a4771ec3ccf7f878467107dfcc20ec18d`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1666731a4771ec3ccf7f878467107dfcc20ec18d) | 9 | A04 |
| `docs/readme-hq-99-v0.0.3-draft` | [`45e61d344deb294f5cb0b49d1676224f71e4ab37`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/45e61d344deb294f5cb0b49d1676224f71e4ab37) | 0 | A01 |
| `docs/readme-hq-graphify-map` | [`5b8c0cf7f890946101794a6e18e632ee3564e472`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/5b8c0cf7f890946101794a6e18e632ee3564e472) | 20 | A09 |
| `docs/readme-hq-v0.0.4` | [`f653296f4105ad6098845b3e0d06bf26479df345`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/f653296f4105ad6098845b3e0d06bf26479df345) | 0 | A01 |
| `docs/readme-hq-v0.0.5` | [`341cbcab8c49ebdb2266971b5da8d7453a96b09f`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/341cbcab8c49ebdb2266971b5da8d7453a96b09f) | 0 | A01 |
| `docs/readme-hq-v0.0.6` | [`c6c1a253e9f5995849177f65ceafc444ecf5e19e`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/c6c1a253e9f5995849177f65ceafc444ecf5e19e) | 23 | A08 |
| `docs/readme-v002-campus` | [`3328aa6ec47b04f71f0eeafbae4ae16ad94cf275`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3328aa6ec47b04f71f0eeafbae4ae16ad94cf275) | 9 | A04 |
| `docs/readme-v002-render` | [`cf3991745922002acc6c870a65e689c2cffaaa65`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/cf3991745922002acc6c870a65e689c2cffaaa65) | 0 | A01 |
| `docs/readme-v002-root-review` | [`1ff41eaed4dfdd5fbad625824e15f48dc2bb4d21`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1ff41eaed4dfdd5fbad625824e15f48dc2bb4d21) | 0 | A01 |
| `docs/readme-v003-root-review` | [`1542374ea23e32a0ed906423e1c148614a0ad5cb`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1542374ea23e32a0ed906423e1c148614a0ad5cb) | 9 | A04 |
| `element-hq-v1` | [`6fd35f2076b75830d10d7131fb15a9eda4483745`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/6fd35f2076b75830d10d7131fb15a9eda4483745) | 0 | A01 |
| `fix-issue-75-live-creature-selection` | [`48a615062064c699c88fdc96c9663269394c758d`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/48a615062064c699c88fdc96c9663269394c758d) | 9 | A04 |
| `fix/75-live-creature-selection` | [`f88bc516cc4efed3a6c344fd53284994d701af03`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/f88bc516cc4efed3a6c344fd53284994d701af03) | 9 | A04 |
| `fix/82-authoritative-progression` | [`a242c6b3f6e48c7b12dc985a937c6a310be5eee8`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/a242c6b3f6e48c7b12dc985a937c6a310be5eee8) | 9 | A04 |
| `fix/audit-integration` | [`57071d72c9971a20b434cd0239b2dff647346371`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/57071d72c9971a20b434cd0239b2dff647346371) | 0 | A01 |
| `fix/bug-library-standalone-boundary` | [`445d9cf9be32cf49c9ed0935a76fa609125a161f`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/445d9cf9be32cf49c9ed0935a76fa609125a161f) | 9 | A04 |
| `fix/deterministic-combat-effect-ids` | [`783ec4ff24e3423fd4a8234f599cbc1cb0a77ccb`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/783ec4ff24e3423fd4a8234f599cbc1cb0a77ccb) | 9 | A04 |
| `fix/first-spark-browser` | [`8345e2f446b2ccbfed56d6be6d041ab798f36511`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/8345e2f446b2ccbfed56d6be6d041ab798f36511) | 9 | A04 |
| `fix/guest-migration-35` | [`0c942c2ce75ab325a76c56f6ca6e5caeb11a2762`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/0c942c2ce75ab325a76c56f6ca6e5caeb11a2762) | 9 | A04 |
| `fix/guest-prestige-lineages` | [`44f28f518d13a632f2c0706dac5305ac284ca6dc`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/44f28f518d13a632f2c0706dac5305ac284ca6dc) | 9 | A04 |
| `fix/issue-13-campus-quest-reward-tests` | [`e46768e4d5a729e6c5fe10bab2d9effc13e9a1ff`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/e46768e4d5a729e6c5fe10bab2d9effc13e9a1ff) | 9 | A04 |
| `fix/issue-75-authenticated-matchmaking-ci` | [`e22c0dcc43db2d5e700f943e23ff871c8a1a05e2`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/e22c0dcc43db2d5e700f943e23ff871c8a1a05e2) | 9 | A04 |
| `fix/readme-hq-73-validator` | [`5d82035e0cd7514da4dcdeaf1d3485d4f71d7f79`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/5d82035e0cd7514da4dcdeaf1d3485d4f71d7f79) | 0 | A01 |
| `fix/repository-audit` | [`979e470369833c2d7a50afe00c4e8c71dafaab51`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/979e470369833c2d7a50afe00c4e8c71dafaab51) | 0 | A01 |
| `graphify-hq` | [`434d03bcc55d98418c27eda562c8310be68296ab`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/434d03bcc55d98418c27eda562c8310be68296ab) | 18 | A10 |
| `graphify-snapshots` | [`ae544b6f6fffe511374404addb53e665ffe8a5c5`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/ae544b6f6fffe511374404addb53e665ffe8a5c5) | 16 | A11 |
| `Launcher-Agent-Template` | [`b4c1c3e2f2a6a942cb93b7ab38aed8a8052b1a88`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/b4c1c3e2f2a6a942cb93b7ab38aed8a8052b1a88) | 11 | A12 |
| `main` | [`a6c2060b8175f505cc6327ccb5658cc00a458b24`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/a6c2060b8175f505cc6327ccb5658cc00a458b24) | 9 | A04 |
| `notion-agent` | [`1e9bdd538f71cd39d98c2255550c152e445ef211`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1e9bdd538f71cd39d98c2255550c152e445ef211) | 9 | A04 |
| `ops/agent-graphify` | [`37f66c9dfd0bd01b70224ac3a5c30aa7dfab36f8`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/37f66c9dfd0bd01b70224ac3a5c30aa7dfab36f8) | 7 | A13 |
| `ops/chatgpt-project-folder-instructions-v0.0.1` | [`ce4d76db15856a8b620c0736155359692bf283b0`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/ce4d76db15856a8b620c0736155359692bf283b0) | 9 | A04 |
| `ops/chatgpt-project-instructions-v0.0.1` | [`470451f7cb8eaf81160b69582954e2b235242649`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/470451f7cb8eaf81160b69582954e2b235242649) | 0 | A01 |
| `ops/graphify-first-spark` | [`d3eb63ddb04163bdb8771f2c60fe6df23d753e7a`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/d3eb63ddb04163bdb8771f2c60fe6df23d753e7a) | 20 | A14 |
| `ops/graphify-hq-v0.0.7-archive` | [`94dc2324285d56574d8cef86eb724d923372ada4`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/94dc2324285d56574d8cef86eb724d923372ada4) | 19 | A15 |
| `ops/revert-graphify-hq-main` | [`64bb7a492c62a31c3abfb3da960b505fc031f219`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/64bb7a492c62a31c3abfb3da960b505fc031f219) | 9 | A04 |
| `policy/public-hosted-runners-guard` | [`8f746b4195255d8cf09c00b355f46b501a655481`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/8f746b4195255d8cf09c00b355f46b501a655481) | 9 | A04 |
| `readme-hq` | [`007617884c75b9f422fc0feda031042da62962eb`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/007617884c75b9f422fc0feda031042da62962eb) | 23 | A08 |
| `Test-Vault` | [`b0092267fd64e3025cbfece18db6d4fb3b1c356c`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/b0092267fd64e3025cbfece18db6d4fb3b1c356c) | 12 | A16 |
| `test-vault/bash-graphify` | [`6bb5f0df86d2fc7ddb559f114ea69c539f6f36c9`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/6bb5f0df86d2fc7ddb559f114ea69c539f6f36c9) | 10 | A17 |
| `test-vault/consolidate-v0.0.2` | [`29105a580b4d570103f5cca2fe3bd87561a85567`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/29105a580b4d570103f5cca2fe3bd87561a85567) | 10 | A17 |
| `test-vault/cpp-game-contracts` | [`fbcd7ffea604b139589c01be59b15b4c1eaf414b`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/fbcd7ffea604b139589c01be59b15b4c1eaf414b) | 9 | A04 |
| `test-vault/cross-language-testing-rules` | [`a34713cc053f0d88d33c8336a8f5385c324cda6a`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/a34713cc053f0d88d33c8336a8f5385c324cda6a) | 10 | A03 |
| `test-vault/csharp-guest-saves` | [`2e8872b44b473403ed03c395456b391a92be7a62`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/2e8872b44b473403ed03c395456b391a92be7a62) | 9 | A04 |
| `test-vault/first-spark-evidence` | [`5364cd19c862dbf071faeea58d9245e110d3b377`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/5364cd19c862dbf071faeea58d9245e110d3b377) | 10 | A03 |
| `test-vault/fsharp-quest-sequences` | [`a13507d7fc8e027f724e0651fd22edcca9f51653`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/a13507d7fc8e027f724e0651fd22edcca9f51653) | 9 | A04 |
| `test-vault/go-guest-presence` | [`fcdc30668f78ad4596aa7ee6d5289a5da5cc3a0b`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/fcdc30668f78ad4596aa7ee6d5289a5da5cc3a0b) | 9 | A04 |
| `test-vault/graphify-snapshot` | [`2317dfffb22b5ee3ec7185c0ef1cb073029723fd`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/2317dfffb22b5ee3ec7185c0ef1cb073029723fd) | 10 | A03 |
| `test-vault/haskell-spell-cards` | [`423d30c3520ea10674edea5f89246676226b9d0a`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/423d30c3520ea10674edea5f89246676226b9d0a) | 10 | A03 |
| `test-vault/java-asset-delivery` | [`eb6e09954ede0f43560d826c57896e06936c3262`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/eb6e09954ede0f43560d826c57896e06936c3262) | 10 | A03 |
| `test-vault/lua-campus-movement` | [`897a5fd6955efbd6eab9389248b2960d379ccfb8`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/897a5fd6955efbd6eab9389248b2960d379ccfb8) | 10 | A03 |
| `test-vault/powershell-launcher` | [`cea7020c695196d788072511ab82cb2d53a344df`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/cea7020c695196d788072511ab82cb2d53a344df) | 9 | A04 |
| `test-vault/public-template` | [`9e030719ebfbe9c261e68aa7941f9438e363d6e3`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/9e030719ebfbe9c261e68aa7941f9438e363d6e3) | 9 | A04 |
| `test-vault/python-runner-policy` | [`3894f6a2d5d9e72a1d8d207a5667a66caed4bb8b`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/3894f6a2d5d9e72a1d8d207a5667a66caed4bb8b) | 9 | A04 |
| `test-vault/v0.0.2` | [`1914f2197cf42e0dfb50bbdb364bd41903e4406c`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/1914f2197cf42e0dfb50bbdb364bd41903e4406c) | 9 | A04 |
| `test-vault/v0.0.3` | [`bb5cff192509a69f92c8b1ca9bd26ef8b8ea14f6`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/bb5cff192509a69f92c8b1ca9bd26ef8b8ea14f6) | 12 | A16 |
| `test/element-combat-baseline` | [`afcd82ec3e2fd5ce134b55984f63ae7a36f5f537`](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/afcd82ec3e2fd5ce134b55984f63ae7a36f5f537) | 9 | A04 |

### Lydite Test Vault

| Branch | Exact commit | Matching files | Group |
| --- | --- | ---: | --- |
| `feat/standalone-language-vault` | [`7189e358ee0c443d67d2108c15cbd6984a4fc637`](https://github.com/vixttha/Lydite-Test-Vault-Template/tree/7189e358ee0c443d67d2108c15cbd6984a4fc637) | 12 | L01 |
| `hardening/v0.0.3` | [`fbcf265dd72cd5e626204c6d99bfa2556771b09c`](https://github.com/vixttha/Lydite-Test-Vault-Template/tree/fbcf265dd72cd5e626204c6d99bfa2556771b09c) | 12 | L02 |
| `main` | [`fe7b00aa17862d7a01dfd15481594be837bc6d9f`](https://github.com/vixttha/Lydite-Test-Vault-Template/tree/fe7b00aa17862d7a01dfd15481594be837bc6d9f) | 12 | L01 |
