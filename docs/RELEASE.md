# Releases

## Automatic readiness

GitHub Actions runs the **Release readiness (read-only)** job after the Python, MCP stdio, and real Blender jobs pass. Open the CI run summary for the tested commit, package version, CI run ID, and tag availability. Pull requests get a preview. Use the successful push run on the current default branch for publication. This check starts automatically and needs no manual dispatch.

## Owner-approved publication

The repository owner's manual workflow dispatch records approval for one final tag, one full commit SHA, and one successful application CI push run. Select the default branch at the approved commit and supply the three values in the dispatch. The package's version at that commit must match the tag.

The **Verify release approval** workflow verifies the owner identity, the default branch head, and every job in the exact application CI run. It runs with read-only permissions on a standard public GitHub runner.

When you approve publication, open **Prepare or publish a Blender-Agent pre-release**, enter the tag, commit, and CI run ID from the default-branch CI summary, and check **Publish the verified pre-release**. The job verifies owner approval first. It then uses the verified tag and SHA, confirms the default-branch head again, and creates the tag at that SHA before publishing the GitHub pre-release. The publishing job alone receives `contents: write`. An existing tag causes tag creation to fail. If tagging succeeds and publication fails, inspect the tag and failed run before authorizing recovery.

The standard CI unit tests exercise invalid owner, ref, SHA, version, CI run, and job results with synthetic inputs. The public pull-request check also feeds the authentic GitHub event to the publication verifier and requires a rejection. An optional dispatch with the Publish box unchecked exercises the live owner approval gate.
