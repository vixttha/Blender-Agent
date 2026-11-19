# Blender-Agent Refinement Toolkit Test Vault

Based on [Test Vault v0.0.3](https://github.com/vixttha/AlderVale-Pact-of-Ten/tree/dafb72e042b61b5b24217d1f2fc1d3231d8c0f29/starter). Start with the [test plan and current status](PLAN.md). Use the [case catalog](cases.md) for case IDs, priorities, and expected outcomes.

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

To enforce topic coverage in CI, add `test-vault/topics.json` as a JSON array of unique topic IDs, for example `["CLI", "HTTP-GET"]`. The included workflow checks that each registered topic has a case and every case uses a registered topic. To run the same check locally:

```sh
python3 test-vault/validate_catalog.py --topics test-vault/topics.json
```

Use [case and receipt](case-and-receipt.md) to link a case to the actual test command and result. Catalog validation checks documentation structure and optional topic coverage. A test case earns execution evidence when the relevant test runs and its result is recorded.

## Configure GitHub Actions

The included workflow runs on pull requests and merge queues on standard hosted Ubuntu. It also runs after pushes to the repository's default branch and supports manual dispatch. Enable Actions in the target repository and allow its pinned checkout and Python setup actions. Fork runs may require maintainer approval.

Public repositories use standard hosted compute. Private repositories skip by default. A maintainer can set repository Actions variable `TEST_VAULT_ENABLE_PRIVATE=true` after verifying the runner allowance and budget. For a required check, first enable the job for your repository visibility. Then select **Test Vault catalog** after a successful validation run. If the repo uses a merge queue, verify the check also reports on `merge_group`. Keep the required workflow free of path restrictions. Teams using a different runner policy can use the local command or adapt the runner configuration in their own repository.

For a new repository, initialize it and copy this kit. A maintainer of a dedicated GitHub template repository can keep these files on its default branch for GitHub's **Use this template** flow.
