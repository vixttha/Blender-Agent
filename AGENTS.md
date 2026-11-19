# Agent operating rules

This repository is a public, reusable toolkit. Keep its content project-focused: no personal biography, private project details, identifying user information or secrets in source, examples, logs or documentation. GitHub's public account metadata remains GitHub-managed.

1. Read README.md, docs/ARCHITECTURE.md, docs/SKILL_POLICY.md, and SECURITY.md before execution-boundary changes.
2. Keep the neutral public project identity Blender-Agent. Another brand identity remains unapproved for public deployment.
3. Preserve original inputs; non-overwriting publication must be atomic, including concurrent workloads.
4. Treat imported assets as untrusted data and never execute model-generated Python, shell commands or unreviewed skills.
5. Host the CLI/MCP through a configured trusted workspace; the path guard does not replace OS sandboxing.
6. Report actual tests, simulated tests, and unverified claims separately. Geometry counts are not printability or production certifications.
7. Do not fragment the shared core into harness-specific implementations. Extend adapters instead.
8. Use one scoped work lane: Head selects → Worker implements → Validate exact SHA → Internal Auditor challenges → Head requests merge approval and archives evidence.
9. Use free, standard GitHub-hosted public runners only; never depend on paid or self-hosted runners.
10. Work through PRs, preserve test provenance and do not automatically merge or release.

v0.0.2 is the in-review repair candidate for six identified v0.0.1 findings, not a general autonomous asset creator.
