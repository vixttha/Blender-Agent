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

Use Python 3.12 and tools/graphify/requirements.txt. The dependencies are pinned to the independently validated AlderVale Graphify environment, including graphifyy 0.9.109 and MCP 2.3.0.

On a checkout of graphify-hq with complete Git history and release tags:

    python -m pip install --only-binary=:all: --no-deps -r tools/graphify/requirements.txt
    python tools/graphify/version_maps.py --self-test
    python tools/graphify/version_maps.py --generate
    python tools/graphify/version_maps.py --check

The generator produces versions/<version>/README.md, graph.json, and receipt.json. The --check mode creates files in a temporary directory, queries each graph with Graphify MCP over stdio, and compares every output byte with what is committed. A missing, extra, or changed file fails. The --self-test mode uses a synthetic Markdown fixture, tests negative catalog inputs, checks reproducible output bytes, and queries graph_stats and get_node through the same MCP server.

For a generated graph, the local Graphify tool can expose read-only discovery functions:

    python -m graphify.serve versions/v1.0.0/graph.json

Only run that example after v1.0.0 has genuinely been approved and archived. The standard workflow needs no Graphify ChatGPT connection. A separately connected Graphify client can read the same portable graph.json data when available; this branch does not install or authorize a ChatGPT-side connector.

## Public-runner policy

.github/workflows/graphify-hq.yml runs on push or PR targeting graphify-hq, using standard GitHub-hosted ubuntu-latest and read-only permissions. It installs the locked Graphify dependencies, runs a deterministic self-test, and checks all committed version archives. It does not publish artifacts automatically, merge, release, call a private service, or depend on local hardware.

Because the catalog is intentionally empty at bootstrap, the initial runner checks the real template with a **synthetic fixture only**. It does not misrepresent that sample as an approved Blender-Agent release.
