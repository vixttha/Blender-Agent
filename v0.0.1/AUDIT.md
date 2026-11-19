# Run a Code Stack audit

## Map the project

1. Read the project's entrypoint and operating rules. Find the canonical application ref, active candidates and any separately maintained product components. Record the full commit and whether it is released, merged or proposed. Audit more than one component if a single commit cannot cover the scope.
2. List tracked files and manifests. Check entrypoints, dependency and lock files, build and test jobs, code generation, deployment requirements and contributors' setup instructions. Notice languages embedded in other formats, generated or vendored code, notebooks, platform-specific scripts, submodules and ambiguous extensions.
3. For each technology record its role, supported versions, compatibility, licensing or recurring costs when material, and evidence. Use the source tree for use, upstream docs for capabilities, and logs for tested combinations. Treat public popularity as context and measure claimed gains where they affect a decision.
4. Record what is missing or stale. A change to the target branch needs fresh application evidence. Mark fixtures, source-only checks and actual runtime checks distinctly.
5. Put proposal trade-offs in a proposal record. Update memory and the index when evidence or an owner decision changes.

## Run the portable checks

Check out the **target** project at the actual source commit in a separate directory. Keep the template's tools outside that checkout. Git and Python 3 are needed for this audit utility. The audited project can use any stack.

~~~sh
python3 tools/audit.py --repo /path/to/project --discover FULL_COMMIT_SHA
python3 tools/audit.py --repo /path/to/project --config code-stack.json --json audit.json
python3 tools/test_audit.py
~~~

Copy registry.example.json to code-stack.json and replace the example data. Use discovery output to build your registry. Record source languages found in tests and repository tooling as well as shipped code, and give each a precise role. For ambiguous text files, use an exact path in reviewed_paths or an explicit language override. Check generated, vendored and unusual tracked files in the audit scope. Attach the report to a review or retain it in a job summary.

The check reads only a tracked Git tree and selected evidence fragments. It checks required paths, the active language inventory and evidence references. It does not build the target or run its code. A reviewer still assesses upstream sources, embedded languages, benchmark results, runtime support and whether a language change is worth its cost. Use the target project's runner policy. For public GitHub projects, the example runs on a free standard GitHub-hosted Ubuntu runner with read-only repository access.
