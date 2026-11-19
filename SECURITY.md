# Graphify HQ security and operational boundaries

Graphify HQ is a public read-only discovery workspace, not an agent-control plane.

- All catalog entries must resolve to commits and matching version tags in the same public Blender-Agent repository. The generator accepts Markdown source documents only and reads them through git, never by contacting arbitrary URLs.
- The build is deterministic and offline after the pinned dependencies have been installed. Graphify MCP is served over a local stdio subprocess solely to query the generated graph.
- The workflow uses contents: read and a checkout without persisted credentials. It does not use repository secrets, issue access, write tokens, self-hosted runners, local PCs, or deployment keys.
- Never include credentials, machine-local paths, private drafts, personal names, or personal contact information in version maps or documents.
- A valid graph receipt proves graph provenance and reproducibility, not source-code safety, Blender compatibility, release readiness, or authorization to merge.
- Version records are immutable after acceptance. If the same version needs a correction, record and review the change explicitly; do not silently rewrite accepted history.
- Do not merge this sparse HQ branch wholesale into main. Publish separate approved changes to main, when applicable.
