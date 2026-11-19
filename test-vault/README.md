# Blender-Agent Refinement Toolkit Test Vault

This Test Vault uses the starter shipped in [Lydite v0.0.4](https://github.com/vixttha/Lydite-Test-Vault-Template/releases/tag/v0.0.4), pinned to [`87d25d80d3154d295052412b64b29a0f0f152c27`](https://github.com/vixttha/Lydite-Test-Vault-Template/commit/87d25d80d3154d295052412b64b29a0f0f152c27). Start with the [test plan and current status](PLAN.md). Use the [case catalog](cases.md) for case IDs, priorities, and expected outcomes.

The installed starter covers catalog validation and optional execution receipts. New receipts can bind the exact case plan and shared observation bytes. Matching v1 plans and receipts remain readable. The bundled Node.js and Python example exercises the template in a disposable checkout with its example case registered. It is separate from the Blender-Agent Refinement Toolkit catalog and suite. See the [language plan](PLAN.md#test-languages) for proposed use of Lydite's native inventory.

A planned case describes what to build. An implemented case has a runnable assertion. A verified outcome has a case-specific result from the relevant runner and checkout. A catalog run checks the case definitions. A smoke job can succeed while an individual case records a known mismatch.

Use [Case and run receipt](case-and-receipt.md) to record results. [Execution receipts](evidence.md) describes the optional JSON format. See the [upgrade guide](UPGRADE.md) and [changelog](CHANGELOG.md) for template history.

## Build tests for the target project

1. Read the repository's contributor instructions, existing tests and CI. Identify the entry point, supported environments and the behavior or failure you want to protect.
2. Give the case a stable ID and record the expected result. Choose a test layer and framework that exercise the real entry point. Use fixtures for controlled state and known failure cases.
3. Put the executable test in the target project's normal test directory and add it to that project's test command. Use separate test data and environments for tests that need a service.
4. Run the project's test command and the Vault catalog validator on standard public GitHub-hosted runners. Record the test command, target checkout, result and any coverage limits in the [case and receipt form](case-and-receipt.md).

The starter checks your catalog. The target project's test commands execute its tests. Both can run with the project's existing CI.

## Add your cases

Copy the five-column table in [cases.md](cases.md). Use an uppercase topic followed by a hyphen and at least three digits. Examples include `CLI-001`, `HTTP-GET-001`, and `G13-001`. IDs are unique across all case tables. Keep all five cells populated and use `P0`, `P1`, or `P2` for priority. Escape literal table pipes as `\|`. Put a Markdown divider row directly under each table header. Use fenced code blocks outside the tables for examples.

To enforce topic coverage in CI, add `test-vault/topics.json` as a JSON array of unique topic IDs, for example `["CLI", "HTTP-GET"]`. The included workflow checks that each registered topic has a case and every case uses a registered topic. The equivalent catalog command for a public runner is:

```sh
python3 test-vault/validate_catalog.py --topics test-vault/topics.json
```

Use [case and receipt](case-and-receipt.md) to link a case to the actual test command and result. Catalog validation checks documentation structure and optional topic coverage. A test case earns execution evidence when the relevant test runs and its result is recorded.

## GitHub Actions

The [catalog workflow](../.github/workflows/test-vault.yml) validates the catalog on standard public GitHub-hosted Ubuntu. The [application workflow](../.github/workflows/ci.yml) executes the existing Python, MCP and Blender checks on public Ubuntu and Windows. Use the actual checkout and case result when recording evidence. See the [test plan](PLAN.md) for the planned additions to these suites.
