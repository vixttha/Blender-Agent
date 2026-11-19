# Public README v0.0.1 review

The candidate describes [foundation PR #1](https://github.com/vixttha/Blender-Agent/pull/1) at `45726472fbe7f32de32f87426dc0b21b8fc1e8f7`. [Foundation CI](https://github.com/vixttha/Blender-Agent/actions/runs/44431079525) covers Python 3.11 and 3.12 on Linux and Windows and Blender 4.5.0 headless create, STL → GLB → STL conversion, and repair on Ubuntu. Individual MCP hosts and other Blender format combinations need their own verification.

## README HQ checks

The [workflow](../../.github/workflows/readme-hq.yml) uses a GitHub-hosted Ubuntu runner with read-only repository permissions. The check discovers version folders from the tree, verifies index entries, compares the live HQ pages with the newest archived HQ version, and checks existing archive folders against the event baseline. It scans Markdown, including public drafts, for common private-data patterns. It checks relative paths, same-repo HQ links, pinned Git links, and common Markdown heading fragments. External HTTP status and Markdown syntax beyond the supported link forms are review items.

The workflow also installs the package at the revision named in the quick start and checks the synthetic triangle’s CLI version, geometry counts, bounds, and digest.

## Publication

[Draft PR #2](https://github.com/vixttha/Blender-Agent/pull/2) is the proposed public homepage. Both PRs edit the root README. If the foundation lands first, recheck the comparison against the new `main` and resolve any README conflict before publication. Record the accepted README and changelog in the public version history after approval.
