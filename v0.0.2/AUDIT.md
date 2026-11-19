# Run a Code Stack audit

## Install and discover

Copy the contents of this version directory into your hub. Start with Git and Python 3.8 or newer. The template workflow tests the Python available on Ubuntu. The target checkout must be at the full application commit you intend to audit.

~~~sh
python3 tools/audit.py --repo /path/to/source --discover FULL_COMMIT_SHA --json inventory.json
~~~

Review the grouped results. Tracked first-party language files and formats are listed separately. Paths under common generated and vendor directories are reported as such. Document an override when a path’s role differs from the convention. Simple executable shebangs are detected in small extensionless files. Embedded formats and ambiguous files such as Vue, Svelte, notebooks, and Gradle go to review. Gitlinks and symbolic links need review within their own scope. Review embedded shell in CI directly. The checker uses filename and path heuristics and does not execute the target code.

## Complete the registry

Copy registry.example.json to code-stack.json. Replace all placeholders and bind important repo-file evidence to a real path in the checked-out commit.

| Field | Use |
| --- | --- |
| schema_version | Integer 2 |
| project, source_commit | Nonblank project name and full Git commit ID |
| source_repository, source_ref, source_state, template_commit | Optional provenance. Set the canonical owner/repository when known. |
| required_paths, docs_only_paths | Optional lists of regular required files and explicitly approved documentation-only paths |
| reviewed_paths | Map from a pending tracked path to its review reason |
| overrides | Map from a regular tracked path to kind, reason, and name for a language or format. Available kinds are language, format, generated, and vendored. |
| source_checks | Map from tracked regular paths to nonempty lists of expected literal fragments |
| technologies | Unique name, status, basis, role, and evidence IDs |
| sources | Unique ID, kind, HTTPS URL, claim, review state, and kind-specific provenance |

Technology status is active, conditional, research, or retired. For active entries, basis is language, format, or source. Tracked first-party programming languages must be declared active. Declared active formats need a matching file. Use source for runtime or embedded technologies, with repository-file evidence. Other technologies may use proposal. Inventory can include incidental formats without a registry row.

Evidence kind is repo-file, ci-run, or upstream. A repo-file needs the audit commit and a regular tracked path. A GitHub blob link must match that location when the canonical repository is supplied. A ci-run needs its tested commit. Upstream sources can be versioned in the URL. Review is unchecked or reviewed. Record an ISO date in reviewed_on for a reviewed entry. Review status is a reviewer-provided assertion. The checker validates structure and location and does not fetch links or assess claims. Source fragments prove the presence of text. Use application CI for behavior.

## Compare and retain evidence

~~~sh
python3 tools/audit.py --repo /path/to/source --config code-stack.json \
  --live-ref refs/remotes/origin/main --release-ref refs/tags/v1.2.3 \
  --json audit.json --summary summary.md
~~~

The pinned checkout stays at the audited commit. The comparison refs must be fully qualified refs already fetched into that same repository. Fetch history and tags if you need ancestry or release comparisons. Use the target’s actual branch and tag. A comparison reports current, docs-only, stack-relevant, or unknown. Only the standard root README, changelog and contribution paths, plus explicitly listed docs-only paths, qualify as documentation drift. Changes outside that set require review. A different commit with an identical tree is reported in the docs-only group with an explanation. Missing refs or unavailable ancestry give unknown. A freshness result is informational.

Full JSON can be written to a file. The audit prints a CODE_STACK_RECEIPT JSON line and writes the same receipt to the requested job summary. It includes source and template provenance, file counts, freshness, evidence scope, and the run identifiers available in GitHub Actions. Use the existing runner retention for receipts. Include only information appropriate for the target repository’s visibility.

## Add CI when needed

Copy workflow.example.yml to .github/workflows/code-stack-audit.yml. The example assumes a kit folder named code-stack inside the hub tree and a target in the same repository. Adjust the branch, paths, and comparison refs. Place code-stack.json beside tools in the kit. The example uses a public standard Ubuntu runner, a push trigger, read-only permissions, and no persistent checkout credentials. GitHub requires workflow files on the default branch for manual dispatch. The template deliberately omits that trigger for branch-only installations.

The supplied fixture tests inventory, drift, registry validation, receipt output and adoption from a separate copied-kit directory. Apply the destination project's rules to additional checks and evidence. Record proposed changes and owner decisions using the proposal and memory files.
