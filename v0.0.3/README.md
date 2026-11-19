# Code Stack Template v0.0.3

One Git ref produces a language inventory, component-level comparisons, a decision report, and an evidence receipt. The kit uses Git and Python 3.11 or newer with no Python packages to install. It scans a Git tree as data.

## Run the kit

~~~sh
python3 tools/stack.py --repo /path/to/project --ref main --out /path/to/review
~~~

Use any available branch, tag, or commit. Git worktrees and bare clones are supported. A checkout at a different commit and uncommitted files have no effect. The current Git branch is the default when `--ref` is omitted.

| Output | Contents |
| --- | --- |
| `REPORT.md` | Observed stack, language candidates by component, benefits, tradeoffs, evidence, and decisions to revisit |
| `code-stack.json` | Schema 3 inventory, component and toolchain signals, recommendations, Git blobs, and carried decisions |
| `receipt.json` | Exact source SHA, template version, optional template pin, and SHA-256 of the report and registry |

Use [AUDIT.md](AUDIT.md) for planned work, approvals, and reruns. [STACK.md](STACK.md) reloads the steward role in a fresh session. [PROPOSAL.md](PROPOSAL.md) records a change that needs a project-specific decision.

The kit supports a broad extension inventory and a smaller curated comparison catalog. Familiar manifests give component and runtime signals. Unrecognized or ambiguous evidence stays visible for review. The report uses committed source and bundled primary references. Benchmarks, live upstream claims and passing application CI need separate proof.
