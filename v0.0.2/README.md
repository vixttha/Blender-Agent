# Code Stack v0.0.2

Code Stack inventories tracked files at a pinned Git commit and records the evidence behind a project’s languages, formats, and tool choices.

- [Stack](STACK.md) and [memory](STACK_MEMORY.md) carry the project handoff.
- [Audit guide](AUDIT.md) explains setup, results, and the evidence contract.
- [Registry](registry.example.json) gives a schema v2 example. [Migration](MIGRATION.md) shows how to retain an earlier baseline.
- [Proposal](PROPOSAL.md) records a proposed stack change, its trade-offs, validation, and rollback.
- [Workflow example](workflow.example.yml) is optional. It audits from a standard public runner.

Copy this version directory into a separate hub or a folder in a repository. Set the repository URL and working project name, pin the application source, run discovery, then prepare the registry. Keep each accepted snapshot addressable by commit. The template and project installation can evolve at their own pace.
