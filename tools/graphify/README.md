# Blender-Agent version graph workflow

This workspace adapts the version-by-version Graphify HQ pattern already used for AlderVale, but tracks **Blender-Agent software releases**, not game or README HQ template versions.

## Approval and source contract

The catalog lives at catalog/versions.json. A record must have:

- version: vMAJOR.MINOR.PATCH (unique, strictly ascending).
- source_commit: an exact 40-hex Git commit SHA from this repository.
- release_tag: the same version tag, resolving to that exact commit.
- source_files: one or more unique, repository-relative public Markdown paths at that commit.

Only explicitly approved versions belong in the catalog. No release is implied by a branch, proposed tag, milestone, or version string. Avoid personal data and private/internal documents. Graphify HQ does not discover arbitrary files or scrape external links.

Example record for a *future approved release only* (not part of the active catalog):

    {
      "version": "v1.0.0",
      "source_commit": "<full-public-commit-sha>",
      "release_tag": "v1.0.0",
      "source_files": ["README.md", "docs/ARCHITECTURE.md"]
    }

## Generate, validate, and browse

Use CPython 3.12 on Linux x86-64. The requirements lock pins each wheel by SHA-256, including Graphify 0.9.109 and MCP 2.3.0.

On a checkout of graphify-hq with complete Git history and release tags:

    python -m pip install --require-hashes --only-binary=:all: --no-deps -r tools/graphify/requirements.txt
    python -m pip check
    python tools/graphify/version_maps.py --self-test
    python tools/graphify/version_maps.py --generate
    python tools/graphify/version_maps.py --check

The generator produces versions/<version>/README.md, graph.json, and receipt.json. The --check mode creates files in a temporary directory, queries each graph with Graphify MCP over stdio, and compares every output byte with what is committed. A missing, extra, or changed file fails. The --self-test mode uses a synthetic Markdown fixture, tests negative catalog inputs, checks reproducible output bytes, and queries graph_stats and get_node through the same MCP server.

For a generated graph, the local Graphify tool can expose read-only discovery functions:

    python -m graphify.serve versions/v1.0.0/graph.json

Only run that example after v1.0.0 has genuinely been approved and archived. The standard workflow needs no Graphify ChatGPT connection. A separately connected Graphify client can read the same portable graph.json data when available; this branch does not install or authorize a ChatGPT-side connector.

## Public-runner policy

.github/workflows/graphify-hq.yml runs on push or PR targeting graphify-hq, using standard GitHub-hosted ubuntu-latest and read-only permissions. It verifies each installed wheel against the hash lock and checks both the synthetic fixture and the committed archives.

## Unapproved release candidates

Unmerged or draft PRs go into catalog/candidates.json, **not** catalog/versions.json. A candidate records its exact full source commit, public PR number, source branch, and sorted Markdown documents. Its graph and receipt are generated under candidates/vX.Y.Z with `archive_status: candidate` and `release_tag: null`. A candidate is **not** evidence of an approved release.

`python tools/graphify/candidate_maps.py --generate` writes the candidate archive after validating source provenance and MCP read-back. Use `--emit` to print generated files as bounded JSON chunks. After committing the snapshot, `--check` independently rebuilds and compares every byte.

Candidate verification checks the GitHub-reported PR number, source branch, repository and commit. A historical commit must appear in the PR's GitHub commit list. The workflow run summary records the current PR state, PR head, merge commit when present, and the count of review approvals on the archived SHA. This live observation stays in CI so the historical graph and receipt retain stable bytes as reviews and PR state change. The review count is informational; promotion still requires the approved release and matching tag.

## Feature traceability

Either catalog can add a `features` list to a version record. Each entry supplies an ID, a label, a documentation path already in `source_files`, an exact changelog bullet, and one or more test references. A test reference contains the test file path and its complete declaration line with indentation removed. Git resolves those citations from the pinned commit. Missing or ambiguous declarations fail generation.

Graphify links each version to features and each feature to its documentation, changelog entry and tests. The receipt hashes the referenced source blobs. These links identify relevant test code. Test results belong to the application CI run for the source commit.

Promotion requires a separately approved and immutable main-line release: update catalog/versions.json with the real release commit and matching tag, generate the approved map under versions/vX.Y.Z, and independently verify it. Never rename or silently relabel the candidate receipt as approved.
