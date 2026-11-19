# Run and refresh Code Stack

## First run

Provide a Git repository, a ref, and an output directory. Code Stack resolves the ref to a commit, classifies tracked entries, detects known manifests and first-party sources, and generates the three outputs described in the [README](README.md). A GitHub origin contributes exact-commit source links. Other Git repositories still get source paths and blob IDs. Use `--project` to set a stable display name across differently named local clones. A hosted run can set `--template-commit` to the full archive pin.

Each candidate is a draft recommendation. **Keep** favors an observed implementation, **adopt** nominates a candidate for a specified unmet role, **defer** calls for more evidence or a concrete requirement, and **drop** identifies a known mismatch for a role. A finding of co-located languages and manifests does not prove a dependency or deployed use. The inventory uses file patterns and executable shebangs, so generated paths outside recognized conventions may need review. CI definitions indicate intended checks. Use actual job logs for runtime claims.

## Add a future requirement when you know it

The first scan needs no configuration. Pass `--context goals.json` if you want it to compare languages for a planned capability. Each goal has a component path, role, and requirement.

~~~json
{
  "goals": [
    {"component": "preview", "role": "browser", "need": "Preview exported assets without opening the desktop application"}
  ]
}
~~~

Role IDs and their comparison catalogs are in [language_profiles.py](tools/language_profiles.py). Add a goal where the tree lacks evidence for a planned component. Put project information suitable for the output audience in the context file.

## Record an owner decision

Add `--approve decisions.json` on the approved source commit to record explicit decisions. The recommendation continues to show the tool's judgment. An approval must identify a candidate in the generated report.

~~~json
[
  {"component": ".", "role": "cli", "language": "Python", "action": "keep", "reason": "Preserve the shared command and library code"}
]
~~~

## Rerun

~~~sh
python3 tools/stack.py --repo /path/to/project --ref main \
  --previous /path/to/previous/code-stack.json --out /path/to/new-review
~~~

Supply the same context if it still applies. The new registry carries earlier owner decisions and marks them for review if recommendation evidence or a recommendation changes. Decisions also remain visible when the component or candidate disappears. If the earlier commit is unavailable, Git path comparisons are incomplete and fingerprints still surface recommendation changes. The receipt hashes detect a report and registry that came from different write attempts. Retain or archive the generated registry to supply it on future runs.

## Public CI and migration

[workflow.example.yml](workflow.example.yml) is an optional workflow for a public repository. Place it in its default branch to use the manual trigger. It reads the triggering commit and retains the resulting report. The template archive workflow checks the portable kit on multiple pinned projects.

The [legacy audit tool](tools/audit.py) and its tests are included for existing schema 2 registries. Run a new review to generate schema 3. Carry any earlier owner decision with explicit approval input on its corresponding recommendation. Schema 2 records remain readable through the legacy entry point and as their original archival evidence.
